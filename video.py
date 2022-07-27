from User.EndUser import EndUser

class Video:
    all_videos = []
    def __init__(self, name, uploader: EndUser):
        Video.all_videos.append(self)
        self.name = name
        self.uploader = uploader
        self.likes = 0
        self.dislikes = 0
        self.comments = []

    def like(self):
        self.likes += 1
    def dislike(self):
        self.dislikes += 1

########################## test
sa = Video("video1", "")
print(Video.all_videos[0].name)
sa.like()
print(Video.all_videos[0].likes)