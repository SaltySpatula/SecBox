from flask_mongoengine import Document
from flask_mongoengine import MongoEngine as db


class Malware(db().Document):
    name = db().StringField()
    hash = db().StringField(unique=True)
    url = db().StringField()
    type = db().StringField()
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
    malware = db().ReferenceField(Malware, dbref=True)
    selected_os = db().StringField()

    def to_json(self):
        return {"SHA256": self.SHA256,
                "selected_os": self.selected_os
        }

class PerformanceModel(Document):
    ID = db().StringField()
    pid_counts = db().StringField()
    cpu_percentages = db().StringField()
    packet_counts = db().StringField()
    raw_perf_data = db().StringField()

    def to_json(self):
        return {"ID": self.ID,
                "pid_counts": self.pid_counts,
                "cpu_percentages":self.cpu_percentages,
                "packet_counts":self.packet_counts,
                "raw_perf_data":self.raw_perf_data
        }

class NetworkModel(Document):
    ID = db().StringField()
    layer_counts = db().StringField()

    raw_packet_data = db().StringField()

    def to_json(self):
        return {"ID": self.ID,
                "layer_counts": self.layer_counts,
                "raw_packet_data":self.raw_packet_data
        }


class Report(Document):
    title = db().StringField(max_lenth=200, required=True, unique=True)
    date = db().IntField(default=0, max_lenth=1)  # 1 to 9
    malware = db().ReferenceField(Malware)

    def __str__(self):
        return self.title


