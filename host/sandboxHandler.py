from time import sleep
from monitors.systemCallMonitor import systemCallMonitor
from controller import Controller
from multiprocessing import Process

sandboxes = {}

def start_sandbox(json, socketio):
    expected_json = {
        'ID': 123,
        'SHA256': '094fd325049b8a9cf6d3e5ef2a6d4cc6a567d7d49c35f8bb8dd9e3c6acf3d78d',
        'OS': 'ubuntu:latest',
    }
    sandbox_id = json['ID']
    mw_hash = json['SHA256']
    os = json['OS']
    client = socketio
    sandbox = Sandbox(client, mw_hash, os, sandbox_id)
    sandboxes[sandbox_id] = sandbox


def find_by_id(sandbox_id):
    try:
        return sandboxes[sandbox_id]
    except:
        print('Invalid Sanbox ID: ' + str(sandbox_id))


def stop_sandbox(json):
    sandbox = find_by_id(json['ID'])
    sandbox.stopped = True
    sandbox.process.terminate()


def stop_all():
    for sandbox in sandboxes.values():
        sandbox.stopped = True
    sandbox.process.terminate()


def parallel_command(json):
    expected_json = {
        'ID': 123,
        'CMD': 'sudo apt-get update'
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
    def __init__(self, client, mw_hash, os, sandbox_id) -> None:
        self.sandbox_id = sandbox_id
        self.controller = None
        self.syscallMonitor = None

        self.client = client
        self.mw_hash = mw_hash
        self.os = os

        self.stopped = False
        self.process = Process(target=self.run)
        self.process.start()

    def run(self):
        with systemCallMonitor(self.client, self.sandbox_id) as syscallMonitor:
            self.syscallMonitor = syscallMonitor
            with Controller(self.client, self.mw_hash, self.os, self.sandbox_id) as controller:
                self.controller = controller
                while not self.stopped:
                    sleep(1)
