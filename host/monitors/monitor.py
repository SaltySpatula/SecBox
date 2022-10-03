from multiprocessing import Process

class Monitor:
    def __init__(self, command) -> None:
        self.command = command
        
    def stream_over_websocket():
        pass

    def run():
        pass

    def runInParallel(self, fn1, fn2, arg1, arg2):
        fns = [fn1, fn2]
        args =  [arg1, arg2]
        proc = []
        for index in range(len(fns)):
            p = Process(target=fns[index], args=args[index])
            p.start()
            proc.append(p)
        for p in proc:
            p.join()