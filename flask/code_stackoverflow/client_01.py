import websockets
import json
from termcolor import colored
# from classes import File


class Manager:
    SERVER_URL = None
    filename = None
    filesize = 0
    secret = None
    # FileManager = File.Manager()

    def __init__(self, SERVER_URL, filename, filesize, secret):
        self.SERVER_URL = SERVER_URL
        self.filename = filename
        self.filesize = filesize
        self.secret = secret

        # Initialize FileManager
        self.FileManager.secret = self.secret
        self.FileManager.filesize = self.filesize
        self.FileManager.filename = self.filename

    async def start_sender(self):
        async with websockets.connect(self.SERVER_URL) as ws:
            self.FileManager.ws = ws
            await ws.send(json.dumps({"cmd": "sender_init", "key": self.secret}))
            print("Now in the receiver computer", end=" "), print(
                colored("sendpai " + self.secret, "magenta"))
            while True:
                message = await ws.recv()
                deserialized = json.loads(message)
                cmd = deserialized["cmd"]
                if cmd == "receiver_request":
                    await self.FileManager.start_sending()
                elif cmd == "receiver_init":
                    await ws.send(json.dumps({"cmd": "file_details", "key": self.secret, "filename": self.filename, "filesize": self.filesize}))

    async def start_receiver(self):
        async with websockets.connect(self.SERVER_URL) as ws:
            self.FileManager.ws = ws
            await ws.send(json.dumps({"cmd": "receiver_init", "key": self.secret}))
            while True:
                message = await ws.recv()
                deserialized = json.loads(message)
                if "cmd" in deserialized:
                    cmd = deserialized["cmd"]
                    if cmd == "send":
                        if "data" in deserialized:
                            binary_chunk = bytes(
                                deserialized["data"], encoding="utf-8")
                            await self.FileManager.chunk_receiver(binary_chunk)
                    elif cmd == "file_details":
                        self.FileManager.filename = deserialized["filename"]
                        self.FileManager.filesize = deserialized["filesize"]
                        self.FileManager.open_file("hello", "wb")
                        await ws.send(json.dumps({"cmd": "receiver_request", "key": self.secret}))
                        print("[The file is about to be downloaded]")
                        print(
                            "filename: " + colored(str(self.FileManager.filename), "green"), end=" ")
                        print(
                            "filesize: " + colored(str(self.FileManager.filesize / 1000) + "mb", "yellow"))
