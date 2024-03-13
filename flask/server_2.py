import asyncio
import websockets
import cv2
import numpy as np
import json
import lzma


class ServerMonitorTools:

    def __init__(self, *args, **kwargs):
        self.frames = []
        self.websocket = kwargs["websocket"]
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Video codec

    async def get_socket_from_websocket(self) -> list:
        data = await self.websocket.recv()
        data_dict = json.loads(data)
        compressed_raw_image = data_dict['image'].encode(
            "latin-1")  # decoded string in latin-1
        decompress_image = lzma.decompress(
            compressed_raw_image)  # comporessed image frame
        return [decompress_image, data_dict['status'], data_dict['size']]

    async def build_video(self):
        image_bytes = await self.get_socket_from_websocket()
        out = cv2.VideoWriter('video.mp4', self.fourcc,
                              20.0, (image_bytes[2][0], image_bytes[2][1]))
        to_np_array = np.array(image_bytes[0])

        # image_array = np.frombuffer(image_bytes[1], dtype=np.uint8)
        # print('firet ', image_array)
        # to_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        # print(to_image)
        # frame = cv2.cvtColor(to_image, cv2.COLOR_BGRA2BGR)
        # cv2.imshow('video', image_array)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


async def server(websocket, path):
    monitor_tools = ServerMonitorTools(websocket=websocket)
    try:
        while True:
            await monitor_tools.build_video()
            await websocket.send("received...")
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")


# Start the WebSocket server on localhost, port 8080
if __name__ == "__main__":
    start_server = websockets.serve(
        server, '', 8005, ping_interval=None, max_size=1000000)
    print("WebSocket server is running on ws://46.138.93.58:443")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
