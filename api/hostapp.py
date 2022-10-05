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

socketio = SocketIO(app, cors_allowed_origins='http://localhost:5000',
                    namespaces=available_namespaces)

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
