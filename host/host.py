import time
import socketio
import sandboxHandler
import json

socketio = socketio.Client()

@socketio.event
def connect():
    print('connection established')


@socketio.event
def disconnect():
    print('disconnected from server')


@socketio.on("startSandbox", namespace='/sandbox')
def start_sandbox(data):
    sandboxHandler.start_sandbox(json.loads(data))


@socketio.on("stopSandbox", namespace='/sandbox')
def stop_sandbox(data):
    print("stop request received")
    sandboxHandler.stop_sandbox(json.loads(data))


@socketio.on("stopAll", namespace='/sandbox')
def stop_all_sandboxes():
    sandboxHandler.stop_all()


@socketio.on("paralellCommand", namespace='/cmd')
def parallel_command(data):
    print("received Command")
    sandboxHandler.parallel_command(json.loads(data))


@socketio.on("healthyCommand", namespace='/cmd')
def healthy_command(data):
    print("healthy command", data)
    sandboxHandler.healthy_command(json.loads(data))


@socketio.on("infectedCommand", namespace='/cmd')
def infected_command(data):
    print("infected command", data)
    sandboxHandler.infected_command(json.loads(data))


@socketio.on('*')
def catch_all(event, data):
    socketio.emit('Unknown Event')


namespaces = ['/sandbox', '/sysCall',
              '/network', '/performance', '/cmd', '/dummy']
if __name__ == '__main__':
    socketio.connect('http://localhost:5000', namespaces=namespaces)
    print("Host running...")
    socketio.wait()
