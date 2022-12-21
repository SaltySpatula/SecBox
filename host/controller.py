import docker
from multiprocessing import Process
import json
import socketio
import time

syscalls_to_monitor = 384

healthy_dockerfile = "healthy"
infected_dockerfile = "infected"


class Controller:
    def __init__(self, mw_hash, os, sandbox_id) -> None:
        self.client = socketio.Client()
        self.client.connect('http://localhost:5000', namespaces=['/sandbox'])
        self.mw_hash = mw_hash
        self.os = os
        self.sandbox_id = sandbox_id

        healthy_args = {
            "os_image": self.os
        }
        infected_args = {
            "os_image": self.os,
            "malware_hash": self.mw_hash
        }

        self.healthyInstance = Instance(
            healthy_dockerfile, "healthy", self.sandbox_id, healthy_args)
        self.infectedInstance = Instance(
            infected_dockerfile, "infected", self.sandbox_id, infected_args)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_instances()

    def stop_instances(self):
        if self.healthyInstance is not None and self.infectedInstance is not None:
            self.healthyInstance.stop_instance()
            self.infectedInstance.stop_instance()
        self.healthyInstance = None
        self.infectedInstance = None

    def runInParallel(self, healthyfn, infectedfn, command):
        fns = [healthyfn, infectedfn]
        proc = []
        for fn in fns:
            p = Process(target=fn, args=(command,))
            p.start()
            proc.append(p)
        for p in proc:
            p.join()

    def execute_command(self, command):
        self.runInParallel(self.healthyInstance.execute_command,
                           self.infectedInstance.execute_command, command)


class Instance:
    def __init__(self, dockerfile, infection_status, sandbox_id, build_arguments) -> None:
        self.dockerfile = dockerfile
        self.docker_client = docker.from_env()
        print(dockerfile)
        (self.image, self.logs) = self.docker_client.images.build(
            path=dockerfile, buildargs=build_arguments)

        self.log_generator = None
        self.infection_status = infection_status
        self.client = socketio.Client()
        self.client.connect('http://localhost:5000', namespaces=['/cmd'])
        self.sandbox_id = sandbox_id
        self.order_count = 0
        self.current_path = "/"

        syscall_monitoring_str = """{"trace_session": {"name": "Default",
            "points": ["""
        for i in range(syscalls_to_monitor):
            syscall_config = """
            {{
                "name": "syscall/sysno/{}/enter",
                "context_fields": [
                    "time",
                    "container_id",
                    "thread_id",
                    "credentials",
                    "cwd"
                ]
            }}""".format(i)
            if i != 0:
                syscall_monitoring_str = syscall_monitoring_str + "," + syscall_config
            else:
                syscall_monitoring_str = syscall_monitoring_str + syscall_config
        syscall_monitoring_str = syscall_monitoring_str + "],"
        sinks = """
            "sinks": [
                {{
                    "name": "remote",
                    "config": {{
                    "endpoint": "/tmp/{}_{}_gvisor_events.sock",
                    "retries": 3
                }},
            "ignore_setup_error": true
        }}
        ]
    }}
}}"""
        sinks = sinks.format(self.infection_status, self.sandbox_id)

        session = syscall_monitoring_str + sinks
        # Reconfigure the session
        session_path = self.infection_status+"/session.json"
        with open(session_path, "w+") as f:
            f.write(session)

        # set up docker container
        self.container = self.docker_client.containers.run(
            self.image, runtime='runsc-trace-'+self.infection_status, detach=True, tty=True)
        time.sleep(1)
        self.container = self.docker_client.containers.get(self.container.name)
        # set up docker networking
        self.ip = self.container.attrs['NetworkSettings']['IPAddress']

        # Setup Malware to be ready to execute
        if self.infection_status == "infected":
            install_malware_cmd = 'wget -O malware.7z --post-data query="get_file&sha256_hash=' + \
                str(build_arguments["malware_hash"]) + \
                '" https://mb-api.abuse.ch/api/v1/'
            unzip_malware_cmd = '7z e -pinfected malware.7z'
            deinstall_pkgs_cmd = 'apt-get uninstall -y unzip && apt-get uninstall -y wget'

            self.container.exec_run(
                install_malware_cmd, workdir=self.current_path)
            self.container.exec_run(
                unzip_malware_cmd, workdir=self.current_path)
            self.container.exec_run(
                deinstall_pkgs_cmd, workdir=self.current_path)
            print("Malware infection successful")

    def stop_instance(self) -> int:
        if self.container is not None:
            self.container.stop()
            self.container.remove(force=True)
            self.container = None

    def execute_command(self, command):
        message = {
            "ID": self.sandbox_id,
            "infectedStatus": self.infection_status,
            "orderNo": self.order_count,
            "isFirst": True,
            "isLast": False,
            "cmdOut": self.current_path+" $ "+command
        }
        self.client.emit('cmdOut', json.dumps(message), namespace='/cmd')
        if self.container is not None:
            wd = ""
            if command[:2] == "cd":
                wd = command.split()[1]
                if wd[-1] != "/":
                    wd += "/"
                self.current_path += wd
                command = "bash -c " + command
                if self.container.exec_run(command, workdir=self.current_path).exit_code:
                    # Remove failed cd from path
                    end_index = len(wd)
                    self.current_path = self.current_path[:-end_index]
            console_output = self.container.exec_run(
                command, stream=True, workdir=self.current_path).output
            while True:
                try:
                    line = next(console_output)
                    self.order_count = self.order_count + 1
                    message = {
                        "ID": self.sandbox_id,
                        "infectedStatus": self.infection_status,
                        "orderNo": self.order_count,
                        "isFirst": False,
                        "isLast": False,
                        "cmdOut": line.decode('utf-8')
                    }
                    self.client.emit('cmdOut', json.dumps(
                        message), namespace='/cmd')
                except StopIteration:
                    self.order_count = self.order_count + 1
                    message = {
                        "ID": self.sandbox_id,
                        "infectedStatus": self.infection_status,
                        "orderNo": self.order_count,
                        "isFirst": False,
                        "isLast": True,
                        "cmdOut": ""
                    }
                    self.client.emit('cmdOut', json.dumps(
                        message), namespace='/cmd')
                    break
                except:
                    self.order_count = self.order_count + 1
                    message = {
                        "ID": self.sandbox_id,
                        "infectedStatus": self.infection_status,
                        "orderNo": self.order_count,
                        "isFirst": False,
                        "isLast": True,
                        "cmdOut": "Invalid Input"
                    }
                    self.client.emit('cmdOut', json.dumps(
                        message), namespace='/cmd')
                    break
