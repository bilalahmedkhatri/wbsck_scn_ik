# Server
from test import capture_screen
import socket
import numpy as np


MAX_DATA = 1024


print("Server listening on port 8000...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind(('localhost', 8000))
    s.listen()
    conn, address = s.accept()

    with conn:
        print(f"Connected to {address}")
        while True:
            try:

                data = conn.recv(MAX_DATA)
                if not data:
                    break

                if len(data) > MAX_DATA:
                    print("Data exceeds maximum allowed, closing connection.")
                    # conn.close()
                    continue

                bytes_to_array = np.frombuffer(data, dtype=np.uint8)

                print(f"Received (length {len(data)}): {bytes_to_array}")

                # print(f"Received: {data}")

                conn.sendall("Hello from Server".encode())

                conn.close()

            except KeyboardInterrupt:
                print('Interrupted')
                break
