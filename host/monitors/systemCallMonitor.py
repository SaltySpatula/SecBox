import os
from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Process
import json
import socketio
import platform

healthy_server_address = "/tmp/healthy_gvisor_events.sock"
infected_server_address = "/tmp/infected_gvisor_events.sock"

healthy_configuration_file = "SecBox/host/healthy/session.json"
infected_configuration_file = "SecBox/host/infected/session.json"

base_command = "bazel run examples/seccheck:server_cc"


class systemCallMonitor:
    def __init__(self, sandbox_id) -> None:
        self.base_command = base_command
        self.sandbox_id = sandbox_id
        self.client = None
        self.ps = []
        self.arch = platform.processor()

    def run(self):
        p = Process(target=self.runInParallel, args=(
            self.monitoring_process, self.monitoring_process, "healthy", "infected"))
        p.start()
        self.ps.append(p)

    def start(self):
        self.run()
        return self

    def stop(self):
        for p in self.ps:
            p.kill()

    def monitoring_process(self, infected_status):
        self.client = socketio.Client()
        self.client.connect('http://localhost:5000', namespaces=['/sysCall'])
        print("syscall monitor started")
        order_count = 0
        cwd = os.getcwd() + "/gvisor-master/"
        command = self.base_command + " /tmp/" + \
            infected_status + "_gvisor_events.sock"
        print(command)
        running_command = Popen(command.split(),
                             stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=cwd)
        print("Running cmd in ")
        print(cwd)
        for line in running_command.stdout:
            print(line)
            order_count = order_count+1
            message = {
                "ID": self.sandbox_id,
                "architecture": self.arch,
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
            self.ps.append(p)
