import sys
sys.path.append("/home/adrian/Desktop/HS2022/MasterPrject/SecBox")

from backend.dataManager.syscallManager import SysCallManager
from backend.dataManager.performanceManager import PerformanceManager
from backend.dataManager.networkManager import NetworkManager
from backend.dataManager.cmdOutManager import CmdOutManager
from flask import Flask, session, request, abort
from flask_socketio import SocketIO
from flask_socketio import send, emit, join_room, leave_room
from flask_cors import CORS
import json
from backend import handler, models
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, login_user, current_user, UserMixin
import logging
import json

app = Flask(__name__)
CORS(app)
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app.config['SECRET_KEY'] = 'secret!'
app.config['MONGODB_SETTINGS'] = {
    'db': 'SecBoxDB',
    'host': 'mongodb://localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

socketio = SocketIO(app, cors_allowed_origins=[
                    'http://localhost:8080', 'http://localhost:5000', 'http://localhost:5001'])
login = LoginManager(app)

system_call_manager = SysCallManager(socketio, db)
network_manager = NetworkManager(socketio, db)
performance_manager = PerformanceManager(socketio, db)
command_output_manager = CmdOutManager(socketio, db)

allowed_users = {
    'foo': 'bar',
    'python': 'is-great!',
}


@login.user_loader
def user_loader(id):
    return User(id)


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    if username not in allowed_users or allowed_users[username] != password:
        abort(401)
    login_user(User(username))

    return ''


@socketio.on("receive data")
def send_data():
    emit("receive data", handler.get_reports())


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    send_data()


@socketio.on("cli command", namespace='/live')
def post_command(data):
    #TODO: save executed command to DB
    print("received command", data)
    if data["healthy_cmd"] != "" or data["healthy_cmd"] is not None:
        healthy = {
        'ID': int(data["room"]),
        'CMD': data["healthy_cmd"]
        }
        socketio.emit("healthyCommand", json.dumps(healthy),namespace='/cmd')
    if data["infected_cmd"] != "" or data["infected_cmd"] is not None:
        infected = {
        'ID': int(data["room"]),
        'CMD': data["infected_cmd"]
        }
        socketio.emit("infectedCommand", json.dumps(infected),namespace='/cmd')


@socketio.on('disconnect', namespace='/live')
def disconnect():
    print('Client disconnected')


@socketio.on('connect', namespace='/live')
def connected():
    """
    # authentication
    print(current_user.is_anonymous)
    if current_user.is_anonymous:
        return False
    emit('welcome', {
        'username': current_user.id
    })
    """
    print("Client Connected...", )


@socketio.on('join room', namespace='/live')
def join(data):
    print("join room:", data)
    room = data["room"]
    join_room(room)
    print("Client Connected to room", room, print(type(room)))
    emit("Successfully connected to live analysis room " + room, to=room)


@socketio.on('leave room', namespace='/live')
def leave(data):
    room = data["room"]
    leave_room(room)
    print("Client left room", room)


@app.route("/greeting")
def greeting():
    return {"greeting": "Server is running"}


@socketio.on("start request", namespace="/start")
def create(data):
    # malware = models.Malware.objects(hash=data["SHA256"])[0]
    # p = models.Process(SHA256=data["SHA256"], selected_os=data["OS"])
    # p.malware = malware
    # p.save()
    start_data = handler.start_process(sha=data["SHA256"], selected_os=data["OS"])
    feedback = start(start_data)
    emit("start feedback", json.dumps(feedback), namespace="/start")

@socketio.on("stop request", namespace="/live")
def stopAnalysis(data):
    print("Stopping sandbox", data["ID"])
    stop(data)


@ socketio.on('sysCall', namespace='/sysCall')
def handle_sys_call(data):
    system_call_manager.handle_message(json.loads(data))


@ socketio.on('sandboxReady', namespace='/sandbox')
def handle_ready(json):
    print(json)
    print("sandbox ready!")


@ socketio.on('stats', namespace='/performance')
def handle_stats(data):
    performance_manager.handle_message(json.loads(data))


@ socketio.on('cmdOut', namespace='/cmd')
def handle_cmdline(data):
    command_output_manager.handle_message(json.loads(data))


@ socketio.on('packet', namespace='/network')
def handle_networkpacket(data):
    network_manager.handle_message(json.loads(data))

"""
@app.route("/start", methods=['GET'])
def create():
    feedback = handler.start_process()
    start(feedback)
    return feedback
"""


@app.route("/getReports")
def get_reports():
    reports = handler.get_reports()
    return {"reports": reports}


@app.route("/getStartData")
def get_start_data():
    oss = json.dumps(handler.get_available_images())
    malwares = json.dumps(handler.get_available_malware())


    return {"malwares": malwares, "oss": oss}


@socketio.on("startSandbox", namespace="/dummy")
def start(data):
    socketio.emit("startSandbox", json.dumps(data), namespace='/sandbox')
    return data
@socketio.on("stopSandbox", namespace="/sandbox")
def stop(data):
    print("Stop function called")
    socketio.emit("stopSandbox", json.dumps(data), namespace="/sandbox")
    return data

if __name__ == '__main__':
    socketio.run(app, port=5000)
    app.run()
