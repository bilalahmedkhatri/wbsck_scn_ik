from websockets import connect, exceptions
import json
import asyncio


async def send_data():

    url = "ws://localhost:8000/ws/"
    async with connect(url) as websocket:
        print("websockets connected")
        try:
            while True:
                d = "received data from websockets"
                await websocket.send(d)
                rec = await websocket.recv()
                await asyncio.sleep(1)
                print(f"receve :", rec)

        except exceptions.ConnectionClosed as e:
            print("Connection closed : ", e)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_data())
