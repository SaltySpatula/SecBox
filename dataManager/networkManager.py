from telnetlib import IP
from dataManager.dataManager import DataManager
from scapy.all import *


class NetworkManager(DataManager):
    def __init__(self, fe_client, db):
        super().__init__(fe_client, db)
    
    def setup_data_structures(self, sandbox_id, infected_status, data):
        pass

    def handle_message(self, data):
        processed_data = self.process_data(data)
        if not self.save_data(processed_data):
            return False
        # Call emit functions here
        return True

    def process_data(self, data):
        pass

#packet = Ether(data["packet"])
#data["layers"] = packet.layers
#return data"""
        
    def save_data(self, data):
        pass
