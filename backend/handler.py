import time
import json
import subprocess
import requests
import uuid
from backend import models


def start_process(sha, selected_os):
    dictionary = {
        "ID": uuid.uuid4().hex,
        "SHA256": sha,
        "OS": selected_os,
    }
    return dictionary


def get_reports():
    reports = models.Report.objects()
    try:
        for report in reports:
            report["malware"] = json.loads(report["malware"])
    except:
        print("no malware found")
    return reports


def get_available_images():
    output = subprocess.run(
        ['curl', '-L', '-s', 'https://registry.hub.docker.com/v2/repositories/library/ubuntu/tags?page_size=40'],
        text=True, capture_output=True)
    available_images = []
    for item in json.loads(output.stdout)['results']:
        available_images.append("ubuntu:" + item['name'])
    return available_images


def write_malware_to_DB():
    print("Looking for Malware out there...")
    data = {'query': 'get_file_type', 'file_type': 'elf', 'limit': 10000}
    url = "https://mb-api.abuse.ch/api/v1/"
    response = requests.post(url, data=data)
    malware_list = []
    if response.status_code == 200:
        response = response.json()
        malware_names = [(malware["name"], malware["type"]) for malware in models.Malware.objects]
        for malware in response["data"]:
            if malware["tags"]:
                if "32" in malware["tags"] or "64" in malware["tags"]:
                    bitness = 64 if "64" in malware["tags"] else 32
                    if (malware["signature"], malware["file_type"], bitness) not in malware_names and malware["signature"] is not None and ("64" in malware["tags"] or "32" in malware["tags"]):
                        malware_dict = {
                            "name": malware["signature"],
                            "hash": malware["sha256_hash"],
                            "url": "https://bazaar.abuse.ch/sample/" + str(malware["sha256_hash"]) + "/",
                            "type": malware["file_type"],
                            "bitness": bitness,
                            "tags": malware["tags"]
                        }
                        malware_list.append(malware_dict)
                        malware_names.append((malware_dict["name"], malware_dict["type"], bitness))
        malware_list.append({
            "name": "DarkRadiation",
            "hash": "89a694bea1970c2d66aec04c3e530508625d4b28cc6f3fc996e7ba99f1c37841",
            "url": "https://bazaar.abuse.ch/sample/" + "89a694bea1970c2d66aec04c3e530508625d4b28cc6f3fc996e7ba99f1c37841" + "/",
            "type": "sh",
            "bitness": 64,
            "tags": ["DarkRadiation", "Ransomware", "sh", "64"]
        }
        )
        malware_list.append({
            "name": "Monti",
            "hash": "edfe81babf50c2506853fd8375f1be0b7bebbefb2e5e9a33eff95ec23e867de1",
            "url": "https://bazaar.abuse.ch/sample/" + "edfe81babf50c2506853fd8375f1be0b7bebbefb2e5e9a33eff95ec23e867de1" + "/",
            "type": "elf",
            "bitness": 64,
            "tags": ["Monti", "Ransomware", "elf", "64"]
        })
        malware_list.append({
            "name": "CoinMiner",
            "hash": "0e79ec7b00c14a4c576803a1fd2e8dd3ea077e4e98dafa77d26c0f9d6f27f0c9",
            "url": "https://bazaar.abuse.ch/sample/" + "0e79ec7b00c14a4c576803a1fd2e8dd3ea077e4e98dafa77d26c0f9d6f27f0c9" + "/",
            "type": "sh",
            "bitness": 64,
            "tags": ["CoinMiner", "Miner", "elf", "64"]
        })
    else:
        print("Invalid Request Response!")

    data = {'query': 'get_file_type', 'file_type': 'sh', 'limit': 10000}
    url = "https://mb-api.abuse.ch/api/v1/"
    response = requests.post(url, data=data)
    if response.status_code == 200:
        response = response.json()
        for malware in response["data"]:
            if malware["tags"]:
                if "32" in malware["tags"] or "64" in malware["tags"]:
                    bitness = 64 if "64" in malware["tags"] else 32
                    if (malware["signature"], malware["file_type"], bitness) not in malware_names and malware["signature"] is not None and ("64" in malware["tags"] or "32" in malware["tags"]):
                        malware_dict = {
                            "name": malware["signature"],
                            "hash": malware["sha256_hash"],
                            "url": "https://bazaar.abuse.ch/sample/" + str(malware["sha256_hash"]) + "/",
                            "type": malware["file_type"],
                            "bitness": bitness,
                            "tags": malware["tags"]
                        }
                        malware_list.append(malware_dict)
                        malware_names.append((malware_dict["name"], malware_dict["type"], bitness))
    else:
        print("Invalid Request Response!")
    for malware in malware_list:
        mwm = models.Malware(
            name=malware["name"],
            hash=malware["hash"],
            url=malware["url"],
            type=malware["type"],
            bitness = malware["bitness"],
            tags=malware["tags"]
        )
        try:
            mwm.save()
        except:
            print("Sample already present in DB, skipping...")
    print("Done!")


def get_available_malware(bitness):
    malware_list = []
    for malware in models.Malware.objects:
        if malware["bitness"]==bitness:
            malware_dict = {
                "name": malware["name"],
                "hash": malware["hash"],
                "url": malware["url"],
                "type": malware["type"],
                "bitness": malware["bitness"],
                "tags": malware["tags"]
            }
            malware_list.append(malware_dict)
    return malware_list
