import socketio
import json
import time

socketio = socketio.Client()


@socketio.on("cpu_percentages_graph", namespace="/live")
def cpu_percentages(data):
    #print(data)
    pass


@socketio.on("pid_graph", namespace="/live")
def pid_graph(data):
    #print(data)
    pass

@socketio.on("packet_graph", namespace="/live")
def packet_graph(data):
    print(data)
    pass


if __name__ == '__main__':
    socketio.connect('http://localhost:5000',
                     namespaces=['/dummy', '/cmd', '/live'])
    print("Dummy FE running...")
    time.sleep(10)
    data = json.dumps(
        {"ID": 123, "SHA256": "094fd325049b8a9cf6d3e5ef2a6d4cc6a567d7d49c35f8bb8dd9e3c6acf3d78d", "OS": "ubuntu:latest"})
    print("Sending start Sandbox Request")
    data = "Start Sandbox Request received"
    socketio.emit("startSandbox", data, namespace='/dummy')
    print("Emitted Event")
    time.sleep(10)
    expected_json = {
        'ID': 123,
        'CMD': 'sudo apt-get update'
    }
    socketio.emit("paralellCommand", json.dumps(
        expected_json), namespace='/cmd')
    print("Emitted Command")
    socketio.wait()
