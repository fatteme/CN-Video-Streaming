from models.video.video import Video
import cv2
import wave
import time
import pickle
import os
import pyaudio
import struct
import traceback
import moviepy.editor as mp
import socket


class server_video:
    _instance = None

    @staticmethod
    def getInstance():
        if server_video._instance is None:
            server_video()
        return server_video._instance

    def __init__(self):
        if server_video._instance is not None:
            raise Exception("You can not have more than one super admin!")
        else:
            pass

    def get_video(self, vid_name):  # get video from database
        return None

    def send_audio(self, vid_name):
        print("Sending Audio ...")
        video_path = self.get_video(vid_name)
        audio_path = video_path.name.replace(".mp4", ".wav")

        CHUNK = 4 * 1024
        wf = wave.open(audio_path)

        data = None
        sample_rate = wf.getframerate()

        while True:
            data = wf.readframes(CHUNK)
            if data == b'':
                break
            # client.sendall(data)
            time.sleep(0.8 * CHUNK / sample_rate)
        wf.close()

    def send_video(self, client, vid_name):
        print("Sending Video ...")

        video_path = self.get_video(vid_name)
        try:
            while True:
                if client:
                    vid = cv2.VideoCapture(video_path)

                    success = True
                    while success:
                        success, frame = vid.read()
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

    def save_video(self, video, frame):
        video.write(frame)

    def save_audio(self, wf2, frame):
        wf2.writeframes(frame)

    def receive_audio(self):
        audio_path = "sth"  # todo add legit audio path
        wf2 = wave.open(audio_path.replace("vid.wav", "vid2.wav"), 'w')

        wf2.setnchannels(1)  # todo wf.getnchannels()
        wf2.setsampwidth(2)  # todo wf.getsampwidth()
        wf2.setframerate(20)  # todo wf.getframerate()

        while True:
            try:
                frame = self.audio_stream_socket.recv(4 * 1024)
                self.save_audio(wf2, frame)
            except Exception as e:
                wf2.close()
                break

    def receive_video(self):
        print("receiving video...")

        data = b""
        payload_size = struct.calcsize("Q")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        first_time = True

        try:
            while True:
                while len(data) < payload_size:
                    packet = self.video_stream_socket.recv(4 * 1024)  # 4K
                    if not packet: break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += self.video_stream_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)

                if first_time:
                    height, width, layers = frame.shape
                    video = cv2.VideoWriter('video.avi', fourcc, 20, (width, height))  # todo fix fps, address
                    first_time = False
                self.save_video(video, frame)
            print("upload ended")
        except:
            traceback.print_exc()
            print("upload ended")


class client_video:  # only should have instances in EndUser
    def __init__(self):
        pass
        # todo audio and video stream socket initialization

    def get_video(self, path):
        pass

    def send_audio(self, path):
        print("Uploading Audio ...")

        video_path = self.get_video(path)
        audio_path = video_path.replace(".mp4", ".wav")

        my_clip = mp.VideoFileClip(video_path)
        my_clip.audio.write_audiofile(audio_path)

        CHUNK = 4 * 1024
        wf = wave.open(audio_path)

        data = None
        sample_rate = wf.getframerate()

        while True:
            data = wf.readframes(CHUNK)
            if data == b'':
                break
            # client.sendall(data)
            time.sleep(0.8 * CHUNK / sample_rate)
        wf.close()

    def send_video(self, client, path):
        print("Uploading Video ...")

        video = self.get_video(path)
        video_path = os.path.join(os.getcwd(), 'videos', video.name)
        try:
            while True:
                if client:
                    vid = cv2.VideoCapture(video_path)

                    success = True
                    while success:
                        success, frame = vid.read()
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

    def receive_audio(self):
        p = pyaudio.PyAudio()
        CHUNK = 4 * 1024
        stream = p.open(format=p.get_format_from_width(2),
                        channels=2,
                        rate=44100,
                        output=True,
                        frames_per_buffer=CHUNK)

        while True:
            try:
                frame = self.audio_stream_socket.recv(4 * 1024)
                stream.write(frame)
            except Exception as e:
                p.terminate()
                break

    def receive_video(self):
        print("receiving video...")

        data = b""
        payload_size = struct.calcsize("Q")

        print("To quit streaming, you can click 'q' key...")

        try:
            while True:
                while len(data) < payload_size:
                    packet = self.video_stream_socket.recv(4 * 1024)  # 4K
                    if not packet: break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += self.video_stream_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow("RECEIVING VIDEO", frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            print("stream ended")
            cv2.destroyAllWindows()
            cv2.waitKey(1)
        except:
            traceback.print_exc()
            print("stream ended")
            cv2.destroyAllWindows()
            cv2.waitKey(1)
