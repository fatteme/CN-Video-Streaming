from uuid import uuid4


class Video:
    def __init__(self, title, owner, adrs):
        self.title = title
        self.name_identifier = str(uuid4())
        self.owner = owner
        self.adrs = adrs
        self.available = True
        self.likes = 0
        self.dislikes = 0
        self.comments = []

    def export(self):
        return {
            "title": self.title,
            "name_identifier": self.name_identifier,
            "owner": self.owner, 
            "adrs": self.adrs,
            "available": self.available,
            "likes": self.likes,
            "dislikes": self.dislikes,
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
        v.comments = d["comments"]
        return v