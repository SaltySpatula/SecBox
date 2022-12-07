from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Process
import threading
import json
from scapy.all import *
import socketio
import contextlib
import io
import time
from time import sleep
import sys

class networkMonitor:
    def __init__(self, sandbox_id, controller) -> None:
        self.sandbox_id = sandbox_id
        self.controller = controller
        self.ps = []
        self.order_count = 0
        self.infected_buf = []
        self.healthy_buf = []
        self.last_emit = {"healthy": time.time(), "infected": time.time()}

    def handler_wrap(self, infected_status, client, lock):
        def handle_packet(packet):
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                export_object(packet)
            output = f.getvalue()
            if infected_status=="healthy":
                self.healthy_buf.append(output)
                buffer = self.healthy_buf
            else:
                self.infected_buf.append(output)
                buffer = self.infected_buf
            if self.last_emit[infected_status] + 1 <= time.time():
                message = {
                    "ID": self.sandbox_id,
                    "infectedStatus": infected_status,
                    "orderNo": self.order_count,
                    "packets": buffer
                }
                with lock:
                    client.emit('packet',
                                    json.dumps(message), namespace='/network')
                    self.last_emit[infected_status] = time.time()
                self.order_count = self.order_count+1
                if infected_status=="healthy":
                    self.healthy_buf = []
                else:
                    self.infected_buf = []
            elif sys.getsizeof(buffer)>=1000:
                message = {
                    "ID": self.sandbox_id,
                    "infectedStatus": infected_status,
                    "orderNo": self.order_count,
                    "packets": buffer
                }
                with lock:
                    client.emit('packet',
                                json.dumps(message), namespace='/network')
                    self.last_emit[infected_status] = time.time()
                self.order_count = self.order_count+1
                client.sleep(0)
                sleep(0.1)
                if infected_status=="healthy":
                    self.healthy_buf = []
                else:
                    self.infected_buf = []
        return handle_packet

    def monitoring_process(self, infected_status):
        client = socketio.Client()
        client.connect('http://localhost:5000', namespaces='/network')
        lock = threading.Lock()
        sleep(2)
        print("network monitor started")
        instance = None
        if infected_status == "healthy":
            instance = self.controller.healthyInstance
        else:
            instance = self.controller.infectedInstance
        print("sniffing for " + "host "+str(instance.ip))
        sniff(iface="docker0", filter="host "+str(instance.ip),
              prn=self.handler_wrap(infected_status, client, lock))

    def run(self):
        p = Process(target=self.runInParallel, args=(
            self.monitoring_process, self.monitoring_process, "healthy", "infected"))
        p.start()
        self.ps.append(p)

    def stop(self):
        for p in self.ps:
            p.kill()

    def runInParallel(self, fn1, fn2, args1, args2):
        fns = [fn1, fn2]
        args = [(args1,), (args2,)]
        for index in range(len(fns)):
            p = Process(target=fns[index], args=args[index])
            p.start()
            self.ps.append(p)
