import asyncio
import websockets
import numpy
import cv2
import socket
import numpy as np
import base64


async def build_video():
    pass


def get_system_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()
    s.close()
    return ip


async def server(websocket, path):
    print(f"Client connected: {websocket.remote_address}")

    # Set the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_video.avi', fourcc, 30.0, (640, 480))
    # ip_, port_ = websocket.remote_address
    # print(f"Client connected: {ip_}:{port_}")
    # Open the stream
    try:
        while True:
            # Continuously listen for messages from the client
            async for message in websocket:

                # Convert the screenshot to a numpy array, then to bytes
                # img_array = np.array(msg)
                # frame = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
                # _, buffer = cv2.imencode(
                #     '.jpg', frame, image_encode_compress)
                # array_to_bytes = buffer.tobytes()

                # bytes_to_array = numpy.frombuffer(message, numpy.uint8)
                # to_image = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                # testing images in video frames
                # cv2.imshow("screenshot_video", to_image)
                # cv2.waitKey(1)
                # d_bytes = message.decode('utf-8')
                # ds = base64.dncodebytes(message)
                print(f"received: {message}")
                await websocket.send("received...")
            # out.write(bytes_to_array)

    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")

    finally:
        cv2.destroyAllWindows()

# Start the WebSocket server on localhost, port 8080
if __name__ == "__main__":
    start_server = websockets.serve(
        server, '', 8005, ping_interval=None, max_size=1000000)
    print("WebSocket server is running on ws://46.138.93.58:443")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
