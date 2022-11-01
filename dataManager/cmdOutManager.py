from dataManager.dataManager import DataManager

class CmdOutManager(DataManager):
    def __init__(self,fe_client, db):
        super().__init__(fe_client, db)
        self.order_nos = {}
    
    def setup_data_structures(self, sandbox_id, infected_status, data):
        self.order_nos[sandbox_id] = {"healthy": 1, "infected": 1}


    def handle_message(self, data):
        sandbox_id = data["ID"]
        infected_status = data["infectedStatus"]
        if sandbox_id not in self.order_nos.keys():
            self.setup_data_structures(sandbox_id, infected_status, data)
        if self.order_nos[sandbox_id][infected_status] <= data["orderNo"]:
            message = {
                "infectedStatus": infected_status,
                "cmdOut": data["cmdOut"]
            }
            self.socketio.emit("terminalOutput", json.dumps(message) ,namespace="/live", to=sandbox_id)
            self.order_nos[sandbox_id][infected_status] = data["orderNo"]
        self.db_queue.put(data)
        return True

    def save_data(self, data):
        pass