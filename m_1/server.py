# Server-Side

import socket
import base64
import cv2
import ffmpeg
import numpy as np

# Create a WebSocket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8000))
server.listen()

while True:
    # Accept a WebSocket connection
    connection, client_address = server.accept()

    # Receive encoded frames from the client
    frames = []
    x_y = []

    print(x_y)

    while True:
        frame_data = connection.recv(1024)

        print(f"frame_data {frame_data}")
        if not frame_data:
            break

        encoded_frame = base64.b64decode(frame_data).decode('utf-8')
        print(f"encoded_frame {encoded_frame}")

        frame = cv2.imdecode(np.fromstring(
            encoded_frame, np.uint8), cv2.IMREAD_COLOR)

        if not x_y:
            x_y.append(frame.shape[1])

        print(f"frame {frame}")
        frames.append(frame)

    print(f"frames {frames}")

    # Build a video file using FFmpeg
    output_path = 'recorded_video.mp4'
    with open(output_path, 'wb') as out_file:
        writer = ffmpeg.input(
            'pipe:',
            format='image2pipe',
            codec='rawvideo',
            pix_fmt='rgb24',
            framesize=f'{x_y[0]}x{x_y[1]}'
        ).output(out_file)
        writer.run()

    # Send a message to the client indicating video building completion
    connection.send('VIDEO_BUILT'.encode('utf-8'))

    # Serve the video file to the client
    response = 'Content-Type: video/mp4\r\n\r\n'
    with open(output_path, 'rb') as file:
        response += file.read()
    connection.sendall(response.encode('utf-8'))
    connection.close()


# encoding or decoding ka masla aa raha hai
