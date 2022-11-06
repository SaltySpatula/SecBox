import docker
from multiprocessing import Process
import json
import socketio
import os
import time


path = "/home/raf/PycharmProjects/SecBox"
healthy_dockerfile = path + "/host/healthy/"
infected_dockerfile = path + "/host/infected/"


class Controller:
    def __init__(self, mw_hash, os, sandbox_id) -> None:
        self.client = socketio.Client()
        self.client.connect('http://localhost:5000', namespaces=['/sandbox'])
        self.mw_hash = mw_hash
        self.os = os
        self.sandbox_id = sandbox_id

        # setup healthy and infected instances
        # TODO: Parse OS and Malware & build correct dockerfile
        self.healthyInstance = Instance(
            healthy_dockerfile, "healthy", self.sandbox_id)
        self.infectedInstance = Instance(
            infected_dockerfile, "infected", self.sandbox_id)

    def __enter__(self):
        self.start_instances()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_instances()

    def stop_instances(self):
        if self.healthyInstance is not None and self.infectedInstance is not None:
            self.healthyInstance.stop_instance()
            self.infectedInstance.stop_instance()
        self.healthyInstance = None
        self.infectedInstance = None

    def start_instances(self) -> None:
        if self.healthyInstance is None and self.infectedInstance is None:
            # start instances
            self.healthyInstance.start_instance()
            self.infectedInstance.start_instance()
            self.client.emit('sandboxReady', json.dumps(
                {"ID": self.sandbox_id}), namespace='/sandbox')
            print("Sandbox Ready")

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

    def terminate_command(self):
        pass
        # ToDo: implement a way to stop a running command e.g. ping google.com
        # e.g. through ps -aux , find process running currently runniing command and kill


class Instance:
    def __init__(self, dockerfile, infection_status, sandbox_id) -> None:
        self.dockerfile = dockerfile
        self.docker_client = docker.from_env()
        print(dockerfile)
        (self.image, self.logs) = self.docker_client.images.build(path=dockerfile)

        self.log_generator = None
        self.infection_status = infection_status
        self.client = socketio.Client()
        self.client.connect('http://localhost:5000', namespaces=['/cmd'])
        self.sandbox_id = sandbox_id
        self.order_count = 0
        self.current_path = ""

        # set up docker networking
        self.network = self.docker_client.networks.create(
            str(self.sandbox_id) + infection_status + "_network")
        self.bridge = "br-" + self.network.short_id
        # set up docker container
        print(self.image)
        print(self.network.name)
        self.container = self.docker_client.containers.run(
            self.image, runtime='runsc-trace-'+self.infection_status, detach=True, tty=True, network=self.network.name)

    def stop_instance(self) -> int:
        if self.container is not None:
            self.container.stop()
            self.container = None
            self.network.remove()

    def execute_command(self, command):
        if self.container is not None:
            if command[:2]=="cd":
                wd = command.split()[1]
                if wd[-1] != "/":
                    wd += "/"
                self.current_path += wd
                command = "bash -c " + command
            console_output = self.container.exec_run(
                command, stream=True, workdir=self.current_path).output
            for line in console_output:
                self.order_count = self.order_count +1 
                message = {
                    "ID": self.sandbox_id,
                    "infectedStatus": self.infection_status,
                    "orderNo": self.order_count,
                    "cmdOut": line.decode('utf-8')
                }
                self.client.emit('cmdOut', json.dumps(
                    message), namespace='/cmd')