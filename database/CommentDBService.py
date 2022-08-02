from mysql import connector
from models.video.Video import Video
from models.video.Comment import Comment

class CommentDBService:
    def __init__(self, config):
        self.connector = connector.connect(
            host=config["host"],
            user=config["user"],
            # password=config["password"],
            database=config["database"]
            )
        self.table = "Comment"

    def add_comment(self, comment: Comment):
        query = f"INSERT INTO {self.table} (username, video, text) Values (%s, %s, %s)"
        values = (comment.user, comment.video, comment.text)

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        self.connector.commit()

        print(cursor.rowcount, "record inserted.")

    def get_all_comments(self, video: str):
        query = f"SELECT (username, text) from {self.table} JOIN Video ON {self.table}.video = Video.title WHERE video = %s"
        values = (video,)

        cursor = self.connector.cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        for res in results:
            yield Comment(res[0], video, res[1])


        
