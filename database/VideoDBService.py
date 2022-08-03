from mysql import connector
from models.video.Video import Video

class VideoDBService:
    def __init__(self, config):
        self.connector = connector.connect(
            host=config["host"],
            user=config["user"],
            # password=config["password"],
            database=config["database"]
            )
        self.table = "Video"

    def create_video(self, video: Video):
        query = f"INSERT INTO {self.table} (title, name_identifier, owner, adrs, available, likes, dislikes) Values (%s, %s, %s, %s, %s, %s, %s)"
        video_dict = video.export()
        del video_dict["comments"]
        assert len(video_dict) == 7
        values = tuple(video_dict.values())

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        self.connector.commit()

        print(cursor.rowcount, "record inserted.")

    def update_video(self, video: Video):
        query = f"UPDATE {self.table} SET name_identifier = %s, adrs = %s, available= %s, likes = %s, dislikes = %s WHERE title = %s"
        values = (video.name_identifier, video.adrs, video.available, video.likes, video.dislikes, video.title)

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        self.connector.commit()

        print(cursor.rowcount, "record(s) affected")
