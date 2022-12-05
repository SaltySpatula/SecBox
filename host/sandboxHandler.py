import socketio
from multiprocessing import Process
from controller import Controller
from monitors import performanceMonitor
from monitors import networkMonitor
from monitors import systemCallMonitor
from time import sleep

sandboxes = {}


def start_sandbox(json):
    sandbox_id = json['ID']
    mw_hash = json['SHA256']
    os = json['OS']
    sandbox = Sandbox(mw_hash, os, sandbox_id)
    sandboxes[sandbox_id] = sandbox


def find_by_id(sandbox_id):
    try:
        return sandboxes[sandbox_id]
    except:
        print('Invalid Sanbox ID: ' + str(sandbox_id))


def stop_sandbox(json):
    print(json)
    sandbox = find_by_id(json['ID'])
    print(sandbox)
    sandbox.stop()


def stop_all():
    for sandbox in sandboxes.values():
        sandbox.stopped = True
    sandbox.stop()


def parallel_command(json):
    expected_json = {
        'ID': 123,
        'CMD': 'apt-get update'
    }
    sandbox = find_by_id(json['ID'])
    command = json['CMD']
    sandbox.controller.execute_command(command)


def infected_command(json):
    expected_json = {
        'ID': 123,
        'CMD': 'sudo apt-get update'
    }
    sandbox = find_by_id(json['ID'])
    command = json['CMD']
    sandbox.controller.infectedInstance.execute_command(command)


def healthy_command(json):
    expected_json = {
        'ID': 123,
        'CMD': 'sudo apt-get update'
    }
    sandbox = find_by_id(json['ID'])
    command = json['CMD']
    sandbox.controller.healthyInstance.execute_command(command)


class Sandbox:
    def __init__(self, mw_hash, os, sandbox_id) -> None:
        self.client = socketio.Client()
        self.client.connect('http://localhost:5000', namespaces=['/sandbox'])

        self.sandbox_id = sandbox_id

        self.mw_hash = mw_hash
        self.os = os

        self.syscallMonitor = systemCallMonitor.systemCallMonitor(
            self.sandbox_id)
        self.syscallMonitor.start()
        sleep(6)
        self.controller = Controller(self.mw_hash, self.os, self.sandbox_id)

        self.perfMonitor = performanceMonitor.performanceMonitor(
            self.sandbox_id, self.controller)
        self.netMonitor = networkMonitor.networkMonitor(
            self.sandbox_id, self.controller)

        self.stopped = False
        self.process = Process(target=self.run)
        self.process.start()

    def run(self):
        self.perfMonitor.run()
        self.netMonitor.run()
        self.client.emit('sandboxReady', "ready!", namespace='/sandbox')

    def stop(self):
        self.syscallMonitor.stop()
        self.perfMonitor.stop()
        self.netMonitor.stop()
        self.controller.stop_instances()
        self.process.kill()
        print("process killed")
        self.stopped = True
        print("Sandbox stopped, processes joined")
