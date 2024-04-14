import asyncio
import websockets
import mss
import json
import lzma
from ws_tools import ClientMonitorTools


def detect_screens(screens) -> list:
    screen = []
    for monitor_number, monitors in enumerate(screens.monitors[1:], start=1):
        screen.append(monitors)
    # print(screen) format like this : [{'left': 0, 'top': 0, 'width': 1280, 'height': 720}]
    return screen


async def send_images(websocket):

    tools = ClientMonitorTools()
    print(tools.get_start_time())

    with mss.mss() as sct:
        # Detect screens
        detect_screen = detect_screens(sct)
        try:
            while True:
                for scn in detect_screen:

                    # manage length of screens (remaining task)
                    # Capture the screen part
                    screenshot = sct.grab(scn)
                    if not screenshot:
                        break

                    # Send the image data to the server
                    compressed_lmza = lzma.compress(screenshot.rgb)
                    decode_image = compressed_lmza.decode("latin-1")
                    data = json.dumps({
                        'image': decode_image,
                        'status': True,
                        'size': screenshot.size,
                    })
                    await websocket.send(data)
                    recv_data = await websocket.recv()
                    print(f"receve :", recv_data)
                    await asyncio.sleep(0.7)

        except websockets.exceptions.ConnectionClosed as e:
            print("WebSocket connection closed.", e)


async def main():
    tools = ClientMonitorTools()
    USER_NAME = f"{tools.user_name()}_{tools.os_name()}_{tools.secure_token()}"
    url = f"ws://localhost:8006/ws/{USER_NAME}"
    # uri = f"wss://192.168.1.85:8088" # workin fine with IP address
    async with websockets.connect(url, ping_interval=None, ping_timeout=50) as websocket:
        print(f"Connected to {url}, user access token: {USER_NAME} ")
        await send_images(websocket)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
