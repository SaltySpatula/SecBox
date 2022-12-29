from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Process
import json
import socketio
import os

from dotenv import load_dotenv

load_dotenv()


class performanceMonitor:
    def __init__(self, sandbox_id, controller) -> None:
        self.sandbox_id = sandbox_id
        self.client = None
        self.controller = controller
        self.ps = []
        self.mp = None

    def monitoring_process(self, infected_status):
        self.client = socketio.Client()
        self.client.connect(os.getenv('BE_IP_PORT'), namespaces=['/performance'])
        print("performance monitor started")
        order_count = 0
        container = None
        if infected_status=="healthy":
            container = self.controller.healthyInstance.container
        else:
            container = self.controller.infectedInstance.container
        for stats in container.stats(decode=True):
            order_count = order_count+1
            message = {
                "ID": self.sandbox_id,
                "infectedStatus": infected_status,
                "orderNo": order_count,
                "stats": stats
            }
            self.client.emit('stats', json.dumps(message), namespace='/performance')
            self.client.sleep(0)

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
