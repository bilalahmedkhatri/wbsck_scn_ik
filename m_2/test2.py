import socket
import mss
import numpy as np
import time
import string
import random
import cv2


# Function to generate a random file name (not used in this example)
def file_name():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=5)) + '.png'


# Function to detect screens
def detect_screens(screens) -> list:
    screen = []
    for monitor_number, monitors in enumerate(screens.monitors[1:], start=1):
        screen.append(monitors)
    return screen


# Function to capture the screen and send it through a socket
def capture_and_send_screen(address, port):
    with mss.mss() as sct:
        # Detect screens
        detect_screen = detect_screens(sct)
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        client_socket.connect((address, port))
        b = 0
        try:
            while True:
                # data_in_bytes = []
                for scn in detect_screen:
                    # Capture the screen part
                    screenshot = sct.grab(scn)
                    if not screenshot:
                        break

                    # Convert the screenshot to a numpy array, then to bytes
                    img_array = np.array(screenshot)
                    frame = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
                    _, buffer = cv2.imencode('.jpg', frame)
                    array_to_bytes = buffer.tobytes()
                    # data_in_bytes.append(array_to_bytes)

                    # Send the length of the data and the data itself
                    client_socket.send(array_to_bytes)

                # Wait for the server's response (optional)
                data = client_socket.recv(1024).decode()
                print(f"Received: {data}")

                # Sleep for a bit before sending the next screenshot
                b += 1
                print(f"Sleeping for 0.1 seconds...", b)
                time.sleep(0.1)

        except KeyboardInterrupt:
            print('Interrupted')

        finally:
            # Close the socket connection
            client_socket.close()


if __name__ == '__main__':
    capture_and_send_screen('localhost', 8000)
