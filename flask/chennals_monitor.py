from websockets import connect, exceptions
import json
import asyncio
import uuid


def combined_image_data(screenshot):
    scn = screenshot.monitors(0)
    return u_id


def user_ID():
    return uuid.uuid4()


async def send_data():
    url = "ws://localhost:8081/ws/"
    async with connect(url) as websocket:
        try:
            while True:
                num_added = f"Unique Numbers {user_ID()}"
                await websocket.send(num_added)
                await asyncio.sleep(1)

        except exceptions.ConnectionClosed as e:
            print("Connection closed : ", e)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_data())
