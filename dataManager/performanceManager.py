from argparse import Namespace
from dataManager import DataManager
import datetime


class PerformanceManager(DataManager):
    def __init__(self, fe_client, db):
        super().__init__(fe_client, db)
        self.cpu_percentages = {}
        self.pid_counts = {}
        self.order_nos = {}
        self.packet_counts = {}

    def setup_data_structures(self, sandbox_id, infected_status, data):
        self.order_nos[sandbox_id] = {}
        self.order_nos[sandbox_id][infected_status] = data["orderNo"]

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

        if self.order_nos[sandbox_id][infected_status]["orderNo"] <= data["orderNo"]:
            # Call emit functions here
            self.extract_cpu_percentages(sandbox_id, infected_status)
            self.extract_pid_count(sandbox_id, infected_status)
            self.extract_packet_count(sandbox_id, infected_status)

            self.fe_client.emit(
                self.cpu_percentages[sandbox_id][infected_status]["graph"], namespace='/live')
            self.fe_client.emit(
                self.pid_counts[sandbox_id][infected_status]["graph"], namespace='/live')
            self.fe_client.emit(
                self.packet_counts[sandbox_id][infected_status]["graph"], namespace='/live')

        return True

    def save_data(self, data):
        pass

    def extract_pid_count(self, sandbox_id, infected_status, data):
        instance_history = data[sandbox_id][infected_status]

        current_ts = datetime.strptime(
            instance_history["read"], "%Y-%m-%d %H:%M:%S")
        current_pid_count = instance_history["pids_stats"]["current"]
        self.pid_counts[sandbox_id][infected_status]["graph"].append(
            {"timestamp": current_ts, "pid_count": current_pid_count})

    def extract_cpu_percentages(self, sandbox_id, infected_status, data):
        current_ts = datetime.strptime(data["read"], "%Y-%m-%d %H:%M:%S")
        current_ns = data["cpu_stats"]["cpu_usage"]["total_usage"]

        if data["orderNo"] == 1:
            self.cpu_percentages[sandbox_id][infected_status]["previous_ts"] = current_ts
            self.cpu_percentages[sandbox_id][infected_status]["previous_ns"] = current_ns
            self.cpu_percentages[sandbox_id][infected_status]["graph"].append(
                {"timestamp": current_ts.srftime("%Y-%m-%d %H:%M:%S"), "cpu_percentage": 0})
        else:
            previous_ns = self.cpu_percentages[sandbox_id][infected_status]["previous_ns"]
            previous_ts = self.cpu_percentages[sandbox_id][infected_status]["previous_ts"]

            nanoseconds_delta = (previous_ts - current_ts).microseconds * 1000
            percentage = (previous_ns - current_ns) / nanoseconds_delta * 100

            self.cpu_percentages[sandbox_id][infected_status]["graph"].append(
                {"timestamp": current_ts.srftime("%Y-%m-%d %H:%M:%S"), "cpu_percentage": percentage})

            self.cpu_percentages[sandbox_id][infected_status]["previous_ts"] = current_ts
            self.cpu_percentages[sandbox_id][infected_status]["previous_ns"] = current_ns

    def extract_packet_count(self, sandbox_id, infected_status, data):
        current_ts = datetime.strptime(
            data["read"], "%Y-%m-%d %H:%M:%S")
        current_pid_count = data["pids_stats"]["current"]

        self.pid_counts[sandbox_id][infected_status]["graph"].append(
            {"timestamp": current_ts, "pid_count": current_pid_count})
