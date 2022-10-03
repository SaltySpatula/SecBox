import docker
from multiprocessing import Process


class Controller:
    def __init__(self) -> None:
        self.healthyInstance = None
        self.infectedInstance = None

    def __enter__(self):
        self.start_instances("./healthy/", "./infected/")
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
            self.healthyInstance = Instance(healthy_dockerfile, "healthy")
            self.infectedInstance = Instance(infected_dockerfile, "infected")
            # start instances
            self.healthyInstance.start_instance()
            #self.infectedInstance.start_instance()

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
        #e.g. through ps -aux , find process running currently runniing command and kill


class Instance:
    def __init__(self, dockerfile, infection_status) -> None:
        self.dockerfile = dockerfile
        self.client = docker.from_env()
        (self.image, self.logs) = self.client.images.build(path=dockerfile)
        self.container = None
        self.log_generator = None
        self.infection_status = infection_status

    def stop_instance(self) -> int:
        if self.container is not None:
            self.container.stop()
            self.container = None

    def start_instance(self) -> int:
        if self.container is None:
            self.container = self.client.containers.run(
                self.image, runtime='runsc-trace-'+self.infection_status, detach=True, tty=True)

    def execute_command(self, command):
        if self.container is not None:
            console_output = self.container.exec_run(
                command, stream=True).output
            for line in console_output:
                print(self.infection_status + str(line))
                # ToDo: Stream Output to websockets from Controller
