import cmd
from io import StringIO

import os
from time import time, sleep
from database.video_db_service import VideoDBService
from models.video.video import Video
from services.ticket_service import TicketService
from socket import socket

from services.user_service import UserService
from consts import DB_CONFIG, VIDEO_FOLDER_ADDRESS
from services.ticket_service import TicketService
from services.user_service import UserService
from services.video_service import VideoService
from video_handler import ClientVideo, ServerVideo


class ClientCommandHandler(cmd.Cmd):
    INVALID_ARGS = f'invalid arguments'
    NOT_LOGGED_IN = f'You are not logged in!'
    prompt = '(youtube) '

    user_service = UserService()
    ticket_service = TicketService()

    video_server_service = ServerVideo()
    video_client_service = ClientVideo()
    video_service = VideoService()
    video_db_service = VideoDBService(DB_CONFIG)


    def do_help(self, arg: str) -> str:
        'help or ?'
        help_output = StringIO()
        super().__setattr__('stdout', help_output)
        super().do_help(arg)
        return help_output.getvalue()

    def do_login(self, arg):
        'login [username] [password]'
        args = parse(arg)
        if len(args) < 2:
            return ClientCommandHandler.INVALID_ARGS
        return ClientCommandHandler.user_service.get_end_user(username=args[0], password=args[1])

    def do_whoami(self, arg):
        'whoami'
        user = self.user_service.user
        return user.username if user else 'No one is logged in'


    def do_logout(self, arg):
        'logout'
        self.user_service.logout()
        return f'logout successfull.'
    
    def do_signup(self, arg):
        'signup [username] [password]'
        args = parse(arg)
        if len(args) < 2:
            return ClientCommandHandler.INVALID_ARGS
        ClientCommandHandler.user_service.create_end_user(args[0], args[1])
        return f'signup successfull. Admin permission is needed.'

    def do_ticket(self, arg):
        'ticket [text]'
        if not self.user_service.user:
            return ClientCommandHandler.NOT_LOGGED_IN
        args = parse(arg)
        result = self.ticket_service.create_ticket(self.user_service.user.username, args[0])
        return result

    def do_set_ticket_state(self, arg):
        'set_ticket_state [ticketid] [state]'
        if not self.user_service.user:
            return ClientCommandHandler.NOT_LOGGED_IN
        args = parse(arg)
        result = self.ticket_service.set_ticket_state(args[0], args[1], self.user_service.user.username)
        return result

    def do_my_tickets(self, arg):
        'my_tickets'
        if not self.user_service.user:
            return ClientCommandHandler.NOT_LOGGED_IN
        args = parse(arg)
        result = self.ticket_service.get_all_user_tickets(self.user_service.user.username)
        return result
    
    def do_upload(self, arg):
        'upload [name]'
        # 'upload [name] [ip] [video_port] embedded in client code
        args = parse(arg)
        user = self.user_service.user
        if not user:
            return ClientCommandHandler.NOT_LOGGED_IN
        if len(args) != 3:
            return ClientCommandHandler.INVALID_ARGS
        print(user.strikes)
        if int(user.strikes) >= 2:
            return f'Unable to upload video due to strikes'
        ip, video_port = args[1], int(args[2])
        audio_port = video_port + 1
        video_socket = socket()
        video_socket.connect((ip, video_port))
        audio_socket = socket()
        audio_socket.connect((ip, audio_port))
        title = args[0].split("/")[-1]
        try:
            video = Video(title, user.username, os.path.join(VIDEO_FOLDER_ADDRESS, title))
            print("video created")
            self.video_db_service.create_video(video)
            print("done inserting to the db.")
        except:
            return "Error while uploading (possibly duplicate title)"
        print("uploading ...")
        self.video_server_service.receive(title=title, video_socket=video_socket, audio_socket=audio_socket)
        return "Upload successful"

    def do_watch(self, arg):
        'watch [name]'
        # 'upload [name] [ip] [video_port] embedded in client code
        args = parse(arg)
        ip, video_port = args[1], int(args[2])
        audio_port = video_port + 1
        video_socket = socket()
        video_socket.connect((ip, video_port))
        audio_socket = socket()
        audio_socket.connect((ip, audio_port))
        title = args[0].split("/")[-1]
        
        try:
            video = self.video_db_service.get_video(title)
            print("video adrs:", video.adrs)
        except:
            return "Video not found!"
        self.video_server_service.send(path=video.adrs, video_socket=video_socket, audio_socket=audio_socket)

        sleep(1)
        self.video_server_service.video_lock.acquire()
        self.video_server_service.video_lock.release()
        self.video_server_service.audio_lock.acquire()
        self.video_server_service.audio_lock.release()
        return "End of the video."
    
    def do_like(self, arg):
        'like [video_title]'
        args = parse(arg)
        user = self.user_service.user
        if not user:
            return ClientCommandHandler.NOT_LOGGED_IN
        if len(args) != 1:
            return ClientCommandHandler.INVALID_ARGS
        return self.video_service.like(args[0])
    
    def do_dislike(self, arg):
        'dislike [video_title]'
        args = parse(arg)
        user = self.user_service.user
        if not user:
            return ClientCommandHandler.NOT_LOGGED_IN
        if len(args) != 1:
            return ClientCommandHandler.INVALID_ARGS
        return self.video_service.dislike(args[0])
    
    def do_add_comment(self, arg):
        'add_comment [video_title] [comment_text]'
        args = parse(arg)
        user = self.user_service.user
        if not user:
            return ClientCommandHandler.NOT_LOGGED_IN
        if len(args) < 1:
            return ClientCommandHandler.INVALID_ARGS
        comment = " ".join(args[1:])
        return self.video_service.add_comment(video_title=args[0], user=user.username, comment=comment)

    def do_video_info(self, arg):
        'video_info [video_title]'
        args = parse(arg)
        user = self.user_service.user
        if len(args) != 1:
            return ClientCommandHandler.INVALID_ARGS
        return self.video_service.get_video(args[0])    

    def do_video_labels(self, arg):
        'video_labels [video_title]'
        args = parse(arg)
        user = self.user_service.user
        if len(args) != 1:
            return ClientCommandHandler.INVALID_ARGS
        return self.video_service.get_video_labels(args[0])        

    def do_exit(self, arg):
        'type q to exit'
        return ''

class ProxyCommandHandler(cmd.Cmd):
    INVALID_ARGS = f'invalid arguments'
    prompt = '(turtle) '
    user_service = UserService()
    ticket_service = TicketService()
    video_service = VideoService()

    def set_user(self, username):
        self.user_service.set_proxy_user(username=username)
    
    def do_permissions(self, arg):
        'permissions'
        # 'permissions [admin]' admin is embedded in app
        args = parse(arg)
        self.set_user(args[-1])
        unapproved_users = self.user_service.get_unapproved_users()
        return f'here is the signup permission list:\n {unapproved_users}' if unapproved_users else 'there is no unapproved user'

    def do_approve(self, arg):
        'approve [username]'
        # 'approve [username] [admin]' admin is embedded in app
        args = parse(arg)
        if len(args) < 2:
            return self.INVALID_ARGS
        self.set_user(args[-1])
        return self.user_service.approve(args[0])

    def do_ticket(self, arg):
        'ticket [text]'
        # 'ticket [text] [admin]' admin is embedded in app
        args = parse(arg)
        if len(args) < 2:
            return self.INVALID_ARGS
        self.set_user(args[-1])
        text = " ".join(args[:-1])
        # assignee is None, so its superuser
        result = self.ticket_service.create_ticket(username=args[-1], text=text, assignee="manager")
        return result

    def do_reply_ticket(self, arg):
        'reply_ticket [ticketid] [text]'
        # 'reply_ticket [ticketid] [text] [admin]' admin is embedded in app
        args = parse(arg)
        if len(args) < 3:
            return self.INVALID_ARGS
        self.set_user(args[-1])
        text = " ".join(args[1:-1])
        result = self.ticket_service.reply_to_ticket(ticket_id=args[0], reply_text=text, username=args[-1])
        return result

    def do_set_ticket_state(self, arg):
        'set_ticket_state [ticketid] [state]'
        # 'set_ticket_state [ticketid] [state] [admin]' admin is embedded in app
        args = parse(arg)
        if len(args) < 3:
            return self.INVALID_ARGS
        if args[1] not in ["NEW", "PENDING", "RESOLVED", "CLOSED"]:
            return self.INVALID_ARGS
        self.set_user(args[-1])
        result = self.ticket_service.set_ticket_state(ticket_id=args[0], state=args[1], user=args[-1])
        return result

    def do_open_tickets(self, arg):
        'open_tickets'
        # 'open_tickets [admin]' admin is embedded in app
        args = parse(arg)
        self.set_user(args[-1])
        result = self.ticket_service.get_all_open_tickets()
        return result

    def do_label(self, arg):
        'label [video_title] [text]'
        # 'label [video_title] [text] [admin]' admin is embedded in app
        args = parse(arg)
        if len(args) != 3:
            return ClientCommandHandler.INVALID_ARGS
        self.set_user(args[-1])
        return self.video_service.label(args[0], args[1])
    
    def do_remove(self, arg):
        'remove [video_title]'
        # 'remove [video_title] [admin]' admin is embedded in app
        args = parse(arg)
        if len(args) != 2:
            return ClientCommandHandler.INVALID_ARGS
        self.set_user(args[-1])
        username = self.video_service.get_video_owner(args[0])
        
        return f'{self.video_service.remove_video(args[0])}\n{self.user_service.add_strike(username=username)}'

    def do_unstrike(self, arg):
        'unstrike [username]'
        # 'unstrike [username] [admin]' admin is embedded in app
        args = parse(arg)
        if len(args) != 2:
            return ClientCommandHandler.INVALID_ARGS
        self.set_user(args[-1])
        return self.user_service.unstrike_user(args[0])

def parse(arg):
    return arg.split()
