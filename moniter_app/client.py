import asyncio
import websockets
import mss
import socket
import json
import lzma
from os import environ
from sys import platform
from time import time


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


def detect_screens(screens) -> list:
    screen = []
    for monitor_number, monitors in enumerate(screens.monitors[1:], start=1):
        screen.append(monitors)
    print(screen)
    return screen


async def send_images(websocket):

    with mss.mss() as sct:
        # Detect screens
        detect_screen = detect_screens(sct)
        try:
            while True:
                for scn in detect_screen:

                    # Capture the screen part
                    screenshot = sct.grab(scn)
                    # sct.close()
                    print(sct)
                    if not screenshot:
                        break

                    print(screenshot.size)

                    # Send the image data to the server
                    compressed_lmza = lzma.compress(screenshot.rgb)
                    decode_image = compressed_lmza.decode("latin-1")
                    data = json.dumps({
                        'image': decode_image,
                        'status': True,
                        'size': screenshot.size
                    })
                    await websocket.send(data)
                    recv_data = await websocket.recv()
                    print(f"receve :", recv_data)
                    await asyncio.sleep(0.7)

        except websockets.exceptions.ConnectionClosed as e:
            print("WebSocket connection closed.", e)


async def main():
    url = "ws://localhost:8006"
    # uri = f"wss://192.168.1.85:8088" # workin fine with IP address
    async with websockets.connect(url, ping_interval=None, ping_timeout=50) as websocket:
        print(f"Connected to {url}, Local system IP address ")
        await send_images(websocket)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
