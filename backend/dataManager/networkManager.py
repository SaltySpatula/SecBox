from backend.dataManager.dataManager import DataManager
from scapy.all import *
from scapy.utils import hexstr


class NetworkManager(DataManager):
    def __init__(self, fe_client, db):
        super().__init__(fe_client, db)
        self.layer_counts = {}

    def setup_data_structures(self, sandbox_id, infected_status, data):
        self.order_nos[sandbox_id] = {"healthy": 1, "infected": 1}

        self.layer_counts[sandbox_id] = {
            "healthy": {"graph": {}}, "infected": {"graph": {}}}

    def handle_message(self, data):
        processed_data = self.process_data(data)
        sandbox_id = processed_data["ID"]
        infected_status = processed_data["infectedStatus"]

        if sandbox_id not in self.order_nos.keys():
            self.setup_data_structures(
                sandbox_id, infected_status, processed_data)
        if self.order_nos[sandbox_id][infected_status] <= processed_data["orderNo"]:

            # Call extract functions here
            self.extract_layer_counts(
                sandbox_id, infected_status, processed_data)
            # Call emit functions here
            self.socketio.emit("layer_counts_graph", self.layer_counts, namespace='/live', room=str(sandbox_id))
            #Add order no. to history
            self.order_nos[sandbox_id][infected_status] = processed_data["orderNo"]

        self.db_queue.put(processed_data)
        return True

    def process_data(self, data):
        dict = {}
        p = import_object(data["packet"][1:-1])
        try:
            for index in range(50):
                layer = p[index]
                dict[layer.name] = layer.fields
        except IndexError:
            pass
        dict["export"] = ""
        data["packet"] = dict
        return data

    def extract_layer_counts(self, sandbox_id, infected_status, data):
        for layer in data["packet"].keys():
            if layer not in ["export", "Raw"]:
                if layer not in self.layer_counts[sandbox_id][infected_status]["graph"].keys():
                    self.layer_counts[sandbox_id][infected_status]["graph"][layer] = 1
                else:
                    self.layer_counts[sandbox_id][infected_status]["graph"][layer] += 1

    def save_data(self, data):
        pass
