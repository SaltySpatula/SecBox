import queue 

class DataManager:
    def __init__(self, socketio, db):
        self.sent_packages = []
        self.db = db
        self.socketio = socketio
        self.windowsize = 1000
        self.db_queue = queue.Queue(maxsize=1000)
        self.order_nos = {}

    def handle_message(msg):
        pass

    def process_data(self, data):
        pass

    def batch_process():
        pass