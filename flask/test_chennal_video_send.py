import asyncio
import websockets
import mss
import numpy as np
import cv2
import socket
import base64


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

        # Create a image compress object
        image_encode_compress = [int(cv2.IMWRITE_JPEG_QUALITY), 70]

        try:
            while True:
                for scn in detect_screen:

                    # Capture the screen part
                    screenshot = sct.grab(scn)
                    if not screenshot:
                        break

                    print('data type : ', screenshot.__str__())
                    # img_bytes = screenshot.encode('ascii')

                    # # Convert the screenshot to a numpy array, then to bytes
                    # img_array = np.array(screenshot)
                    # frame = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
                    # _, buffer = cv2.imencode(
                    #     '.jpg', frame, image_encode_compress)
                    # array_to_bytes = buffer.tobytes()

                    # Send the image data to the server
                    await websocket.send(screenshot)
                    # await websocket.send("tets")
                    await asyncio.sleep(0.08)

                    print(type(screenshot))

        except websockets.exceptions.ConnectionClosed as e:
            print("WebSocket connection closed.", e)

        finally:
            cv2.destroyAllWindows()


async def main():
    uri = f"ws://0.0.0.0:8005"
    # uri = f"ws://localhost:8000/ws/video/"
    # uri = f"wss://192.168.1.85:8088" # workin fine with IP address

    async with websockets.connect(uri, ping_interval=None) as websocket:
        print(f"Connected to {uri}, {get_system_ip()}")

        # Send images continuously to the server
        await send_images(websocket)


if __name__ == "__main__":
    # Run the WebSocket client
    asyncio.get_event_loop().run_until_complete(main())
