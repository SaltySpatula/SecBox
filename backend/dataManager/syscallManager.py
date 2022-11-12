from os import system
import system_calls
import platform
from backend.dataManager.dataManager import DataManager

class SysCallManager(DataManager):
    def __init__(self,fe_client, db):
        super().__init__(fe_client, db)
        self.arch = platform.processor()
        #self.translation_array = list(system_calls.syscalls["archs"][self.arch].keys())
        #self.index_array = list(system_calls.syscalls["archs"][self.arch].values())

    def handle_message(self, data):
        processed_data = self.process_data(data)
        if not self.save_data(processed_data):
            return False
        return True
        

    def process_data(self, data):
        pass

    def save_data(self, data):
        pass