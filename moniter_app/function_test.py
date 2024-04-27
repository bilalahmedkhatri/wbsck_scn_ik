# import datetime


# x = datetime.datetime.now()
# print(x.ctime().replace(" ", "_"))


import websockets
import asyncio
import os

# print(os.getcwd())
# print()


async def send_data_in_loop(websocket):
    while True:
        await websocket.send("Data from Python")
        await asyncio.sleep(1)  # Adjust delay as needed


async def connect_and_send(uri):
    async with websockets.connect(uri) as websocket:
        # Start data sending in a separate task
        asyncio.create_task(send_data_in_loop(websocket))

if __name__ == "__main__":
    uri = "ws://your-server.com:port"  # Replace with your server URL
    asyncio.run(connect_and_send(uri))
