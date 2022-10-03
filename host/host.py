from controller import Controller
from multiprocessing import Process

def main():
    with Controller() as test_controller:
        test_controller.start_instances("./healthy/", "./infected/")
        test_controller.execute_command("apt-get install -y iputils-ping")
        test_controller.execute_command("ping google.com")
        test_controller.execute_command("ps")

if __name__ == "__main__":
    main()