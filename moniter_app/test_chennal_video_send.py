import asyncio
import websockets
import mss
import numpy as np
import cv2
import socket
import base64
import io


def detect_screens(screens) -> list:
    screen = []
    for monitor_number, monitors in enumerate(screens.monitors[1:], start=1):
        screen.append(monitors)
    return screen


def get_system_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()
    s.close()
    return ip


async def send_images(websocket):

    with mss.mss() as sct:
        # Detect screens
        detect_screen = detect_screens(sct)

        try:
            while True:
                for scn in detect_screen:

                    # Capture the screen part
                    screenshot = sct.grab(scn)
                    if not screenshot:
                        break

                    # print(type(screenshot.raw))
                    # pickle dekna hai.
                    # nn = np.array(screenshot.raw)
                    # nnp = np.array(screenshot)
                    # print(nn.shape)
                    # print(nnp.shape)

                    await websocket.send(screenshot.raw)

                    await asyncio.sleep(0.08)

        except websockets.exceptions.ConnectionClosed as e:
            print("WebSocket connection closed.", e)


async def main():
    uri = f"ws://0.0.0.0:8005"
    # uri = f"ws://localhost:8000/ws/video/"
    # uri = f"wss://192.168.1.85:8088" # workin fine with IP address

    async with websockets.connect(uri, ping_interval=None, compression='deflate') as websocket:
        print(f"Connected to {uri}, {get_system_ip()}")

        # Send images continuously to the server
        await send_images(websocket)


if __name__ == "__main__":
    # Run the WebSocket client
    asyncio.get_event_loop().run_until_complete(main())


# bytes['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'removeprefix', 'removesuffix', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill'] ['_ScreenShot__pixels', '_ScreenShot__rgb', '__array_interface__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', 'bgra', 'from_size', 'height', 'left', 'pixel', 'pixels', 'pos', 'raw', 'rgb', 'size', 'top', 'width']
