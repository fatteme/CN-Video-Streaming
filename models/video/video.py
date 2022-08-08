from uuid import uuid4


class Video:
    def __init__(self, title, owner, adrs, name_identifier=None, availabe=True, likes=0, dislikes=0, comments=[], label=""):
        self.title = title
        self.name_identifier = name_identifier
        if not self.name_identifier:
            self.name_identifier = str(uuid4())
        self.owner = owner
        self.adrs = adrs
        self.available = availabe
        self.likes = likes
        self.dislikes = dislikes
        self.comments = comments
        self.label = label

    def export(self):
        return {
            "title": self.title,
            "name_identifier": self.name_identifier,
            "owner": self.owner, 
            "adrs": self.adrs,
            "available": self.available,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "comments": self.comments,
            "label": self.label
        }

    @staticmethod
    def generate(self, dictionary):
        d = dictionary
        v = Video(d["title"], d["owner"], d["adrs"])
        v.name_identifier = d["name_identifier"]
        v.available = d["available"]
        v.likes = d["likes"]
        v.dislikes = d["dislikes"]
        v.comments = d["comments"]
        v.label = d["label"]
        return v