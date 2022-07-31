from mysql import connector

class VideoService:
    def __init__(self, config):
        self.connector = connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"]
            )
