from socket import *
import json
import time
from datetime import datetime
import argparse
import select
import asyncio
from queue import Queue
from threading import Thread
from server_log_config import logger_srv as log
###from databases import Database
import sqlite3
import pymongo


class SenderThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_queue = Queue()

    def send(self, item):
        self.input_queue.put(item)

    def close(self):
        self.input_queue.put(None)
        self.input_queue.join()

    def run(self):
        while True:
            item = self.input_queue.get()
            if item is None: break

            client, msg = item

            log.info(f"Server send to: {client['ip']}; User: {client['name']}; Message:{msg}")
            try:
                client['socket'].send(msg)
            except error as er:
                log.error(f"Error: {er}")
                client['socket'].close()

            self.input_queue.task_done()

        self.input_queue.task_done()
        return


class DBsqlite:
    def __init__(self, addr):
        self.db_path = addr
        self.conn = sqlite3.connect(self.db_path)
        self.db = self.conn.cursor()
        self.create_chat_table()
        self.create_users_table()

    def create_chat_table(self):
        query = "CREATE TABLE if not exists mainchat (id INTEGER PRIMARY KEY, " \
                                        "date DATETIME, " \
                                        "username VARCHAR(100), " \
                                        "msg VARCHAR(10000))"
        self.db.execute(query)

    def create_users_table(self):
        query = "CREATE TABLE if not exists users (id INTEGER PRIMARY KEY, " \
                                     "date DATETIME, " \
                                     "username VARCHAR(100), " \
                                     "status VARCHAR(1000), " \
                                     "ip VARCHAR(100))"
        self.db.execute(query)

    def add_mainchat_message(self, user: str, msg: str):
        dt = datetime.now().strftime('%b %d %Y %I:%M%p')
        q = "INSERT INTO mainchat (date, username, msg) VALUES (?, ?, ?)"
        v = [(dt, user, msg)]
        self.db.executemany(q, v)
        self.conn.commit()

    def add_user(self, user: str, status: str):
        dt = datetime.now().strftime('%b %d %Y %I:%M%p')
        q = "INSERT INTO users (date, username, status) VALUES (?, ?, ?)"
        v = [(dt, user, status)]
        self.db.executemany(q, v)
        self.conn.commit()

    def get_chat_allmgs(self):
        query = "SELECT * FROM mainchat"
        return self.db.execute(query)

    def end(self):
        return self.conn.close()


class DBmongo:
    def __init__(self, addr):
        self.db_path = addr
        self.conn = pymongo.MongoClient(self.db_path)
        self.db = self.conn['jim_db']
    #    self.create_chat_table()       #  Create automatically
    #    self.create_users_table()      #  Create automatically

    def create_chat_table(self):
        query = "db.createCollection('mainchat')"
        self.db.execute(query)

    def create_users_table(self):
        query = "db.createCollection('users')"
        self.db.execute(query)

    def add_mainchat_message(self, user: str, msg: str):
        coll = self.db['mainchat']
        dt = datetime.now().strftime('%b %d %Y %I:%M%p')
        q = {"date": dt, "user": user, "msg": msg}
        coll.insert_one(q)

    def add_user(self, user: str, status: str):
        coll = self.db['users']
        dt = datetime.now().strftime('%b %d %Y %I:%M%p')
        q = {"date": dt, "user": user, "status": status}
        coll.insert_one(q)

    def update_user(self, user: str, status: str):
        coll = self.db['users']
        dt = datetime.now().strftime('%b %d %Y %I:%M%p')
        q = {"user": user}
        v = {"$set": {"date": dt, "status": status}}
        coll.update_one(q, v)

    def get_chat_allmgs(self):
        coll = self.db['mainchat']
        return coll.find()

    def end(self):
        return self.conn.close()


class JIMServer:
    def __init__(self, db_path: str, addr: str = "localhost", port: int = 7777):
        self.JIMAddress = addr
        self.JIMPort = port
        self.db = DBmongo(db_path)
        self.srv_socket = None
        self.clients = []
        self.to_clients = SenderThread()
        self.textanswers = {
            100: "Message",
            101: "Warning",
            200: "OK!",
            201: "Object created.",
            202: "Accepted",
            400: "Wrong request or JSON",
            401: "Not authorized",
            402: "Wrong login or password",
            403: "Forbidden",
            404: "User not found",
            405: "Conflict. Already connected.",
            410: "User offline",
            500: "Server error, something goes wrong."
        }

    def srv_poll(self, mask, timeout):
        poller = select.poll()
        poller.register(self.srv_socket.fileno(), mask)
        return poller.poll(int(timeout * 1000))

    def clinet_poll(self, sock, timeout):
        poller = select.poll()
        poller.register(sock.fileno(), select.POLLIN | select.POLLPRI)
        return poller.poll(int(timeout * 1000))

    def read_events(self, socket):
        if socket is self.srv_socket:
            newsocket, ip = socket.accept()
            newsocket.setblocking(0)
            fd_to_socket = {self.srv_socket.fileno(): self.srv_socket, }
            fd_to_socket[newsocket.fileno()] = newsocket
            poller = select.poll()
            poller.register(newsocket, select.POLLIN | select.POLLPRI)

            socket = newsocket

        data = socket.recv(1000000)
        data = data.decode('utf-8')
        user, code, action, status = self.check_message(data)

        # New user coming
        if action == "presence":
            new_client = {'name': user, 'status': status, 'socket': socket, 'ip': ip[0], 'port': ip[1]}
            self.clients.append(new_client)
            self.db.add_user(user, status)
            self.answer(new_client, code, self.textanswers[code])
            for db_msg in self.db.get_chat_allmgs():
                self.answer(new_client, 100, f"|#mainchat| {db_msg['user']}: {db_msg['msg']}")

        if action == "msg":
            for client in self.clients:
                if client['name'] == user:
                    # client['socket'] = socket
                    # client['ip'], client['port'] = ip
                    self.answer(client, code, self.textanswers[code])

    def newmessage_events(self, socket, client):
        data = socket.recv(1000000)
        data = data.decode('utf-8')
        if data != None:
            data = str.replace(data, "}{", "}&&{")
            for each in str.split(data, "&&"):
                user, code, action, status = self.check_message(each)
                self.answer(client, code, self.textanswers[code])

    def error_events(self, socket):
        log.error("Connection refused or client disconnected")
        select.poller.unregister(socket)
        socket.close()

    def init_server(self):
        self.srv_socket = socket(AF_INET, SOCK_STREAM)
        #self.srv_socket.setblocking(0)
        self.srv_socket.bind((self.JIMAddress, self.JIMPort))
        self.srv_socket.listen(5)

        self.to_clients.start()  # <- New thread coming

    def listen(self):
        while True:
            try:
                events_in = self.srv_poll(select.POLLIN | select.POLLPRI, 1)
                events_err = self.srv_poll(select.POLLERR | select.POLLHUP, 1)

                fd_to_socket = {self.srv_socket.fileno(): self.srv_socket, }

                for fd, flag in events_in:
                    soc = fd_to_socket[fd]
                    self.read_events(soc)

                for fd, flag in events_err:
                    soc = fd_to_socket[fd]
                    self.error_events(soc)

                for client in self.clients:
                    if client['socket'].fileno() != -1:
                        event_client = self.clinet_poll(client['socket'], 1)
                        fd_to_socket = {client['socket'].fileno(): client['socket'], }

                        for fd, flag in event_client:
                            soc = fd_to_socket[fd]
                            self.newmessage_events(soc, client)
                    else:
                        self.clients.remove(client)

            except error as ex:
                log.error("Error %s", ex)

    def get_time(self):
        return time.time()

    def answer(self, client, code, msg):

        if code >= 400:
            msgtype = "error"
        else:
            msgtype = "alert"

        template_server_answer = {
            "response": str(code),
            "time": self.get_time(),
            msgtype: str(msg)
                }

        JIMMSG = json.dumps(template_server_answer)
        JIMMSG = JIMMSG.encode("utf-8")
        log.debug("Server answer : %s", JIMMSG)
        self.to_clients.send((client, JIMMSG))

    def check_message(self, data):
        code = 200
        jimrec = user = status = action = None

        try:
            jimrec = json.loads(data)

            if jimrec.get("action") is None or jimrec.get("time") is None:
                code = 400

        except json.JSONDecodeError:
            code = 400

        if code == 200:
            action = jimrec.get("action")
            if action == "presence":
                user = jimrec.get("user")['account_name']
                status = jimrec.get("user")['status']

            elif action == "msg":
                user = jimrec.get("from")
                for_who = jimrec.get("to")
                message = jimrec.get("message")

                if for_who[0] == "#":
                    for client in self.clients:
                        self.answer(client, 100, f"|{for_who}| {user}: {message}")
                        self.db.add_mainchat_message(user, message)
                else:
                    for client in self.clients:
                        if client['name'] == for_who:
                            self.answer(client, 100, f"{user}: {message}")

        log.info(f"User: {user}, Message:{data}")

        return user, code, action, status


def get_args():
    parser = argparse.ArgumentParser(
        description='JIM Server can be started on custom address and port'
    )
    parser.add_argument('-a', '--address', default="0.0.0.0", type=str, required=False, action='store', help='Input ip address')
    parser.add_argument('-p', '--port', default=7777, type=int, required=False, action='store', help='Input port')
    parser.add_argument('-db', '--db_path', default='mongodb://localhost:27017/', type=str, required=False, action='store', help='Path to connect database')

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    runJIMrun = JIMServer(
        db_path=args.db_path,
        addr=args.address,
        port=args.port
    )

    runJIMrun.init_server()
    runJIMrun.listen()
