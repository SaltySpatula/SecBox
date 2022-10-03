from controller import Controller
from multiprocessing import Process
from monitors.systemCallMonitor import systemCallMonitor

def main():
    with systemCallMonitor() as systemCallmonitor:
        with Controller() as test_controller:
            test_controller.execute_command("apt-get install -y iputils-ping")
            test_controller.execute_command("ping google.com")
            test_controller.execute_command("ps")

if __name__ == "__main__":
    main()