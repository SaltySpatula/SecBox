from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Process
import json
from scapy.all import *
import socketio
import contextlib, io

class networkMonitor:
    def __init__(self, sandbox_id, controller) -> None:
        self.sandbox_id = sandbox_id
        self.client = None
        self.controller = controller
        self.ps = []
        self.order_count = 0

    def handler_wrap(self, infected_status):
        def handle_packet(packet):
            self.order_count = self.order_count+1
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                export_object(packet)
            output = f.getvalue()
            message = {
                "ID": self.sandbox_id,
                "infectedStatus": infected_status,
                "orderNo": self.order_count,
                "packet": output
                }
            self.client.emit('packet',
                json.dumps(message), namespace='/network')
        return handle_packet

    def monitoring_process(self, infected_status):
        self.client = socketio.Client()
        self.client.connect('http://localhost:5000', namespaces=['/network'])
        print("network monitor started")
        instance = None
        if infected_status == "healthy":
            instance = self.controller.healthyInstance
        else:
            instance = self.controller.infectedInstance
        print("Listening on docker0 for " + str(instance.ip))
        sniff(iface="docker0", filter="host "+str(instance.ip), prn=self.handler_wrap(infected_status))

    def run(self):
        self.mp = Process(target=self.runInParallel, args=(
            self.monitoring_process, self.monitoring_process, "healthy", "infected"))
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
