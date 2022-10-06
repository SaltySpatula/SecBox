from flask import Flask, session
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask_cors import CORS
from dataManager import handler

# generate unique id for container set here
available_namespaces = ['/sandbox', '/sysCall',
                        '/network', '/performance', '/cmd']
app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

@ socketio.on('disconnect')
def disconnect():
    print('Client disconnected')


@ socketio.on('connect')
def connected():
    print("Client Connected ...")


@ socketio.on('sysCall', namespace='/sysCall')
def handle_sys_call(json):
    pass


@ socketio.on('sandboxReady', namespace='/sandbox')
def handle_ready(json):
    pass


@ socketio.on('cmdOut', namespace='/cmd')
def handle_cmdline(json):
    pass

@ socketio.on('startSandbox')
def start(data):
    print("trying to start with", data)
    socketio.emit("startSandbox", data)
