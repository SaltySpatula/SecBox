import os
from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Process
import json



class performanceMonitor:
    def __init__(self, client, sandbox_id, controller) -> None:
        self.sandbox_id = sandbox_id
        self.client = client
        self.controller = controller

    def run(self):
        healthy_container= self.controller.healthyInstance.container
        infected_container = self.controller.infectedInstance.container
        self.mp = Process(target=self.runInParallel, args=(
            self.monitoring_process, self.monitoring_process, ("healthy", healthy_container), ("infected", infected_container)))
        self.runInParallel(self.monitoring_process, self.monitoring_process,
                           "healthy", "infected")

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for p in self.ps:
            p.join()
        self.mp.join()

    def monitoring_process(self, infected_status, container):
        order_count = 0
        for stats in container.stats(decode=True):
            ++order_count
            message = {
                "ID": self.sandbox_id,
                "infectedStatus": infected_status,
                "orderNo": order_count,
                "sysCall": stats
            }
            order_count = 0
            self.client.emit('stats', json.dumps(message), namespace='/performance')

    def runInParallel(self, fn1, fn2, args1, args2):
        fns = [fn1, fn2]
        args = [args1, args2]
        procs = []
        for index in range(len(fns)):
            p = Process(target=fns[index], args=args[index])
            p.start()
            procs.append(p)
        self.ps = procs
