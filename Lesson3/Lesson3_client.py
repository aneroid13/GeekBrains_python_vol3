from socket import *
import json
import time
import random
import argparse
import threading
import asyncio
from client_log_config import logger_cl as log


# def threaded(fn):
#     def wrapper(*args, **kwargs):
#         thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
#         thread.start()
#         return thread
#     return wrapper

class JIMClient:
    def __init__(self, addr="localhost", port=7777):
        self.JIMAddress = addr
        self.JIMPort = port
        self.data = None
        self.username = None
        self.userlogin = False
        self.sender = None

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
        return JIMMSG.encode("utf-8")

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
        self.sender.write(JIMMSG.encode("utf-8"))

#    @threaded
    async def type_message(self, chatname):
        while True:
            data = input(f'{chatname}> ')
            if data == 'exit':
                break
            self.send_message(chatname, data)
            await asyncio.sleep(0.1)

#    @threaded
    async def network_io(self):
        self.data = None
        try:
            # Connect and user login
            reader, writer = await asyncio.open_connection(self.JIMAddress, self.JIMPort)  # async socket connection
            self.sender = writer
            self.sender.write(runJIMrun.user_presence(self.get_random_nik(),
                                                      "I am using JIM Messenger !"))   # Login new user
            print("You are connected to server.")
            print("Remeber! you are: " + self.username)

            # Constantly receive new messages
            while True:
                self.data = (await reader.read(1000)).decode("utf-8")
                if self.data != '':
                    self.data = str.replace(self.data, "}{", "}&&{")
                    for each in str.split(self.data, "&&"):
                        self.srv_answer(each)

            self.sender.close()
        except asyncio.CancelledError:
            log.info("Connection.run was cancelled")
        except ConnectionResetError as ex:
            log.warning(f"Connection was reset: {ex}")
        except error as ex:
            log.error(f"Error receive data: {ex}")

    def srv_answer(self, giveme_data):
        try:
            JIMANSW = json.loads(giveme_data)
        except (json.JSONDecodeError, TypeError):
            log.warning(f"Incorrect server answer: {self.data}")
            JIMANSW = "Incorrect"

        if JIMANSW is not "Incorrect":
            status_code = int(JIMANSW.get('response'))
            log.debug(f"Code: {status_code}")

            if status_code < 400:
                if status_code == 100:
                    print(JIMANSW.get('alert'))
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
    parser.add_argument('-a', '--address', default="0.0.0.0", required=False, action='store', help='Input ip address')
    parser.add_argument('-p', '--port', default=7777, required=False, action='store', help='Input port')
    return parser.parse_args()


async def run_async_tasks():
    task_network_io = asyncio.create_task(runJIMrun.network_io())
    task_input_main = asyncio.create_task(runJIMrun.type_message("#mainroom"))
    await task_network_io
    await task_input_main

if __name__ == "__main__":
    runJIMrun = JIMClient(
        str(get_args().address),
        int(get_args().port)
    )

    asyncio.run(run_async_tasks())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(runJIMrun.network_io(), runJIMrun.type_message("#mainroom")))
