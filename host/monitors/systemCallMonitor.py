import socket
import os
from  subprocess import Popen, PIPE, STDOUT

healthy_server_address = "/tmp/healthy_gvisor_events.sock"
infected_server_address = "/tmp/infected_gvisor_events.sock"

healthy_configuration_file = "SecBox/host/healthy/session.json"
infected_configuration_file = "SecBox/host/infected/session.json"


class systemCallMonitor:
    def __init__(self, server_adress) -> None:
        self.server_address = server_adress

    def monitoring_process(server_address):
        server = Popen("/usr/bin/bazel run examples/seccheck:server_cc", server_address)
        with open(server_address[5:] + "_syscalls.log") as f:
            for line in server.stdout:
                print(line, file=f)
                # ToDo: Stream over Websocket
    


