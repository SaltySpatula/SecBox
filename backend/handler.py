import time
import json
import subprocess

counter = 0

def start_process():
    time.sleep(10)
    return "MQ=="

def start_process(sha, selected_os):
    global counter
    counter = counter + 1
    random_id = counter
    dictionary = {
        "ID": random_id,
        "SHA256": sha,
        "OS": selected_os,
    }
    return dictionary


def get_available_os():
    oss = ["ubuntu 22.04", "ubuntu 20.04", "ubuntu 18.04"]
    return json.dumps(oss)


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
                                                                                     "hash": "e2394ac05edcb0094bac8a12a6d5adfdbe56239165e81b773a16a81236b28b4f",
                                                                                     "url": "https://bazaar.abuse.ch/sample/e2394ac05edcb0094bac8a12a6d5adfdbe56239165e81b773a16a81236b28b4f/"
                                                                                     },

                "6537d07bcfebd413e82d10b3a2308cb922605a3adae3aa8091af6548ac267106": {"name": "Gafgyt",
                                                                                     "type": "elf",
                                                                                     "tags": ["elf", "mirai"],
                                                                                     "hash": "6537d07bcfebd413e82d10b3a2308cb922605a3adae3aa8091af6548ac267106",
                                                                                     "url": "https://bazaar.abuse.ch/sample/6537d07bcfebd413e82d10b3a2308cb922605a3adae3aa8091af6548ac267106"
                                                                                     }
                }

    return json.dumps(data_set)


def get_available_images():
    output = subprocess.run(
        ['curl', '-L', '-s', 'https://registry.hub.docker.com/v2/repositories/library/ubuntu/tags?page_size=40'], text=True, capture_output=True)
    available_images = []
    for item in json.loads(output.stdout)['results']:
        available_images.append("ubuntu:"+item['name'])
    return available_images
