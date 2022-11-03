from dataManager.dataManager import DataManager
from scapy.all import *
from scapy.utils import hexstr


class NetworkManager(DataManager):
    def __init__(self, fe_client, db):
        super().__init__(fe_client, db)
    
    def setup_data_structures(self, sandbox_id, infected_status, data):
        pass

    def handle_message(self, data):
        p = import_object(data["packet"][1:-1])
        # p.show()

        processed_data = self.process_data(data)
        if not self.save_data(processed_data):
            return False
        # Call emit functions here
        return True

    def process_data(self, data):
        pass
        
    def save_data(self, data):
        pass
