import time


def start_process():
    time.sleep(10)
    return "MQ=="


def get_reports():
    # some DB action required
    reports = "[{name:Mirai,},{name:Bhdo,}]"
    return reports
