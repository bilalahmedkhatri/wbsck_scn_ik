from open_port import find_process_by_port, close_port
from psutil import NoSuchProcess, AccessDenied
from ser_tools import ServerMonitorTools
import asyncio
import websockets


PORT_NUMBER = 8005
USERS_CONNECTED = list()


async def server(websocket, path):
    # "ws" for websocket connection from url path
    monitor_tools = ServerMonitorTools(websocket, path)
    USERS_CONNECTED.append(websocket.path)
    print('clients', USERS_CONNECTED)
    try:
        while websocket.data_received:
            for client in USERS_CONNECTED:
                # receivng from user screens an sening back them to user
                if path in client:
                    # await monitor_tools.image_status()
                    x = await websocket.recv()
                    print('users :', x,  USERS_CONNECTED)
            await asyncio.sleep(0.1)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {websocket.remote_address}")

    # finally:
    #     USERS_CONNECTED.remove(websocket)

# Start the WebSocket server on localhost, port 8080
if __name__ == "__main__":
    port = PORT_NUMBER
    start_server = websockets.serve(
        server, 'localhost', port, ping_interval=None, max_size=1000000)
    print(f"WebSocket server started")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


# [ '_fragmented_message_waiter', '_host', '_paused', '_pop_message_waiter', '_port', '_process_request', '_put_message_waiter', '_secure', '_select_subprotocol', 'abort_pings', 'available_extensions', 'available_subprotocols', 'close', 'close_code', 'close_connection', 'close_connection_task', 'close_rcvd', 'close_rcvd_then_sent', 'close_reason', 'close_sent', 'close_timeout', 'close_transport', 'closed', 'connection_closed_exc', 'connection_lost', 'connection_lost_waiter', 'connection_made', 'connection_open', 'data_received', 'debug', 'drain', 'ensure_open', 'eof_received', 'extensions', 'extra_headers', 'fail_connection', 'handler', 'handler_task', 'handshake', 'host', 'id', 'is_client', 'keepalive_ping', 'keepalive_ping_task', 'latency', 'legacy_recv', 'local_address', 'logger', 'loop', 'max_queue', 'max_size', 'messages', 'open', 'open_timeout', 'origin', 'origins', 'path', 'pause_writing', 'ping', 'ping_interval', 'ping_timeout', 'pings', 'pong', 'port', 'process_extensions', 'process_origin', 'process_request', 'process_subprotocol', 'read_data_frame', 'read_frame', 'read_http_request', 'read_limit', 'read_message', 'reader', 'recv', 'remote_address', 'request_headers', 'response_headers', 'resume_writing', 'secure', 'select_subprotocol', 'send', 'server_header', 'side', 'state', 'subprotocol', 'transfer_data', 'transfer_data_exc', 'transfer_data_task', 'transport', 'wait_closed', 'wait_for_connection_lost', 'write_close_frame', 'write_frame', 'write_frame_sync', 'write_http_response', 'write_limit', 'ws_handler', 'ws_server']

# dir['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'removeprefix', 'removesuffix', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
