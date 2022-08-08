from unicodedata import name
from mysql import connector
from models.video.video import Video

class VideoDBService:
    def __init__(self, config):
        self.connector = connector.connect(
            host=config["host"],
            user=config["user"],
            # password=config["password"],
            database=config["database"]
            )
        self.table = "video"

    def create_video(self, video: Video):
        try:
            query = f"INSERT INTO {self.table} (title, name_identifier, owner, adrs, available, likes, dislikes, label) Values (%s, %s, %s, %s, %s, %s, %s, %s)"
            video_dict = video.export()
            del video_dict["comments"]
            values = tuple(video_dict.values())

            print("values:", values)
            cursor = self.connector.cursor()
            cursor.execute(query, values)
            self.connector.commit()

            print(cursor.rowcount, "record inserted.")
        except Exception as e:
            print(e)

    def update_video(self, video: Video):
        query = f"UPDATE {self.table} SET name_identifier = %s, adrs = %s, available= %s, likes = %s, dislikes = %s, label = %s, WHERE title = %s"
        values = (video.name_identifier, video.adrs, video.available, video.likes, video.dislikes, video.label, video.title)

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        self.connector.commit()

        print(cursor.rowcount, "record(s) affected")

    def get_video(self, title):
        query = f"SELECT * from {self.table} WHERE title = %s"
        values = (title,)
        cursor = self.connector.cursor()
        cursor.execute(query, values)
        result = cursor.fetchone()
        return Video(title=result[0], name_identifier=result[1],
            owner=result[2], adrs=result[3], availabe=result[4], likes=result[5],
            dislikes=result[6], label=result[7])
