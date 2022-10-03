from flask import Flask, session
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask_cors import CORS
from dataManager import handler


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins='http://localhost:8080')

@socketio.on("receive data")
def send_data():
    emit("receive data", handler.get_reports())

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    send_data()

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('connect')
def connected():
    print("Client Connected ...")


@app.route("/greeting")
def greeting():
    return {"greeting": "Server is running"}


@app.route("/start")
def create():
    return {"processId": handler.start_process()}


@app.route("/getReports")
def get_reports():
    reports = handler.get_reports()
    return {"reports": reports}


if __name__ == '__main__':
    socketio.run(app)
    app.run()
