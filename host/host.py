import time
import socketio
import sandboxHandler
import json

socketio = socketio.Client()
id_counter = 0

@socketio.event
def connect():
    print('connection established')


@socketio.event
def disconnect():
    print('disconnected from server')


@socketio.on("startSandbox", namespace='/sandbox')
def start_sandbox(data):
    print(data)
    sandboxHandler.start_sandbox(json.loads(data), socketio)


@socketio.on("stopSandbox", namespace='/sandbox')
def stop_sandbox(data):
    sandboxHandler.stop_sandbox(json.loads(data))


@socketio.on("stopAll", namespace='/sandbox')
def stop_all_sandboxes():
    sandboxHandler.stop_all()


@socketio.on("paralellCommand", namespace='/cmd')
def parallel_command(data):
    sandboxHandler.parallel_command(json.loads(data))


@socketio.on("healthyCommand", namespace='/cmd')
def healthy_command(data):
    sandboxHandler.healthy_command(json.loads(data))


@socketio.on("infectedCommand", namespace='/cmd')
def healthy_command(data):
    sandboxHandler.infected_command(json.loads(data))


@socketio.on('*')
def catch_all(event, data):
    socketio.emit('Unknown Event')


namespaces = ['/sandbox', '/sysCall', '/network', '/performance', '/cmd']
if __name__ == '__main__':
    socketio.connect('http://localhost:5000', namespaces=['/sandbox', '/sysCall', '/network', '/performance', '/cmd'], wait_timeout=10)
    socketio.wait()
