import asyncio
import websockets
import mss
import json
import lzma
from ws_tools import ClientMonitorTools
import logging
import datetime


log_datetime = datetime.datetime.now()
dt_replace = log_datetime.ctime().replace(" ", "_")
logging.basicConfig(filename=f'{dt_replace}.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def detect_screens(screens) -> list:
    screen = []
    for monitor_number, monitors in enumerate(screens.monitors[1:], start=1):
        screen.append(monitors)
    # print(screen) format like this : [{'left': 0, 'top': 0, 'width': 1280, 'height': 720}]
    if screen:
        logging.info(f'image captured: {screen}')
    else:
        logging.error(f'image captured: {screen}')
    return screen


async def send_images(websocket):

    print('dirs: ', websocket.extra_headers)

    with mss.mss() as sct:
        # Detect screens
        detect_screen = detect_screens(sct)
        try:
            while websocket.is_client:  # if client then response is true
                for scn in detect_screen:
                    # manage length of screens (remaining task)
                    # Capture the screen part
                    screenshot = sct.grab(scn)
                    if not screenshot:
                        break

                    # Send the image data to the server
                    compressed_lmza = lzma.compress(screenshot.rgb)
                    decode_image = compressed_lmza.decode("latin-1")
                    data = json.dumps({
                        'image': decode_image,
                        'status': True,
                        'size': screenshot.size,
                    })
                    await websocket.send(data)
                    recv_data = await websocket.recv()
                    print(f"receve :", recv_data)
                    await asyncio.sleep(0.7)

        except websockets.exceptions.ConnectionClosed as e:
            print("WebSocket connection closed.", e)


async def main():
    tools = ClientMonitorTools()
    SECURE_TOKEN = tools.secure_token()
    url = f"ws://localhost:8006/ws/{SECURE_TOKEN}"
    extra_header_data = tools.extra_header_data()
    async with websockets.connect(url, ping_interval=None, ping_timeout=50, extra_headers=extra_header_data) as websocket:
        logging.info(f'Client connected to {url}')
        print(f"Connected to {url}")
        await send_images(websocket)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())


# websocket dirs:  ['__aiter__', '__annotations__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_drain', '_drain_helper', '_drain_lock', '_drain_waiter', '_fragmented_message_waiter', '_host', '_paused', '_pop_message_waiter', '_port', '_put_message_waiter', '_secure', 'abort_pings', 'available_extensions', 'available_subprotocols', 'close', 'close_code', 'close_connection', 'close_connection_task', 'close_rcvd', 'close_rcvd_then_sent', 'close_reason', 'close_sent', 'close_timeout', 'close_transport', 'closed', 'connection_closed_exc', 'connection_lost', 'connection_lost_waiter', 'connection_made', 'connection_open', 'data_received', 'debug', 'drain', 'ensure_open', 'eof_received', 'extensions', 'extra_headers', 'fail_connection', 'handshake', 'host', 'id', 'is_client', 'keepalive_ping', 'keepalive_ping_task', 'latency', 'legacy_recv', 'local_address', 'logger', 'loop', 'max_queue', 'max_size', 'messages', 'open', 'origin', 'path', 'pause_writing', 'ping', 'ping_interval', 'ping_timeout', 'pings', 'pong', 'port', 'process_extensions', 'process_subprotocol', 'read_data_frame', 'read_frame', 'read_http_response', 'read_limit', 'read_message', 'reader', 'recv', 'remote_address', 'request_headers', 'response_headers', 'resume_writing', 'secure', 'send', 'side', 'state', 'subprotocol', 'transfer_data', 'transfer_data_exc', 'transfer_data_task', 'transport', 'user_agent_header', 'wait_closed', 'wait_for_connection_lost', 'write_close_frame', 'write_frame', 'write_frame_sync', 'write_http_request', 'write_limit']
