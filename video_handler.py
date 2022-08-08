import socket
import threading

# testing imports
from models.user.end_user import EndUser


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
from consts import HOST, PORT, EXIT_MESSAGE


class ServerVideo:

    def __init__(self):
        self.audio_stream_socket = None
        self.video_stream_socket = None
        self.video_stream_thread = None
        self.audio_stream_thread = None

    def send(self, connection, name):
        video_stream_thread = threading.Thread(target=self.send_video, args=(connection, name))
        audio_stream_thread = threading.Thread(target=self.send_audio, args=(connection, name))
        video_stream_thread.start()
        self.video_stream_thread = video_stream_thread
        audio_stream_thread.start()
        self.audio_stream_thread = audio_stream_thread

    def receive(self, name, username, video_socket, audio_socket):
        self.initialize_vid(username, name)
        self.audio_stream_socket = audio_socket
        self.video_stream_socket = video_socket
        video_stream_thread = threading.Thread(target=self.receive_video, args=(name, ))
        audio_stream_thread = threading.Thread(target=self.receive_audio, args=(name, ))
        video_stream_thread.start()
        self.video_stream_thread = video_stream_thread
        audio_stream_thread.start()
        self.audio_stream_thread = audio_stream_thread

    def initialize_vid(self, client, name):
        Video(name, client, os.path.join(os.getcwd(), 'videos', name))

    def get_video(self, vid_name):  # todo assumes adrs from name does not use database
        return os.path.join(os.getcwd(), '../../videos', vid_name)

    def send_audio(self, connection, vid_name):  # assumes video has an audio file with the same address
        print("Sending Audio ...")
        video_path = self.get_video(vid_name)
        audio_path = video_path.replace(".mp4", ".wav")

        CHUNK = 4 * 1024
        wf = wave.open(audio_path)

        data = None
        sample_rate = wf.getframerate()

        while True:
            data = wf.readframes(CHUNK)
            if data == b'':
                break
            connection.sendall(data)
            time.sleep(0.8 * CHUNK / sample_rate)
        wf.close()

    def send_video(self, connection, vid_name):
        print("Sending Video ...")

        video_path = self.get_video(vid_name)
        try:
            while True:
                if connection:
                    vid = cv2.VideoCapture(video_path)

                    success = True
                    while success:
                        success, frame = vid.read()
                        a = pickle.dumps(frame)
                        message = struct.pack("Q", len(a)) + a
                        connection.sendall(message)
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

    def receive_audio(self, name):
        audio_path = self.get_video(name)
        wf2 = wave.open(audio_path.replace(".mp4", ".wav"), 'w')

        wf2.setnchannels(2)  # todo wf.getnchannels()
        wf2.setsampwidth(2)  # todo wf.getsampwidth()
        wf2.setframerate(44100)  # todo wf.getframerate()

        while True:
            try:
                frame = self.audio_stream_socket.recv(4 * 1024)
                self.save_audio(wf2, frame)
            except Exception as e:
                wf2.close()
                break

    def receive_video(self, name):
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
                    vid_path = os.path.join('videos', name)
                    height, width, layers = frame.shape
                    video = cv2.VideoWriter(vid_path , fourcc, 24, (width, height))  # todo fix fps, address
                    first_time = False
                self.save_video(video, frame)
            print("upload ended")
            self.end_streaming()
        except:
            traceback.print_exc()
            print("upload ended")
            self.end_streaming()

    def end_streaming(self):
        self.close_socket(self.video_stream_socket)
        self.close_socket(self.audio_stream_socket)
        time.sleep(1)

    def close_socket(self, sck: socket.socket):
        sck.send(EXIT_MESSAGE.encode())
        sck.close()


class ClientVideo:  # only should have instances in EndUser
    def __init__(self):
        self.path = os.getcwd()
        self.audio_stream_socket = None
        self.video_stream_socket = None
        self.video_stream_thread = None
        self.audio_stream_thread = None

    def send(self, audio_socket, video_socket, name):
        self.audio_stream_socket = audio_socket
        self.video_stream_socket = video_socket
        video_stream_thread = threading.Thread(target=self.send_video, args=(name, ))
        audio_stream_thread = threading.Thread(target=self.send_audio, args=(name, ))
        video_stream_thread.start()
        self.video_stream_thread = video_stream_thread
        audio_stream_thread.start()
        self.audio_stream_thread = audio_stream_thread

    def receive(self, video_stream_socket, audio_stream_socket):
        try:
            audio_stream_socket.connect((HOST, PORT))
            video_stream_socket.connect((HOST, PORT))
        except socket.error as e:
            print(f"An error occurred {str(e)}")
            exit()
        video_stream_thread = threading.Thread(target=self.receive_video)
        audio_stream_thread = threading.Thread(target=self.receive_audio)
        video_stream_thread.start()
        self.video_stream_thread = video_stream_thread
        audio_stream_thread.start()
        self.audio_stream_thread = audio_stream_thread

    def get_video(self, path):
        return os.path.join(self.path, path)

    def send_audio(self, connection, path):  # specify path from current folder
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
            self.audio_stream_socket.send(data)
            time.sleep(0.8 * CHUNK / sample_rate)
        wf.close()

    def send_video(self, connection, path):
        print("Uploading Video ...")

        video_path = self.get_video(path)
        try:
            while True:
                if connection:
                    vid = cv2.VideoCapture(video_path)

                    success = True
                    while success:
                        success, frame = vid.read()
                        a = pickle.dumps(frame)
                        message = struct.pack("Q", len(a)) + a
                        self.video_stream_socket.send(message)
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
            self.end_streaming()
        except:
            traceback.print_exc()
            print("stream ended")
            self.end_streaming()

    def end_streaming(self):
        cv2.destroyAllWindows()
        cv2.waitKey(1)
