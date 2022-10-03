import socket
import os
from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Process

healthy_server_address = "/tmp/healthy_gvisor_events.sock"
infected_server_address = "/tmp/infected_gvisor_events.sock"

healthy_configuration_file = "SecBox/host/healthy/session.json"
infected_configuration_file = "SecBox/host/infected/session.json"

base_command = "bazel run examples/seccheck:server_cc"


class systemCallMonitor():
    def __init__(self) -> None:
        self.base_command = base_command

    def run(self):
        self.mp = Process(target=self.runInParallel, args=(self.monitoring_process, self.monitoring_process, "healthy", "infected"))
        self.runInParallel(self.monitoring_process, self.monitoring_process,
                           "healthy", "infected")

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for p in self.ps:
            p.join()
        self.mp.join()

    def monitoring_process(self, infected_status):
        cwd = os.getcwd() + "/gvisor-master/"
        command = self.base_command + " /tmp/" + \
            infected_status + "_gvisor_events.sock"
        print(command)
        # ToDo: rename self.process
        self.process = Popen(command.split(),
                             stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=cwd)
        with open(infected_status + "_syscalls.log", "w+") as f:
            for line in self.process.stdout:
                print(line, file=f)
                # ToDo: Stream over Websocket

    def runInParallel(self, fn1, fn2, arg1, arg2):
        fns = [fn1, fn2]
        args = [arg1, arg2]
        procs = []
        for index in range(len(fns)):
            p = Process(target=fns[index], args=(args[index],))
            p.start()
            procs.append(p)
        self.ps = procs
