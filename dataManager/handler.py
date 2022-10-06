import time, json
from api import hostapp


def start_process():
    expected_json = {
        'ID': 123,
        'SHA256': '094fd325049b8a9cf6d3e5ef2a6d4cc6a567d7d49c35f8bb8dd9e3c6acf3d78d',
        'OS': 'ubuntu:latest',
    }
    return expected_json


def get_reports():
    # some DB action required
    data_set = {"1": {"title": "Mirai Network Traffic analysis", "malware": "Mirai", "tags": ["elf"]},
                "2": {"title": "Javascript Malware", "malware": "Vjw0rm", "tags": ["js", "vjw0rm"]}}

    reports = json.dumps(data_set)
    return reports


def get_available_malwares():
    # some DB action required
    data_set = {"e2394ac05edcb0094bac8a12a6d5adfdbe56239165e81b773a16a81236b28b4f": {"name": "Mirai",
                                                                                     "type": "elf",
                                                                                     "tags": ["elf"],
                                                                                     "hash":"e2394ac05edcb0094bac8a12a6d5adfdbe56239165e81b773a16a81236b28b4f",
                                                                                     "url":"https://bazaar.abuse.ch/sample/e2394ac05edcb0094bac8a12a6d5adfdbe56239165e81b773a16a81236b28b4f/"
                                                                                     },

                "6537d07bcfebd413e82d10b3a2308cb922605a3adae3aa8091af6548ac267106": {"name": "Gafgyt",
                                                                                     "type": "elf",
                                                                                     "tags": ["elf", "mirai"],
                                                                                     "hash":"6537d07bcfebd413e82d10b3a2308cb922605a3adae3aa8091af6548ac267106",
                                                                                    "url":"https://bazaar.abuse.ch/sample/6537d07bcfebd413e82d10b3a2308cb922605a3adae3aa8091af6548ac267106"
                                                                                     }
                }

    malwares = json.dumps(data_set)
    return malwares


