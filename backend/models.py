from flask_mongoengine import Document
from flask_mongoengine import MongoEngine as db


class Process(db().Document):
    SHA256 = db().StringField()
    selected_os = db().StringField()

    def to_json(self):
        return {"SHA256": self.SHA256,
                "selected_os": self.selected_os}


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


class Report(Document):
    title = db().StringField(max_lenth=200, required=True, unique=True)
    date = db().IntField(default=0, max_lenth=1)  # 1 to 9
    malware = db().ReferenceField(Malware)

    def __str__(self):
        return self.title

