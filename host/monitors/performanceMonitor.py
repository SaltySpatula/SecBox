from subprocess import Popen, PIPE, STDOUT
from multiprocessing import Process
import json
import socketio



class performanceMonitor:
    def __init__(self, sandbox_id, controller) -> None:
        self.sandbox_id = sandbox_id
        self.client = socketio.Client()
        self.client.connect('http://localhost:5000', namespaces = ['/performance'])
        self.controller = controller
        self.ps = []

    def monitoring_process(self, infected_status):
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
