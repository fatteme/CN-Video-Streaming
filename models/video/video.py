from uuid import uuid4


class Video:
    def __init__(self, title, owner, adrs, name_identifier=None, availabe=True, likes=0, dislikes=0, label="", comments=[]):
        print('video label', label)
        self.title = title
        self.name_identifier = name_identifier
        if not self.name_identifier:
            self.name_identifier = str(uuid4())
        self.owner = owner
        self.adrs = adrs
        self.available = availabe
        self.likes = likes
        self.dislikes = dislikes
        self.label = label
        self.comments = comments

    def export(self):
        return {
            "title": self.title,
            "name_identifier": self.name_identifier,
            "owner": self.owner, 
            "adrs": self.adrs,
            "available": self.available,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "label": self.label,
            "comments": self.comments
        }

    @staticmethod
    def generate(self, dictionary):
        d = dictionary
        v = Video(d["title"], d["owner"], d["adrs"])
        v.name_identifier = d["name_identifier"]
        v.available = d["available"]
        v.likes = d["likes"]
        v.dislikes = d["dislikes"]
        v.label = d["label"]
        v.comments = d["comments"]
        return v