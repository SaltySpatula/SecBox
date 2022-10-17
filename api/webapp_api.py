from flask import Flask, session, request, abort
from flask_socketio import SocketIO
from flask_socketio import send, emit, join_room, leave_room
from flask_cors import CORS
from backend import handler, models
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, login_user, current_user, UserMixin

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret!'

app.config['MONGODB_SETTINGS'] = {
    'db': 'SecBoxDB',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

socketio = SocketIO(app, cors_allowed_origins=['http://localhost:8080', 'http://localhost:5000'])
login = LoginManager(app)

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


@app.route('/login', methods = ['POST'])
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
def post_command(json):
    print("received command", json)
    get_command(json)


@socketio.on("cli feedback", namespace='/live')
def get_command(cmd):
    print("Echo: ", cmd)
    room = cmd["room"]
    cmd["clean_cmd"] = "echo " + cmd["clean_cmd"]
    cmd["infected_cmd"] = "echo " + cmd["infected_cmd"]
    emit("cli feedback", cmd, to=room)


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
    room = data["room"]
    join_room(room)
    print("Client Connected to room", room)
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
    malware = models.Malware.objects(hash=data["SHA256"])[0]
    p = models.Process(SHA256=data["SHA256"], selected_os=data["OS"])
    p.malware = malware
    p.save()
    feedback = handler.start_process(sha=data["SHA256"], selected_os=data["OS"])
    start(feedback)
    start_feedback(feedback)


@socketio.on("start feedback", namespace="/start")
def start_feedback(feedback):
    emit("start feedback", feedback, namespace="/start")


@app.route("/getReports")
def get_reports():
    reports = handler.get_reports()
    return {"reports": reports}


@app.route("/getStartData")
def get_malware():
    # malwares = handler.get_available_malwares()
    malwares = models.Malware.objects.to_json()
    oss = handler.get_available_os()

    return {"malwares": malwares, "oss": oss}


@socketio.on('startSandbox')
def start(data):
    print("trying to start with", data)
    socketio.emit("startSandbox", data)


if __name__ == '__main__':
    socketio.run(app, port=5000)
    app.run()
