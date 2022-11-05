from dataManager.dataManager import DataManager
from dateutil import parser
from datetime import datetime
class PerformanceManager(DataManager):
    def __init__(self, socketio, db):
        super().__init__(socketio, db)
        self.cpu_percentages = {}
        self.pid_counts = {}
        self.order_nos = {}
        self.packet_counts = {}

    def setup_data_structures(self, sandbox_id, infected_status, data):
        self.order_nos[sandbox_id] = {"healthy": 1, "infected": 1}

        self.cpu_percentages[sandbox_id] = {
            "healthy": {"graph": []}, "infected": {"graph": []}}

        self.pid_counts[sandbox_id] = {"healthy": {
            "graph": []}, "infected": {"graph": []}}

        self.packet_counts[sandbox_id] = {
            "healthy": {"graph": []}, "infected": {"graph": []}}

    def handle_message(self, data):
        sandbox_id = data["ID"]
        infected_status = data["infectedStatus"]

        if sandbox_id not in self.order_nos.keys():
            self.setup_data_structures(sandbox_id, infected_status, data)
        if self.order_nos[sandbox_id][infected_status] <= data["orderNo"]:
            # Call emit functions here
            self.extract_cpu_percentages(sandbox_id, infected_status, data)
            self.extract_pid_count(sandbox_id, infected_status, data["stats"])
            self.extract_packet_count(
                sandbox_id, infected_status, data["stats"])

            # TODO: Create function for preppring data
            cpu_percentage_trimmed = self.cpu_percentages[sandbox_id][infected_status]["graph"]

            if len(cpu_percentage_trimmed) >= 60:
                cpu_percentage_trimmed = cpu_percentage_trimmed[-61:]

            times = []
            percentages = []
            for t in cpu_percentage_trimmed:
                time = datetime.strptime(t["timestamp"], "%m/%d/%Y, %H:%M:%S.%f%Z")
                times.append(datetime.strftime(time, "%H:%M:%S"))
                percentages.append(round(t["cpu_percentage"], 2))

            response_cpu_percentage = {
                "infected_status":infected_status,
                "data":{
                "timestamps":times,
                "percentages":percentages
                }
            }

            self.socketio.emit("cpu_percentages_graph",
                               response_cpu_percentage,
                               namespace='/live', room=str(sandbox_id))

            trimmed_pid_counts = self.pid_counts[sandbox_id][infected_status]["graph"]
            trimmed_pid_counts = trimmed_pid_counts[-1]
            self.socketio.emit("pid_graph",
                               trimmed_pid_counts, namespace='/live', room=str(sandbox_id))

            packets_trimmed = self.packet_counts[sandbox_id][infected_status]["graph"][-1:]

            times = []

            response_packets = {
                "infected_status": infected_status,
                "data": {
                    "packets": packets_trimmed
                }
            }

            self.socketio.emit("packet_graph",
                               response_packets, namespace='/live', room=str(sandbox_id))
            self.order_nos[sandbox_id][infected_status] = data["orderNo"]
        self.db_queue.put(data)
        return True

    def save_data(self, data):
        # ToDo:
        pass


    def extract_pid_count(self, sandbox_id, infected_status, data):
        current_ts = parser.parse(data["read"])
        current_pid_count = data["pids_stats"]["current"]
        self.pid_counts[sandbox_id][infected_status]["graph"].append(
            {"timestamp": current_ts.strftime("%m/%d/%Y, %H:%M:%S.%f%Z"), "pid_count": current_pid_count})

    def extract_cpu_percentages(self, sandbox_id, infected_status, data):
        current_ts = parser.parse(data["stats"]["read"])
        current_ns = data["stats"]["cpu_stats"]["cpu_usage"]["total_usage"]

        if data["orderNo"] == 1:
            self.cpu_percentages[sandbox_id][infected_status]["previous_ts"] = current_ts.strftime(
                "%m/%d/%Y, %H:%M:%S.%f%Z")
            self.cpu_percentages[sandbox_id][infected_status]["previous_ns"] = current_ns
            self.cpu_percentages[sandbox_id][infected_status]["graph"].append(
                {"timestamp": current_ts.strftime("%m/%d/%Y, %H:%M:%S.%f%Z"), "cpu_percentage": 0})
        else:
            previous_ns = self.cpu_percentages[sandbox_id][infected_status]["previous_ns"]
            previous_ts = parser.parse(
                self.cpu_percentages[sandbox_id][infected_status]["previous_ts"])

            nanoseconds_delta = (previous_ts - current_ts).microseconds * 1000
            percentage = current_ns / nanoseconds_delta * 100

            self.cpu_percentages[sandbox_id][infected_status]["graph"].append(
                {"timestamp": current_ts.strftime("%m/%d/%Y, %H:%M:%S.%f%Z"), "cpu_percentage": percentage})

            self.cpu_percentages[sandbox_id][infected_status]["previous_ts"] = current_ts.strftime(
                "%m/%d/%Y, %H:%M:%S.%f%Z")
            self.cpu_percentages[sandbox_id][infected_status]["previous_ns"] = current_ns

    def extract_packet_count(self, sandbox_id, infected_status, data):
        current_ts = parser.parse(
            data["read"])
        received_packages = data["networks"]["eth0"]["rx_packets"]
        transmitted_packages = data["networks"]["eth0"]["tx_packets"]

        self.packet_counts[sandbox_id][infected_status]["graph"].append(
            {"timestamp": current_ts.strftime("%m/%d/%Y, %H:%M:%S.%f%Z"), "received_packages": received_packages, "transmitted_packages": transmitted_packages})

    def batch_process():
        pass
