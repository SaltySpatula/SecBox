import os
from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Process
import json

healthy_server_address = "/tmp/healthy_gvisor_events.sock"
infected_server_address = "/tmp/infected_gvisor_events.sock"

healthy_configuration_file = "SecBox/host/healthy/session.json"
infected_configuration_file = "SecBox/host/infected/session.json"

base_command = "bazel run examples/seccheck:server_cc"


class systemCallMonitor:
    def __init__(self, client, sandbox_id) -> None:
        self.base_command = base_command
        self.sandbox_id = sandbox_id
        self.client = client
        self.ps = []

    def run(self):
        self.mp = Process(target=self.runInParallel, args=(self.monitoring_process, self.monitoring_process, "healthy", "infected"))
        self.mp.start()

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for p in self.ps:
            p.join()
        self.mp.join()

    def monitoring_process(self, infected_status):
        order_count = 0
        cwd = os.getcwd() + "/host/gvisor-master/"
        command = self.base_command + " /tmp/" + \
            infected_status + "_gvisor_events.sock"
        print(command)
        # ToDo: rename self.process
        self.process = Popen(command.split(),
                             stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=cwd)
        for line in self.process.stdout:
            order_count = order_count+1
            message = {
                "ID": self.sandbox_id,
                "infectedStatus": infected_status,
                "orderNo": order_count,
                "sysCall": str(line)
            }
            self.client.emit('sysCall', json.dumps(message), namespace='/sysCall')

    def runInParallel(self, fn1, fn2, arg1, arg2):
        fns = [fn1, fn2]
        args = [arg1, arg2]
        procs = []
        for index in range(len(fns)):
            p = Process(target=fns[index], args=(args[index],))
            p.start()
            procs.append(p)
        self.ps = procs
