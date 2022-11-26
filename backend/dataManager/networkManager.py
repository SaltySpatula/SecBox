from backend.dataManager.dataManager import DataManager
from scapy.all import *
from scapy.utils import hexstr
import json
from backend import models
import contextlib, io


class NetworkManager(DataManager):
    def __init__(self, fe_client, db):
        super().__init__(fe_client, db)
        self.layer_counts = {}
        self.raw_packet_data = {}
        self.ip_adress_frequency = {}

    def setup_data_structures(self, sandbox_id, infected_status, data):
        self.order_nos[sandbox_id] = {"healthy": 1, "infected": 1}

        self.layer_counts[sandbox_id] = {
            "healthy": {"graph": {}}, "infected": {"graph": {}}}

        self.ip_adress_frequency[sandbox_id] = {}
        
        self.raw_packet_data[sandbox_id] = {"healthy": [], "infected": []}

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
            self.extract_IP_adresses(
                sandbox_id, infected_status, processed_data
            )
            # Call emit functions here
            self.socketio.emit("layer_counts_graph", self.layer_counts, namespace='/live', room=str(sandbox_id))
            # Add order no. to history
            self.order_nos[sandbox_id][infected_status] = processed_data["orderNo"]
            
            self.raw_packet_data[sandbox_id][infected_status].append(processed_data["packet"])
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
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            export_object(p)
        output = f.getvalue()
        dict["export"] = output
        data["packet"] = dict
        return data

    def extract_layer_counts(self, sandbox_id, infected_status, data):
        for layer in data["packet"].keys():
            if layer not in ["export", "Raw"]:
                if layer not in self.layer_counts[sandbox_id][infected_status].keys():
                    self.layer_counts[sandbox_id][infected_status]["graph"][layer] = 1
                else:
                    self.layer_counts[sandbox_id][infected_status]["graph"][layer] += 1
    
    def extract_IP_adresses(self, sandbox_id, infected_status, data):
        for layer in data["packet"].keys():
            if layer in ["IP"]:
                src = data["packet"]["IP"]["src"]
                dst = data["packet"]["IP"]["dst"]

                empty_model = {
                    "healthy_src":0,
                    "healthy_dst":0,
                    "infected_src":0,
                    "infected_dst":0
                }
                # check if src address exists
                if src not in self.ip_adress_frequency[sandbox_id].keys():
                    # create new object because src ip does not exist
                    self.ip_adress_frequency[sandbox_id][src] = empty_model
                # add to counter
                self.ip_adress_frequency[sandbox_id][src][infected_status+"_src"] += 1

                # check if dst address exists
                if dst not in self.ip_adress_frequency[sandbox_id].keys():
                    # create new object because dst ip does not exist
                    self.ip_adress_frequency[sandbox_id][dst] = empty_model
                self.ip_adress_frequency[sandbox_id][dst][infected_status+"_dst"] += 1

                print(self.ip_adress_frequency[sandbox_id])
    
    def export_pcap(self, data, ID):
        for infected_status in data.keys():
            for packet in data[infected_status]:
                pkt = import_object(packet["export"][1:-1])
                wrpcap(infected_status + '/' + str(ID) + '.pcap', pkt, append=True)


    def save_data(self, data):
        try:
            print("Saving Network Data: ", data["ID"])
            i = data["ID"]
            pm = models.NetworkModel(
                ID=i,
                layer_counts=json.dumps(self.layer_counts[i]),
                IP_frequency=json.dumps(self.ip_adress_frequency[i])
            )
            pm.save()
            print("Exporting PCAP... ")
            self.export_pcap(self.raw_packet_data[i], i)
            print("Done!")
        except KeyError:
            print("No network data to save, proceeding...")
    