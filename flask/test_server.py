from websockets import serve


async def get_data_client():
    async for message in websocket:
        await websocket.send(message)
