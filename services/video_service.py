from distutils.command.config import config
from consts import DB_CONFIG
from database.comment_db_service import CommentDBService
from database.video_db_service import VideoDBService
from models.video.video import Video
from models.video.comment import Comment



class VideoService:
    def __init__(self):
        self.videoDBService = VideoDBService(config=DB_CONFIG)
        self.commentDBService = CommentDBService(config=DB_CONFIG)

    def like(self, title):
        video = self.videoDBService.get_video(title=title)
        video.likes += 1
        self.videoDBService.update_video(video=video)
        return f'video liked!, likes: {video.likes}'
    
    def dislike(self, title):
        video: Video = self.videoDBService.get_video(title=title)
        video.dislikes += 1
        self.videoDBService.update_video(video=video)
        return f'video disliked!, dislikes: {video.dislikes}'

    def label(self, title, label):
        video: Video = self.videoDBService.get_video(title=title)
        video.label = f'{video.label}, {label}'
        self.videoDBService.update_video(video=video)
        return f'video label added. labels: {video.label}'

    def add_comment(self, video_title, user, comment):
        self.commentDBService.add_comment(Comment(user=user, video=video_title, text=comment))
        return f'comment added!, comment: {comment}'

    def get_video(self, title):
        video: Video = self.videoDBService.get_video(title=title)
        video_comments = self.commentDBService.get_all_comments(video=title)
        video_comments_str = "\n".join(list(map(lambda c: f'({c.user} - {c.text})', video_comments)))
        return f'video info =>\ntitle:{video.title}, likes:{video.likes}, dislikes:{video.dislikes}, comments:{video_comments_str}'

    def get_video_labels(self, title):
        video: Video = self.videoDBService.get_video(title=title)
        return f'video labels: {video.label}'

    def remove_video(self, title):
        self.videoDBService.delete_video(title=title)
        return f'video {title} removed.'