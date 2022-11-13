from os import system
import system_calls
import platform
from backend.dataManager.dataManager import DataManager

class SysCallManager(DataManager):
    def __init__(self,socketio, db):
        super().__init__(socketio, db)
        self.syscalls = system_calls.syscalls()

        self.reads_vs_writes = {}

    def setup_data_structures(self, sandbox_id, infected_status, data):
        self.order_nos[sandbox_id] = {"healthy": 1, "infected": 1}

        self.reads_vs_writes[sandbox_id] = {
            "healthy": {"graph": {"reads":0, "writes": 0}}, "infected": {"graph": {"reads": 0, "writes":0}}}


    def handle_message(self, data):
        processed_data = self.process_data(data)
        sandbox_id = processed_data["ID"]
        infected_status = processed_data["infectedStatus"]

        if sandbox_id not in self.order_nos.keys():
            self.setup_data_structures(sandbox_id, infected_status, processed_data)
        if self.order_nos[sandbox_id][infected_status] <= processed_data["orderNo"]:
            if processed_data["sysCall"]:

                #Call extract functions here
                self.extract_reads_v_writes(sandbox_id, infected_status, processed_data)

                #Call emit fucntions here
                self.socketio.emit("reads_vs_writes_graph",
                                self.reads_vs_writes,
                                namespace='/live', room=str(sandbox_id))
                # Add order no to history
                self.order_nos[sandbox_id][infected_status] = processed_data["orderNo"]
        self.db_queue.put(processed_data)
        return True
    
    def get_name_from_no(self, sysno, architecture):
        names = list(self.syscalls.syscalls["archs"][architecture].keys())
        index = list(self.syscalls.syscalls["archs"][architecture].values()).index(sysno)
        return names[index]

    def process_data(self, data):
        components = data["sysCall"].split()
        
        if components[0] in ["b'E", "b'X"]:
            args = []
            time = int(components[5])
            thread = int(components[7])
            sysno = int(components[17])
            sysname = self.get_name_from_no(sysno, data["architecture"])
            container_id = components[9]
            cwd= components[14]
            cred = components[11:13]

            for i in range(len(components[16:])):
                if i%2==1:
                    #TODO: Fix last argument newline still inside
                    args.append(components[16:][i])

            system_call = {
                "time_ns": time,
                "thread_id": thread,
                "sysno": sysno,
                "sysname": sysname,
                "container_id": container_id,
                "cwd": cwd,
                "credentials": cred,
                "args": args
            }
            data["sysCall"] = system_call
        else:
            data["sysCall"]=0
        return data


    def save_data(self, data):
        pass

    def extract_reads_v_writes(self, sandbox_id, infected_status, data):
        if data["sysCall"]["sysname"]=="read":
            ++self.reads_vs_writes[sandbox_id][infected_status]["graph"]["reads"]
        if data["sysCall"]["sysname"]=="write":
            ++self.reads_vs_writes[sandbox_id][infected_status]["graph"]["writes"]