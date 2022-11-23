from backend.dataManager.dataManager import DataManager
from dateutil import parser
from datetime import datetime
import json
from backend import models


class PerformanceManager(DataManager):
    def __init__(self, socketio, db):
        super().__init__(socketio, db)
        self.cpu_percentages = {}
        self.pid_counts = {}
        self.packet_counts = {}
        self.raw_perf_data = {}

    def setup_data_structures(self, sandbox_id, infected_status, data):
        self.order_nos[sandbox_id] = {"healthy": 1, "infected": 1}

        self.cpu_percentages[sandbox_id] = {
            "healthy": {"graph": []}, "infected": {"graph": []}}

        self.pid_counts[sandbox_id] = {"healthy": {
            "graph": []}, "infected": {"graph": []}}

        self.packet_counts[sandbox_id] = {
            "healthy": {"graph": []}, "infected": {"graph": []}}

        self.raw_perf_data[sandbox_id] = {"healthy": [], "infected": []}

    def handle_message(self, data):
        sandbox_id = str(data["ID"])  # todo: remove string casting
        infected_status = data["infectedStatus"]

        if sandbox_id not in self.order_nos.keys():
            self.setup_data_structures(sandbox_id, infected_status, data)
        if self.order_nos[sandbox_id][infected_status] <= data["orderNo"]:
            # Call emit functions here
            self.extract_cpu_percentages(sandbox_id, infected_status, data)
            self.extract_pid_count(sandbox_id, infected_status, data["stats"])
            self.extract_packet_count(
                sandbox_id, infected_status, data["stats"])

            # TODO: Create function for prepping data
            cpu_percentage_trimmed = self.cpu_percentages[sandbox_id][infected_status]["graph"]

            if len(cpu_percentage_trimmed) >= 60:
                cpu_percentage_trimmed = cpu_percentage_trimmed[-60:]
            else:
                length_dummy_data = 60 - len(cpu_percentage_trimmed)
                dummy_data = length_dummy_data * [cpu_percentage_trimmed[0]]
                cpu_percentage_trimmed = dummy_data + cpu_percentage_trimmed

            times = []
            percentages = []
            for t in cpu_percentage_trimmed:
                time = datetime.strptime(
                    t["timestamp"], "%m/%d/%Y, %H:%M:%S.%f%Z")
                times.append(datetime.strftime(time, "%H:%M:%S"))
                percentages.append(round(t["cpu_percentage"], 4))

            response_cpu_percentage = {
                "infected_status": infected_status,
                "data": {
                    "timestamps": times,
                    "percentages": percentages
                }
            }

            self.socketio.emit("cpu_percentages_graph",
                               response_cpu_percentage,
                               namespace='/live', room=str(sandbox_id))

            trimmed_pid_counts = self.pid_counts[sandbox_id][infected_status]["graph"]

            if len(self.pid_counts[sandbox_id][infected_status]["graph"]) >= 2:
                # if a new value appears, we send it to the front end (we also send every 20th
                if trimmed_pid_counts[-1]["pid_count"] != trimmed_pid_counts[-2]["pid_count"] or len(trimmed_pid_counts) % 20 == 0:
                    response_pid = {
                        "infected_status": infected_status,
                        "data": {
                            "pid_count": trimmed_pid_counts[-1]
                        }
                    }
                    self.socketio.emit("pid_graph",
                                       response_pid, namespace='/live', room=str(sandbox_id))

            else:
                response_pid = {
                    "infected_status": infected_status,
                    "data": {
                        "pid_count": trimmed_pid_counts[-1]
                    }
                }
                self.socketio.emit("pid_graph",
                                   response_pid, namespace='/live', room=str(sandbox_id))

            packets_trimmed = self.packet_counts[sandbox_id][infected_status]["graph"][-1:]

            response_packets = {
                "infected_status": infected_status,
                "data": {
                    "packets": packets_trimmed
                }
            }

            self.socketio.emit("packet_graph",
                               response_packets, namespace='/live', room=str(sandbox_id))
            self.order_nos[sandbox_id][infected_status] = data["orderNo"]
            self.raw_perf_data[sandbox_id][infected_status].append(data["stats"])
        return True

    def save_data(self, data):
        print("Saving Performance Data: ", data["ID"])
        i = data["ID"]
        pm = models.PerformanceModel(
            ID=i,
            pid_counts=json.dumps(self.pid_counts[i]),
            cpu_percentages=json.dumps(self.cpu_percentages[i]),
            packet_counts=json.dumps(self.packet_counts[i]),
            raw_perf_data=json.dumps(self.raw_perf_data[i])
        )
        pm.save()

    def extract_pid_count(self, sandbox_id, infected_status, data):
        current_ts = parser.parse(data["read"])
        # Todo: Fix error after shutdown
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
            if nanoseconds_delta:
                percentage = (current_ns-previous_ns) / nanoseconds_delta * 100
            else:
                percentage = 0

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
