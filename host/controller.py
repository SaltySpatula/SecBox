import docker
from multiprocessing import Process
import json


class Controller:
    def __init__(self, client, mw_hash, os, sandbox_id) -> None:
        self.healthyInstance = None
        self.infectedInstance = None
        self.client = client
        self.mw_hash = mw_hash
        self.os = os
        self.sandbox_id = sandbox_id

    def __enter__(self):
        self.start_instances("./host/healthy/", "./host/infected/")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_instances()

    def stop_instances(self):
        if self.healthyInstance is not None and self.infectedInstance is not None:
            self.healthyInstance.stop_instance()
            self.infectedInstance.stop_instance()
        self.healthyInstance = None
        self.infectedInstance = None

    def start_instances(self, healthy_dockerfile, infected_dockerfile) -> int:
        if self.healthyInstance is None and self.infectedInstance is None:
            # setup healthy and infected instances
            self.healthyInstance = Instance(
                healthy_dockerfile, "healthy", self.client, self.sandbox_id)
            self.infectedInstance = Instance(
                infected_dockerfile, "infected", self.client, self.sandbox_id)
            # start instances
            self.healthyInstance.start_instance()
            self.infectedInstance.start_instance()
            self.client.emit('sandboxReady', json.dumps({"ID": self.sandbox_id}), namespace='/sandbox')
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
    def __init__(self, dockerfile, infection_status, client, sandbox_id) -> None:
        self.dockerfile = dockerfile
        self.docker_client = docker.from_env()
        (self.image, self.logs) = self.docker_client.images.build(path=dockerfile)
        self.container = None
        self.log_generator = None
        self.infection_status = infection_status
        self.client = client
        self.sandbox_id = sandbox_id
        self.order_count = 0

        #set up docker networking
        self.network = self.docker_client.networks.create(str(self.sandbox_id) + infection_status + "_network")
        self.bridge = "br-" + self.network.short_id

    def stop_instance(self) -> int:
        if self.container is not None:
            self.container.stop()
            self.container = None
            self.network.remove()
    
    def get_container_veth(self):
        pass


    def start_instance(self) -> int:
        if self.container is None:

            self.container = self.docker_client.containers.run(
                self.image, runtime='runsc-trace-'+self.infection_status, detach=True, tty=True, network=self.network.name)
            self.veth_device = get_container_veth
            

    def execute_command(self, command):
        if self.container is not None:
            console_output = self.container.exec_run(
                command, stream=True).output
            for line in console_output:
                ++self.order_count
                message = {
                    "ID": self.sandbox_id,
                    "infectedStatus": self.infection_status,
                    "orderNo": self.order_count,
                    "cmdOut": line
                }
                self.client.emit('cmdOut', json.dumps(message), namespace='/cmd')
