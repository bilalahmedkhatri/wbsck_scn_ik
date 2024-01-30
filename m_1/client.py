# Client-Side

import cv2
import socket
import base64
import numpy as np
import time

# Record screen frames using PyAutoGUI
import pyautogui
from PIL import ImageGrab


# # Connect to the server via WebSocket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(("localhost", 8000))

# # Start recording
# pyautogui.PAUSE = 0.0001  # Set low frame rate for demonstration
# pyautogui.press('f13')  # Enable screen recording

# Record screen frames and send them to the server
while True:

    # Capture the screenshot
    frame = ImageGrab.grab()

    # frame = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    image_data = cv2.imencode('.jpg', frame)[1].tobytes()

    # Encode the frame into Base64
    encoded_frame = base64.b64encode(image_data).decode('utf-8')
    decoded_frame = encoded_frame.encode('utf-8')

    print(f"encoded_frame {type(encoded_frame)}")

    print(f"decoded_frame {type(decoded_frame)}")
#     # Send the encoded frame to the server
    socket.sendall(decoded_frame)
    time.sleep(1)

# # Stop recording and send end recording message
# pyautogui.press('f13')  # Disable screen recording
# socket.send('END_RECORDING'.encode('utf-8'))


# encoding or decoding ka masla aa raha hai
