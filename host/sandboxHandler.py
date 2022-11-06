from http import client
import sys
import time
# sys.path.append("/home/adrian/Desktop/HS2022/MasterPrject/SecBox/host/monitors")
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
    # ToDo: handle integer casting
    print(json)
    sandbox = find_by_id(int(json['ID']))
    sandbox.stopped = True
    sandbox.process.terminate()
    sandbox.controller.stop_instances()


def stop_all():
    for sandbox in sandboxes.values():
        sandbox.stopped = True
    sandbox.process.terminate()


def parallel_command(json):
    expected_json = {
        'ID': 123,
        'CMD': 'apt-get update'
    }
    sandbox = find_by_id(json['ID'])
    command = json['CMD']
    print("sandbox"+str(sandbox.sandbox_id))
    print(sandbox.performanceMonitor)
    print(sandboxes)
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
        self.sandbox_id = sandbox_id

        self.mw_hash = mw_hash
        self.os = os

        self.syscallMonitor = systemCallMonitor.systemCallMonitor(self.sandbox_id)
        self.controller = Controller(self.mw_hash, self.os, self.sandbox_id)
        self.performanceMonitor = performanceMonitor.performanceMonitor(self.sandbox_id, self.controller)
        self.networkMonitor = networkMonitor.networkMonitor(self.sandbox_id, self.controller)


        self.stopped = False
        self.process = Process(target=self.run)
        self.process.start()

    def run(self):
        with self.syscallMonitor as syscallMonitor:
            with self.controller as controller:
                with self.performanceMonitor as performanceMonitor:
                    with self.networkMonitor as networkMonitor:
                        self.client.emit('sandboxReady',"ready!", namespace='/sandbox')
                        while not self.stopped:
                            sleep(1)

