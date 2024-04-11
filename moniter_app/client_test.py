import asyncio
import websockets
import mss
import socket
import json
import lzma
from os import environ
from sys import platform
from time import time
import BytesIO
import base64


class ClientMonitor:

    def __init__(self, host='0.0.0.0', ip=8001) -> None:
        self.host = host
        self.ip = ip

    def screenshot(self):
        with mss.mss() as scn:
            img = scn.grab(scn.monitors[0])
        return img

    def img_serializer(self):
        scn = self.screenshot()
        buffer = BytesIO()
        scn.save(buffer, format="jpeg")
        data_string = base64.b64encode(buffer.getvalue())
        return data_string


result = ClientMonitor()
print(result.img_serializer())
