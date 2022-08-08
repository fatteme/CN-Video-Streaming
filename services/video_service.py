from consts import DB_CONFIG
from database.video_db_service import VideoDBService
from models.video.video import Video


class VideoService:
    def __init__(self):
        self.videoDBService = VideoDBService(config=DB_CONFIG)

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

    def get_video(self, title):
        video: Video = self.videoDBService.get_video(title=title)
        return f'video info =>\ntitle:{video.title},likes:{video.likes}, dislikes:{video.dislikes}'