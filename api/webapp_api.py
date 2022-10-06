from flask import Flask, session
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask_cors import CORS
from dataManager import handler


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins=['http://localhost:8080', 'http://localhost:5000'])


@socketio.on("receive data")
def send_data():
    emit("receive data", handler.get_reports())


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    send_data()


@socketio.on("cli command", namespace='/live')
def post_command(json):
    print("received command", json)


@socketio.on("cli feedback", namespace='/live')
def get_command(cmd):
    emit("get cli feedback", cmd)


@socketio.on('disconnect', namespace='/live')
def disconnect():
    print('Client disconnected')


@socketio.on('connect', namespace='/live')
def connected():
    print("Client Connected ...")


@app.route("/greeting")
def greeting():
    return {"greeting": "Server is running"}


@app.route("/start", methods=['GET'])
def create():
    feedback = handler.start_process()
    start(feedback)

    return feedback


@app.route("/getReports")
def get_reports():
    reports = handler.get_reports()
    return {"reports": reports}


@app.route("/getAvailableMalwares")
def get_malware():
    malwares = handler.get_available_malwares()
    return {"malwares": malwares}


@ socketio.on('startSandbox')
def start(data):
    print("trying to start with", data)
    socketio.emit("startSandbox", data)


if __name__ == '__main__':
    socketio.run(app, port=5000)
    app.run()
