import cv2
import numpy as np
from json import loads
from lzma import decompress


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
