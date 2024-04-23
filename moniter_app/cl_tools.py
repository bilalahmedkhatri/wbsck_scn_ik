import datetime
import time
from psutil import boot_time
from secrets import token_urlsafe
from time import time
from sys import platform
from os import environ
from platform import system


class ClientMonitorTools:

    def __init__(self, *args, **kwargs):
        self.START_TIME = time()
        self.USER_NAME = None

    def username(self) -> str:  # done
        return environ["USERNAME"] if platform.startswith(
            'win') else environ["USER"]

    def os_name(self) -> str:  # done
        try:
            return system()
        except:
            return False

    def secure_token(self):
        try:
            securetoken = token_urlsafe()
            return securetoken
        except:
            return False

    def get_sys_started_start(self):
        try:
            start_time = boot_time()
            conv_date_format = datetime.datetime.fromtimestamp(
                start_time).strftime("%d/%m/%Y, %H:%M:%S")
            return (start_time, conv_date_format)
        except:
            return False

    def extra_header_data(self) -> dict:
        return {
            'x-user-name': self.username(),
            'x-os': self.os_name(),
            'x-system-started-time': self.get_sys_started_start()
        }
