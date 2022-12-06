from flask_mongoengine import Document
from flask_mongoengine import MongoEngine as db


class Malware(db().Document):
    name = db().StringField()
    hash = db().StringField(unique=True)
    url = db().StringField()
    type = db().StringField()
    bitness = db().IntField()
    tags = db().ListField(db().StringField()) 

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "name": self.name,
            "hash": self.hash,
            "url": self.url,
            "type": self.type,
            "tags": self.tags
        }


class Process(db().Document):
    SHA256 = db().StringField()
    ID = db().StringField(unique=True)
    malware = db().ReferenceField(Malware, dbref=True)
    selected_os = db().StringField()

    def to_json(self):
        return {"SHA256": self.SHA256,
                "ID": self.ID,
                "selected_os": self.selected_os
        }

class PerformanceModel(Document):
    ID = db().StringField(unique=True)
    pid_counts = db().StringField()
    cpu_percentages = db().StringField()
    ram_usage = db().StringField()
    packet_counts = db().StringField()
    raw_perf_data = db().StringField()

    def to_json(self):
        return {"ID": self.ID,
                "pid_counts": self.pid_counts,
                "cpu_percentages":self.cpu_percentages,
                "ram_usage":self.ram_usage,
                "packet_counts":self.packet_counts,
                "raw_perf_data":self.raw_perf_data
        }

class NetworkModel(Document):
    ID = db().StringField(unique=True)
    layer_counts = db().StringField()
    IP_frequency = db().StringField()


    def to_json(self):
        return {"ID": self.ID,
                "layer_counts": self.layer_counts,
                "IP_frequency":self.IP_frequency
        }

class SystemCallModel(Document):
    ID = db().StringField(unique=True)
    reads_vs_writes = db().StringField()
    directory_frequency = db().StringField()


    def to_json(self):
        return {"ID": self.ID,
                "reads_vs_writes": self.reads_vs_writes,
                "directory_frequency":self.directory_frequency
        }


class Report(Document):
    ID = db().StringField(unique=True)
    title = db().StringField(max_lenth=200, required=True)
    date = db().StringField()  # 1 to 9
    malware = db().ReferenceField(Malware)
    selected_graphs = db().ListField()

    def __str__(self):
        return self.title

    def to_json(self):
        return {"ID": self.ID,
                "title": self.title,
                "date":self.date,
                "malware":self.malware,
                "selected_graphs":self.selected_graphs
        }

