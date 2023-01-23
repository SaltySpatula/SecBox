import sys
from datetime import datetime
import os

cwd = os.getcwd()
path = cwd[:-4]
sys.path.append(path)

from backend.dataManager.syscallManager import SysCallManager
from backend.dataManager.performanceManager import PerformanceManager
from backend.dataManager.networkManager import NetworkManager
from backend.dataManager.cmdOutManager import CmdOutManager
from flask import Flask, session, request, abort, send_file
from flask_socketio import SocketIO
from flask_socketio import send, emit, join_room, leave_room
from flask_cors import CORS
import json
from backend import handler, models
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, login_user, current_user, UserMixin
import logging
import json

from dotenv import load_dotenv

load_dotenv()
# Hosted DB:
# admin
# HmxrjkxTwd0etI6Y
# mongodb+srv://admin:HmxrjkxTwd0etI6Y@secboxmongodb.nhcx1ch.mongodb.net/?retryWrites=true&w=majority

app = Flask(__name__)
CORS(app)
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGODB_SETTINGS'] = {
    'db': os.getenv('DB'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT'))
}

db = MongoEngine()
db.init_app(app)

host_bitness = int(os.getenv('HOST_BITNESS'))

print("Filling Malware DB...")
handler.write_malware_to_DB()

socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=300)
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


# TODO: Remove
@socketio.on("receive data")
def send_data():
    emit("receive data", handler.get_reports())


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    send_data()


@socketio.on("cli command", namespace='/live')
def post_command(data):
    # TODO: save executed command to DB
    print("received command", data)
    if data["healthy_cmd"] != "":
        healthy = {
            'ID': data["room"],
            'CMD': data["healthy_cmd"]
        }
        socketio.emit("healthyCommand", json.dumps(healthy), namespace='/cmd')
    if data["infected_cmd"] != "":
        infected = {
            'ID': data["room"],
            'CMD': data["infected_cmd"]
        }
        socketio.emit("infectedCommand", json.dumps(infected), namespace='/cmd')


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
    try:
        process = models.Process.objects(ID__exact=data["room"])[0]
        malware = process["malware"].to_json()

        socketio.emit("Malware of Process", json.dumps(malware), namespace="/live", room=data["room"])
    except IndexError:
        print("No corresponding DB entry found for Process:", data["room"])


@socketio.on('join analysis room', namespace="/analysis")
def join_analysis(data):
    join_room(data["room"])
    try:
        process = models.Process.objects(ID__exact=data["room"])[0]
        malware = process["malware"].to_json()

        socketio.emit("Malware of Process", json.dumps(malware), namespace="/analysis", room=data["room"])
    except IndexError:
        print("No corresponding DB entry found for Process:", data["room"])


@socketio.on('leave room', namespace='/live')
def leave(data):
    room = data["room"]
    leave_room(room)
    print("Client left room", room)


@socketio.on("stop request", namespace="/live")
def stopAnalysis(data):
    print("Stopping sandbox", data["ID"])
    stop(data)


@socketio.on("get CPU Usage", namespace="/analysis")
def getCPUMemory(data):
    sandbox_id = data["ID"]
    objects = json.loads(models.PerformanceModel.objects(ID__exact=sandbox_id).to_json())
    # assert len(objects) == 1, "Multiple (or no) objects have been found in the DB"
    try:
        response = json.loads(objects[0]["cpu_percentages"])
        socketio.emit("CPU Usage", json.dumps(response), namespace="/analysis", room=objects[0]["ID"])
    except IndexError:
        print("No corresponding DB entry found for CPU Usage - ID:", sandbox_id)


@socketio.on("get Network Layers", namespace="/analysis")
def getNetworkLayers(data):
    sandbox_id = data["ID"]
    try:
        objects = json.loads(models.NetworkModel.objects(ID__exact=sandbox_id).to_json())
        response = json.loads(objects[0]["layer_counts"])
        socketio.emit("Network Layers", json.dumps(response), namespace="/analysis", room=objects[0]["ID"])
    except IndexError:
        print("No corresponding DB entry found for Network Layer - ID:", sandbox_id)

"""
@socketio.on("get Malware of Process")
def get_malware_of_process(data):
    sandbox_id = data["ID"]
    try:
        process = models.Process.objects(ID__exact=data["ID"])[0]
        malware = json.dumps(process["malware"].to_json())

        socketio.emit("Malware of Process", json.dumps(malware), namespace="/analysis", room=data["ID"])
    except IndexError:
        print("No corresponding DB entry found for Process:", sandbox_id)
"""

@socketio.on("get IP Addresses", namespace="/analysis")
def getIPAddresses(data):
    sandbox_id = data["ID"]
    try:
        objects = json.loads(models.NetworkModel.objects(ID__exact=sandbox_id).to_json())
        response = json.loads(objects[0]["IP_frequency"])
        print(response)
        socketio.emit("IP Addresses", json.dumps(response), namespace="/analysis", room=objects[0]["ID"])
    except IndexError:
        print("No corresponding DB entry found for IP frequency - ID: ", sandbox_id)


@socketio.on("get RAM", namespace="/analysis")
def getRam(data):
    sandbox_id = data["ID"]
    try:
        objects = json.loads(models.PerformanceModel.objects(ID__exact=sandbox_id).to_json())
        response = json.loads(objects[0]["ram_usage"])
        socketio.emit("RAM", json.dumps(response), namespace="/analysis", room=objects[0]["ID"])
    except IndexError:
        print("No corresponding DB entry found for IP frequency - ID: ", sandbox_id)


@socketio.on("get Read Write", namespace="/analysis")
def getRWCount(data):
    sandbox_id = data["ID"]
    try:
        objects = json.loads(models.SystemCallModel.objects(ID__exact=sandbox_id).to_json())
        response = json.loads(objects[0]["reads_vs_writes"])
        print(response)
        socketio.emit("Read Write Counts", json.dumps(response), namespace="/analysis", room=objects[0]["ID"])
    except IndexError:
        print("No corresponding DB entry found for Read Write Counts - ID: ", sandbox_id)


@socketio.on("get Directory Graph", namespace="/analysis")
def getDirs(data):
    sandbox_id = data["ID"]
    try:
        objects = json.loads(models.SystemCallModel.objects(ID__exact=sandbox_id).to_json())
        response = json.loads(objects[0]["directory_frequency"])
        print(response)
        socketio.emit("Directory Graph", json.dumps(response), namespace="/analysis", room=objects[0]["ID"])
    except IndexError:
        print("No corresponding DB entry found for Directory Graph - ID: ", sandbox_id)


@app.route('/report/download_pcap/<identification>/<infection>', methods=['GET'])
def fetch_pcap(identification, infection):
    p = infection + "/" + identification + ".pcap"
    response = send_file(p)
    return response


@app.route('/report/download_syscalls/<identification>/<infection>', methods=['GET'])
def fetch_syscalls(identification, infection):
    p = infection + "/" + identification + ".csv"
    response = send_file(p)
    return response


@socketio.on("create report", namespace="/analysis")
def create_report(data):
    print("creating report for", data["ID"])
    date = datetime.now()

    report = models.Report(ID=data["ID"], selected_graphs=data["selected_graphs"], title="Title",
                           date=date.strftime("%m/%d/%Y, %H:%M"))

    obj = models.Process.objects(ID__exact=data["ID"])[0]
    report.malware = json.dumps(obj["malware"].to_json())
    report.save()


@socketio.on("get report", namespace="/report")
def get_report(data):
    sandbox_id = data["ID"]
    join_room(data["ID"])
    try:
        objects = json.loads(models.Report.objects(ID__exact=sandbox_id).to_json())
        response = objects[0]
        response["malware"] = json.loads(response["malware"])
        socketio.emit("send report", json.dumps(response), namespace="/report", room=objects[0]["ID"])
    except IndexError:
        print("No report found")


@socketio.on("update report", namespace="/report")
def update_report(data):
    sandbox_id = data["ID"]
    try:
        print("updating ", sandbox_id, data)
        models.Report.objects(ID__exact=sandbox_id).update(selected_graphs=data["selected_graphs"], title=data["title"])
    except IndexError:
        print("Could not perform update: ID not found")


@app.route("/greeting")
def greeting():
    return {"greeting": "Server is running"}


@socketio.on("start request", namespace="/start")
def create(data):
    start_data = handler.start_process(sha=data["SHA256"], selected_os=data["OS"])
    feedback = start(start_data)
    emit("start feedback", json.dumps(feedback), namespace="/start")

    malware = models.Malware.objects(hash=data["SHA256"])[0]
    idx = feedback["ID"]
    p = models.Process(SHA256=data["SHA256"], ID=idx, selected_os=data["OS"])
    p.malware = malware
    p.save()


@app.route('/syscall', methods=['GET', 'POST'])
def syscall_upload():
    system_call_manager.handle_message(json.loads(request.json))
    return "That seemed to work!"


@socketio.on('sandboxReady', namespace='/sandbox')
def handle_ready(json):
    print(json)
    print("sandbox ready!")


@socketio.on('stats', namespace='/performance')
def handle_stats(data):
    performance_manager.handle_message(json.loads(data))


@socketio.on('cmdOut', namespace='/cmd')
def handle_cmdline(data):
    command_output_manager.handle_message(json.loads(data))


@socketio.on('packet', namespace='/network')
def handle_networkpacket(data):
    print("Packet received")
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
    malwares = json.dumps(handler.get_available_malware(host_bitness))

    return {"malwares": malwares, "oss": oss}


@socketio.on("startSandbox", namespace="/dummy")
def start(data):
    socketio.emit("startSandbox", json.dumps(data), namespace='/sandbox')
    return data


@socketio.on("stopSandbox", namespace="/sandbox")
def stop(data):
    print("Stop function called")
    try:
        performance_manager.save_data(data)
        print("Saved performance data", data)
        network_manager.save_data(data)
        socketio.emit("stopSandbox", json.dumps(data), namespace="/sandbox")
    except KeyError:
        print("Sandbox has already been stopped and the data saved")
    return data


if __name__ == '__main__':
    socketio.run(app, port=5000)
    app.run()
