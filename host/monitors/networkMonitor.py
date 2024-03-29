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
import os

from dotenv import load_dotenv

load_dotenv()

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
                if self.last_emit[infected_status] + 1 <= time.time():
                    message = {
                        "ID": self.sandbox_id,
                        "infectedStatus": infected_status,
                        "orderNo": self.order_count,
                        "packets": self.healthy_buf
                    }
                    try:
                        with lock:
                            client.emit('packet',
                                            json.dumps(message), namespace='/network')
                            self.last_emit[infected_status] = time.time()
                            self.order_count = self.order_count+1
                        client.sleep(0)
                        self.healthy_buf = []
                    except socketio.exceptions.BadNamespaceError:
                        client.connect(os.getenv('BE_IP_PORT'), namespaces='/network')
                        client.sleep(0)
                elif sys.getsizeof(self.healthy_buf)>=1000:
                    message = {
                        "ID": self.sandbox_id,
                        "infectedStatus": infected_status,
                        "orderNo": self.order_count,
                        "packets": self.healthy_buf
                    }
                    try:
                        with lock:
                            client.emit('packet',
                                        json.dumps(message), namespace='/network')
                            self.last_emit[infected_status] = time.time()
                            self.order_count = self.order_count+1
                        self.healthy_buf = []
                        client.sleep(0)
                        sleep(0.2)
                    except socketio.exceptions.BadNamespaceError:
                        client.connect(os.getenv('BE_IP_PORT'), namespaces='/network')
                        client.sleep(0)
            else:
                self.infected_buf.append(output)
                if self.last_emit[infected_status] + 1 <= time.time():
                    message = {
                        "ID": self.sandbox_id,
                        "infectedStatus": infected_status,
                        "orderNo": self.order_count,
                        "packets": self.infected_buf
                    }
                    try:
                        with lock:
                            client.emit('packet',
                                        json.dumps(message), namespace='/network')
                            self.last_emit[infected_status] = time.time()
                            self.order_count = self.order_count+1
                        self.infected_buf = []
                        client.sleep(0)
                    except socketio.exceptions.BadNamespaceError:
                        client.connect(os.getenv('BE_IP_PORT'), namespaces='/network')
                        client.sleep(0)
                elif sys.getsizeof(self.infected_buf)>=1000:
                    message = {
                        "ID": self.sandbox_id,
                        "infectedStatus": infected_status,
                        "orderNo": self.order_count,
                        "packets": self.infected_buf
                    }
                    try:
                        with lock:
                            client.emit('packet',
                                        json.dumps(message), namespace='/network')
                            self.last_emit[infected_status] = time.time()
                            self.order_count = self.order_count+1
                        self.infected_buf = []
                        client.sleep(0)
                        sleep(0.2)
                    except socketio.exceptions.BadNamespaceError:
                        print("Caught Exception" + str(infected_status))
                        client.connect(os.getenv('BE_IP_PORT'), namespaces='/network')
                        client.sleep(0)
        return handle_packet

    def monitoring_process(self, infected_status, lock):
        client = socketio.Client()
        client.connect(os.getenv('BE_IP_PORT'), namespaces='/network')
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
        lock = threading.Lock()

        p = Process(target=self.runInParallel, args=(
            self.monitoring_process, self.monitoring_process, ("healthy", lock), ("infected", lock)))
        p.start()
        self.ps.append(p)

    def stop(self):
        for p in self.ps:
            p.terminate()
        for p in self.ps:
            print("Waiting for terminated network monitor process to terminate")
            p.join()
            print("Closing terminated process")
            p.close()

    def runInParallel(self, fn1, fn2, args1, args2):
        print("Running in paralell")
        fns = [fn1, fn2]
        args = [(args1), (args2)]
        for index in range(len(fns)):
            p = Process(target=fns[index], args=args[index])
            p.start()
            self.ps.append(p)
