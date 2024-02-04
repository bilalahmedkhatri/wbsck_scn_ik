import websockets
import threading
import logging
import json


class Server():
    clients = []
    clients_lock = threading.Lock()

    async def register(self, ws: websockets.WebSocketServerProtocol, key, who) -> None:
        with self.clients_lock:
            self.clients.append({"key": key, "ws": ws, "who": who})
        logging.info(who + f' {ws.remote_address[0]} connects')

    async def unregister(self, ws: websockets.WebSocketServerProtocol) -> None:
        with self.clients_lock:
            for client in self.clients:
                if client["ws"] == ws:
                    del client
        logging.info(f'{ws.remote_address[0]} connects')

    async def init_event(self, ws: websockets.WebSocketServerProtocol, key: str, who: str) -> None:
        await self.register(ws, key, who)
        logging.info(f'{ws.remote_address[0]} with key f{key}')

    async def receiver_request_event(self, ws: websockets.WebSocketServerProtocol, key: str) -> None:
        await self.register(ws, key, "receiver")
        for client in self.clients:
            if client["key"] == key:
                await client["ws"].send(json.dumps({"cmd": "receiver_request"}))

    async def send_to_receiver(self, key, message):
        for client in self.clients:
            if (client["key"] == key and client["who"] == "receiver"):
                await client["ws"].send(message)

    async def send_to_sender(self, key, message):
        for client in self.clients:
            if (client["key"] == key and client["who"] == "sender"):
                await client["ws"].send(message)

    async def ws_handler(self, ws: websockets.WebSocketServerProtocol, uri: str):
        try:
            async for message in ws:
                deserialized = json.loads(message)
                cmd = deserialized["cmd"]
                key = deserialized["key"]
                if cmd == "sender_init":
                    await self.init_event(ws, key, "sender")
                elif cmd == "receiver_request":
                    await self.receiver_request_event(ws, key)
                elif cmd == "send":
                    await self.send_to_receiver(key, message)
                elif cmd == "receiver_init":
                    await self.init_event(ws, key, "receiver")
                    await self.send_to_sender(key, message)
                elif cmd == "file_details":
                    await self.send_to_receiver(key, message)
        except websockets.exceptions.ConnectionClosed as e:
            logging.info("Connection closed")
