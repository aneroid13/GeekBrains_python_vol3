from socket import *
import json
import time
import random
import argparse
import threading
import pymongo
from client_log_config import logger_cl as log
from kivy.app import App


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


class DBmongo:
    def __init__(self, addr):
        self.db_path = addr
        self.conn = pymongo.MongoClient(self.db_path)
        self.db = self.conn['jim_db']

    def get_allusers(self):
        coll = self.db['users']
        return coll.find()

    def end(self):
        return self.conn.close()


class JIMClient:
    def __init__(self, addr="localhost", port=7777, chat=None):
        self.JIMAddress = addr
        self.JIMPort = port
        self.data = None
        self.username = None
        self.userlogin = False
        self.socket = None
        self.kivy_chat = chat

    def get_time(self):
        return time.time()

    def get_random_nik(self):
        may_be = ["Tomas", "Jeremy", "Mike", "Donald"]
        name = random.choice(may_be)
        nikname = name + "_" + str(time.thread_time_ns())[2:5]
        return nikname

    def user_presence(self, username, status):
        self.username = username
        template_user_present = {
                "action": "presence",
                "time": self.get_time(),
                "type": "status",
                "user": {
                        "account_name": username,
                        "status": status
                        }
                }

        #JIMMSG = "Hallou !"
        JIMMSG = json.dumps(template_user_present)
        log.debug(JIMMSG.encode("utf-8"))

        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.JIMAddress, self.JIMPort))
            self.socket.send(JIMMSG.encode("utf-8"))
        except error as ex:
            log.error("Error %s", ex)

    @threaded
    def send_message(self, to, msg):
        template_chat_message = {
            "action": "msg",
            "time": self.get_time(),
            "to": to,
            "from": self.username,
            "message": msg
        }

        JIMMSG = json.dumps(template_chat_message)
        log.debug(JIMMSG.encode("utf-8"))

        try:
            self.socket.send(JIMMSG.encode("utf-8"))
        except error as ex:
            log.error("Error %s", ex)

    @threaded
    def receive(self):
        while True:
            try:
                self.data = None
                self.data = self.socket.recv(1000000).decode("utf-8")
                if self.data != '':
                    self.data = str.replace(self.data, "}{", "}&&{")
                    for each in str.split(self.data, "&&"):
                        self.srv_answer(each)
            except error as ex:
                log.error("Error %s", ex)

    def srv_answer(self, giveme_data):
        try:
            JIMANSW = json.loads(giveme_data)
        except (json.JSONDecodeError, TypeError):
            #log.warning(f"Incorrect server answer: {self.data}")
            JIMANSW = "Incorrect"

        if JIMANSW is not "Incorrect":
            status_code = int(JIMANSW.get('response'))
            log.debug(f"Code: {status_code}")

            if status_code < 400:
                if status_code == 100:
                    self.kivy_chat.insert_text(str(JIMANSW.get('alert')).rstrip("|#mainchat|") + "\n")
                    log.debug(f"Message: {JIMANSW.get('alert')}")
                if status_code == 200:
                    log.debug(f"User connect : {JIMANSW.get('alert')}")
                    self.userlogin = True
            else:
                log.error(f"User connect failed : {JIMANSW.get('error')}")
                self.userlogin = False

def get_args():
    parser = argparse.ArgumentParser(
        description='JIM Server can be started on custom address and port'
    )
    parser.add_argument('-a', '--address', default="0.0.0.0", type=str, required=False, action='store', help='Input ip address')
    parser.add_argument('-p', '--port', default=7777, type=int, required=False, action='store', help='Input port')
    parser.add_argument('-db', '--db_path', default='mongodb://localhost:27017/', type=str, required=False, action='store', help='Path to connect database')
    return parser.parse_args()


class MyApp(App):
    title = "JIM Chat messenger"

    # def __init__(self):
    #     super().__init__()

    def on_start(self):
        self.root.ids['user_input'].bind(on_text_validate=self.enter_message)
        self.root.ids['send_msg'].bind()
        self.get_users()

        self.runJIMrun = JIMClient(
            str(get_args().address),
            int(get_args().port),
            self.root.ids['text_mainchat']
            )
        self.runJIMrun.user_presence(self.runJIMrun.get_random_nik(), "Haaaiii!!!")
        self.runJIMrun.receive()

    def get_users(self):
        dbmongo = DBmongo(get_args().db_path)

        users = ""
        for user in dbmongo.get_allusers():
            users = users + user['user'] + "\n"

        self.root.ids['text_users'].text = users

    def buttonpress(self):
        uinput = self.root.ids['user_input']
        chatname = "#mainchat"
        self.runJIMrun.send_message(chatname, uinput.text)
        uinput.text = ""


    def enter_message(self, instance):
        chatname = "#mainchat"
        self.runJIMrun.send_message(chatname, instance.text)
        instance.text = ""

if __name__ == "__main__":
    MyApp().run()
