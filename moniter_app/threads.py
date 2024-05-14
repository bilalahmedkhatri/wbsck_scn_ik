import cv2
import numpy as np
from threading import Thread


def build_video_from_bytes_async(byte_data, output_filename="output.avi", fps=25):
    """
    Builds a video from byte data using OpenCV in an async-like manner with threads.

    Args:
      byte_data: The byte data representing the video.
      output_filename: The name of the output video file (e.g., "output.avi").
      fps: The desired frames per second for the output video (default: 25).
    """
    def video_creation_task():
        # Decode bytes into a NumPy array (might require format-specific adjustments)
        decoded_frames = np.frombuffer(
            byte_data, dtype=np.uint8)  # Assuming uint8 format

        # Extract video properties (assuming known or derivable from byte data)
        height, width, channels =  # Your logic to determine height, width, and channels

        # Create video writer
        # Adjust fourcc code for desired format
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        video_writer = cv2.VideoWriter(
            output_filename, fourcc, fps, (width, height))

        # Write each decoded frame to the video
        for frame in decoded_frames.reshape(-1, height, width, channels):
            video_writer.write(frame)

        # Release resources
        video_writer.release()

    # Run video creation in a separate thread
    thread = Thread(target=video_creation_task)
    thread.start()
