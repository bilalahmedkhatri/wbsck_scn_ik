import asyncio
import websockets
import cv2
import numpy as np
from json import loads
from lzma import decompress
from open_port import find_process_by_port, close_port


PORT_NUMBER = 8006
USERS_CONNECTED = set()


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
        print("port closed :", process_port)


async def server(websocket, path):
    v = websocket.data_received

    print(v)
    # "ws" for websocket connection from url path
    monitor_tools = ServerMonitorTools(websocket=websocket)
    client_os_user_name = websocket.path
    # print(client_os_user_name, websocket.extra_headers)
    USERS_CONNECTED.add((websocket.path, websocket.origins))
    try:
        while True:
            client_data = await websocket.recv()
            data = (client_os_user_name, client_data[2])
            for client in USERS_CONNECTED:
                if client != path:
                    await websocket.send(data)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {websocket.remote_address}, {e}")

    finally:
        USERS_CONNECTED.remove(websocket)

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


# [ '_fragmented_message_waiter', '_host', '_paused', '_pop_message_waiter', '_port', '_process_request', '_put_message_waiter', '_secure', '_select_subprotocol', 'abort_pings', 'available_extensions', 'available_subprotocols', 'close', 'close_code', 'close_connection', 'close_connection_task', 'close_rcvd', 'close_rcvd_then_sent', 'close_reason', 'close_sent', 'close_timeout', 'close_transport', 'closed', 'connection_closed_exc', 'connection_lost', 'connection_lost_waiter', 'connection_made', 'connection_open', 'data_received', 'debug', 'drain', 'ensure_open', 'eof_received', 'extensions', 'extra_headers', 'fail_connection', 'handler', 'handler_task', 'handshake', 'host', 'id', 'is_client', 'keepalive_ping', 'keepalive_ping_task', 'latency', 'legacy_recv', 'local_address', 'logger', 'loop', 'max_queue', 'max_size', 'messages', 'open', 'open_timeout', 'origin', 'origins', 'path', 'pause_writing', 'ping', 'ping_interval', 'ping_timeout', 'pings', 'pong', 'port', 'process_extensions', 'process_origin', 'process_request', 'process_subprotocol', 'read_data_frame', 'read_frame', 'read_http_request', 'read_limit', 'read_message', 'reader', 'recv', 'remote_address', 'request_headers', 'response_headers', 'resume_writing', 'secure', 'select_subprotocol', 'send', 'server_header', 'side', 'state', 'subprotocol', 'transfer_data', 'transfer_data_exc', 'transfer_data_task', 'transport', 'wait_closed', 'wait_for_connection_lost', 'write_close_frame', 'write_frame', 'write_frame_sync', 'write_http_response', 'write_limit', 'ws_handler', 'ws_server']

# dir['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'removeprefix', 'removesuffix', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
