import cv2
# import threading
# import numpy as np
from json import loads, dumps
from lzma import decompress
# import subprocess
# import pillow

TEST = "TEST"


class ServerMonitorTools:

    def __init__(self, websocket, *args, **kwargs):
        self.frames = []
        self.websocket = websocket
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Video codec
        self.frame_count = 0
        self.fps = 12.0

    async def file_name(self) -> str:
        name = self.websocket.request_headers
        user_name = name['x-user-name']
        os = name['x-os']
        date = name['x-system-started-time'].split(
            ',')[1][2:].replace('/', '-')
        random_key = name['sec-websocket-key'][:6]
        return f"./video/{user_name}_{os}_{date}_{random_key}.avi"

    async def get_data_from_websocket(self) -> dict:
        data = await self.websocket.recv()
        data_dict = loads(data)
        compressed_raw_image = data_dict['image'].encode(
            "latin-1")  # decoded string in latin-1
        decompress_image = decompress(
            compressed_raw_image)  # comporessed image frame
        self.bytes_start = decompress_image
        return {'x-web-img-byte': decompress_image, 'x-web-status': data_dict['status'], 'x-web-img-size': data_dict['size']}

    def client(self, data, path):
        return dumps({'status': data['x-web-status'], 'size': data['x-web-img-size'], 'path': path})

    def web(self, data, path):
        return dumps({'status': data['x-web-status'], 'size': data['x-web-img-size'], 'path': path})

    async def image_status(self):
        data = await self.get_data_from_websocket()
        path = self.websocket.path

        print(f"path: {type(data['x-web-img-byte'])}, path, : {path}")
        if "client" in path:
            self.client(data, path)

        if "web" in path:
            self.web(data, path)

        # yaha se databejna hai

        # async def write_video(self, image_bytes, video_witter, frame_count, fps, duration):
        #     while frame_count < fps * duration:
        #         video_witter.write(image_bytes)
        #         frame_count += 1

        # image = cv2.imdecode(np.frombuffer(
        #     await image_bytes, np.uint8), cv2.IMREAD_COLOR)
        # video_witter.write(image)

        # async def build_video(self):
        #     file_name = await self.file_name()
        #     image_bytes, _, image_size = await self.get_data_from_websocket()
        #     width, height = image_size
        #     duration = 1
        #     total_frames = int(self.frame_count * self.fps)

        #     image = cv2.imdecode(np.frombuffer(
        #         image_bytes, np.uint8), cv2.IMREAD_COLOR)

        #     video_writer = await cv2.VideoWriter(
        #         file_name, self.fourcc, self.fps, (width, height))
        #     # Define a function to write the same frame repeatedly

        #     v_wrtie = cv2.VideoWriter(
        #         self.file_name(), self.fourcc, self.fps, (width, height))

        #     # def write_frame(video_writer, duration, frame_count):
        #     while self.frame_count < self.fps * duration:
        #         v_wrtie.write(image)
        #         self.frame_count += 1

        #     video_writer.release()

        # async def handle_threader(self):
        #     build_video = await self.build_video()
        #     thread = threading.Thread(target=build_video)
        #     thread.start()
        # thread.join()

        # def generate_video_from_bytes_threaded(self, image_bytes):
        #     # Extract image width and height from the image bytes
        #     image = cv2.imdecode(np.frombuffer(
        #         image_bytes, np.uint8), cv2.IMREAD_COLOR)
        #     image_height, image_width, _ = image.shape
        #     fps = 15.0
        #     fourcc = 'XVID'
        #     duration = 1
        #     video_filename = 'video.avi'

        #     video_writer = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(
        #         *fourcc), fps, (image_width, image_height))
        #     # Define a function to write the same frame repeatedly

        #     # def write_frame(video_writer, duration, frame_count):
        #     while frame_count < fps * duration:
        #         video_writer.write(image)
        #         frame_count += 1

        #     video_writer.release()

        #     # # Create video writer object with total number of frames based on fps and duration
        #     # total_frames = int(fps * duration)

        #     # # Create and start a thread to write frames repeatedly
        #     # thread = threading.Thread(target=write_frame, args=(video_writer, duration, 0))
        #     # thread.start()

        #     # # Wait for the thread to finish (after writing all frames)
        #     # thread.join()

        #     # # Release video writer
        #     video_writer.release()

        # # Example usage
        # image_bytes = [...]  # Your single image byte array
        # video_filename = "output_video.avi"
        # fps = 25
        # duration = 2  # Adjust duration as needed
