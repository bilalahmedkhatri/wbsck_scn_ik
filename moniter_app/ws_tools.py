import datetime
import time
import socket
from psutil import boot_time
from secrets import token_urlsafe
from time import time
from sys import platform
from os import environ, getlogin
from platform import system


class ClientMonitorTools:

    def get_start_time(self):
        return time()

    def get_system_ip(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = sock.connect(("8.8.8.8", 80))
        sock.close()
        return ip

    def get_username(self) -> None:
        self.USER_NAME = environ["USERNAME"] if platform.startswith(
            'win') else environ["USER"]

    def os_name(self) -> str:
        try:
            return system()
        except:
            return False

    def user_name(self) -> str:
        try:
            return getlogin()
        except:
            return False

    def secure_token(self):
        try:
            return token_urlsafe()
        except:
            return False

    def get_sys_start(self):
        try:
            start_time = boot_time()
            conv_date_format = datetime.datetime.fromtimestamp(
                start_time).strftime("%d/%m/%Y, %H:%M:%S")
            return conv_date_format
        except:
            return False
