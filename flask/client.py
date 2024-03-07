import asyncio
import websockets
import mss
import numpy as np
import cv2
import socket
import json
import uuid


def detect_screens(screens) -> list:
    screen = []
    for monitor_number, monitors in enumerate(screens.monitors[1:], start=1):
        screen.append(monitors)
    print(screen)
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

        ui_ = uuid.uuid4()

        print(ui_)
        # Create a image compress object
        image_encode_compress = [int(cv2.IMWRITE_JPEG_QUALITY), 70]

        try:
            while True:
                for scn in detect_screen:

                    # Capture the screen part
                    screenshot = sct.grab(scn)
                    if not screenshot:
                        break

                     # Convert the screenshot to a numpy array, then to bytes
                    # img_array = np.array(screenshot)
                    # frame = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
                    # _, buffer = cv2.imencode(
                    #     '.jpg', frame, image_encode_compress)
                    # array_to_bytes = buffer.tobytes()

                    # Send the image data to the server
                    # bytes_ = screenshot.raw
                    await websocket.send(json.dumps({"frames": str(screenshot)}))
                    recv_data = await websocket.recv()
                    # print(f"receve :", recv_data)
                    # await asyncio.sleep(0.08)
                    await asyncio.sleep(2)

        except websockets.exceptions.ConnectionClosed as e:
            print("WebSocket connection closed.", e)

        finally:
            cv2.destroyAllWindows()


async def main():
    url = "ws://localhost:8005"
    # url = f"ws://localhost:8005/"
    # uri = f"ws://localhost:8000/ws/video/"
    # uri = f"wss://192.168.1.85:8088" # workin fine with IP address
    user_id = str(uuid.uuid4())  # Generate unique user ID
    async with websockets.connect(url, headers={'user_id': user_id}, ping_interval=None, ping_timeout=50) as websocket:
        print(f"Connected to {url}, Local system IP address ")

        # Send images continuously to the server
        await send_images(websocket)


if __name__ == "__main__":
    # Run the WebSocket client
    asyncio.get_event_loop().run_until_complete(main())
