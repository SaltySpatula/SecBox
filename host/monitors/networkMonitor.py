from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Process
import json
import scapy.all as scapy
import socketio


class networkMonitor:
    def __init__(self, sandbox_id, controller) -> None:
        self.sandbox_id = sandbox_id
        self.client = None
        self.controller = controller
        self.ps = []

    def monitoring_process(self, infected_status):
        self.client = socketio.Client()
        self.client.connect('http://localhost:5000', namespaces=['/network'])
        print("network monitor started")
        order_count = 0
        instance = None
        if infected_status=="healthy":
            instance = self.controller.healthyInstance
        else:
            instance = self.controller.infectedInstance
        print(instance.bridge)
        command = "sudo tcpdump -i " + instance.bridge
        process = Popen(command.split(),
                             stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        for packet in process.stdout:
            order_count = order_count+1
            message = {
                "ID": self.sandbox_id,
                "infectedStatus": infected_status,
                "orderNo": order_count,
                "packet": (packet.decode('UTF-8'))
            }
            self.client.emit('packet', json.dumps(message), namespace='/network')

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

    def runInParallel(self, fn1, fn2, args1, args2):
        fns = [fn1, fn2]
        args = [(args1,), (args2,)]
        procs = []
        for index in range(len(fns)):
            p = Process(target=fns[index], args=args[index])
            p.start()
            procs.append(p)
        self.ps = procs
