
from websockets.server import serve
import asyncio
import uuid
import cv2
import base64


# async def handle_image(websocket, path):
#     user_id = websocket.request_headers.get('user_id')
#     if not user_id:
#         return await websocket.send('Authentication failed: Missing user ID')

#     async for image in websocket:
#         decoded_image = base64.b64decode(image)
#         frame = cv2.imdecode(np.fromstring(decoded_image, np.uint8), cv2.IMREAD_COLOR)
#         user_frames.setdefault(user_id, []).append(frame)

async def handle_data(websocket, path):
    async for ws in websocket:
        print(ws)

async def main():
    async with serve(
        handle_data,
        "localhost", 8081,
        # extra_headers=['user_id']  # Allow client to send user ID
    ):
        print("server started...")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
