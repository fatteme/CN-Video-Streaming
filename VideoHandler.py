from video.Video import Video
import cv2
import wave
import os

def sendVideo():
    pass

class ServerVideo:
     _instance = None
     @staticmethod
     def getInstance():
         if ServerVideo._instance == None:
             ServerVideo()
         return ServerVideo._instance
     
     def __init__(self):
         if ServerVideo._instance != None:
             raise Exception("You can not have more than one super admin!")
         else:
             pass

     def getVideo(self, vid_name): # get video from database
        return None
     
     def sendAudio(self, vid_name):
        print("Sending Audio ...")
        video = self.getVideo(vid_name)
        audio_name = video.name.replace(".mp4", ".wav")
        audio_path = os.path.join(os.getcwd(), 'audios', audio_name)

        BUFF_SIZE = 65536

        CHUNK = 4 * 1024
        wf = wave.open(audio_path)

        data = None
        sample_rate = wf.getframerate()

        while True:
            data = wf.readframes(CHUNK)
            client.sendall(data)
            time.sleep(0.8 * CHUNK / sample_rate)  
     
     def sendVideo(self, client, vid_name):
        print("Sending Video ...")

        video = self.getVideo(vid_name) 
        video_path = os.path.join(os.getcwd(), 'videos', video.name)
        try:
            while True:
                if client:
                    vid = cv2.VideoCapture(video_path)

                    while vid.isOpened():
                        img, frame = vid.read()
                        a = pickle.dumps(frame)
                        message = struct.pack("Q", len(a)) + a
                        client.sendall(message)
                break
        except:
            print("exception occured! (video)")

        print("-------- stopped streaming")
        if vid:
            vid.release()
            cv2.destroyAllWindows()
       
     def saveVideo(self):
         pass
            
     def receiveAudio(self):
         pass

     def receiveVideo(self):
         pass


class ClientVideo: # only should have instances in EndUser
    def __init__(self):
        pass

    def getVideo(self, path):
        pass

    def sendAudio(self, path):
        print("Uoloading Audio ...")
        video = self.getVideo(path)
        audio_name = video.name.replace(".mp4", ".wav")
        audio_path = os.path.join(os.getcwd(), 'audios', audio_name)

        BUFF_SIZE = 65536

        CHUNK = 4 * 1024
        wf = wave.open(audio_path)

        data = None
        sample_rate = wf.getframerate()

        while True:
            data = wf.readframes(CHUNK)
            client.sendall(data)
            time.sleep(0.8 * CHUNK / sample_rate)  
     
    def sendVideo(self, client, path):
        print("Uploading Video ...")

        video = self.getVideo(path) 
        video_path = os.path.join(os.getcwd(), 'videos', video.name)
        try:
            while True:
                if client:
                    vid = cv2.VideoCapture(video_path)

                    while vid.isOpened():
                        img, frame = vid.read()
                        a = pickle.dumps(frame)
                        message = struct.pack("Q", len(a)) + a
                        client.sendall(message)
                break
        except:
            print("exception occured! (video)")

        print("-------- stopped streaming")
        if vid:
            vid.release()
            cv2.destroyAllWindows()

    def receiveAudio(self):
         pass

    def receiveVideo(self):
         pass