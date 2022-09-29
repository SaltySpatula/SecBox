import time, json


def start_process():
    time.sleep(10)
    return "MQ=="


def get_reports():
    # some DB action required
    data_set = {"1": {"title": "Mirai Network Traffic analysis", "malware": "Mirai", "tags": ["elf"]},
                "2": {"title": "Javascript Malware", "malware": "Vjw0rm", "tags": ["js", "vjw0rm"]}}

    reports = json.dumps(data_set)
    return reports


def get_available_malwares():
    # some DB action required
    data_set = {"1": {"name": "Mirai", "type": "elf", "tags": ["elf"]},
                "2": {"name": "SFadf", "type": "elf", "tags": ["exe"]}}

    reports = json.dumps(data_set)
    return reports
