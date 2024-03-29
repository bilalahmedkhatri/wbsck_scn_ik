import asyncio
import websockets
import cv2
import mss
import numpy as np
from json import loads
from lzma import decompress
from open_port import find_process_by_port, close_port


PORT_NUMBER = 8006


class ServerMonitorTools:

    def __init__(self, *args, **kwargs):
        self.frames = []
        self.websocket = kwargs["websocket"]
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Video codec

    async def get_data_from_websocket(self) -> list:
        data = await self.websocket.recv()
        data_dict = loads(data)
        compressed_raw_image = data_dict['image'].encode(
            "latin-1")  # decoded string in latin-1
        decompress_image = decompress(
            compressed_raw_image)  # comporessed image frame
        return [decompress_image, data_dict['status'], data_dict['size']]

    async def build_video(self):
        image_bytes, image_status, image_size = await self.get_data_from_websocket()
        out = cv2.VideoWriter('video.avi', self.fourcc,
                              15.0, (image_size[0], image_size[1]))

        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        to_image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
        print('types', image_array.size, image_size, type(to_image))


def check_port(port):
    process_port = find_process_by_port(port)
    if process_port:
        close_port(port)
        process_port.terminate()


async def server(websocket, path):
    monitor_tools = ServerMonitorTools(websocket=websocket)
    try:
        while True:
            value = await monitor_tools.build_video()
            await websocket.send("received...")
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")


# Start the WebSocket server on localhost, port 8080
if __name__ == "__main__":
    port = PORT_NUMBER
    check_port(port)
    start_server = websockets.serve(
        server, '', port, ping_interval=None, max_size=1000000)
    print(
        f"WebSocket server is running on localhost {port}")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
