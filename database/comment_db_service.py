from mysql import connector
from models.video.video import Video
from models.video.comment import Comment

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
        query = f"SELECT * from {self.table} WHERE video = %s"
        values = (video,)
        cursor = self.connector.cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()

        comments = []
        for res in results:
            comments.append(Comment(*res))
            
        return comments


        
