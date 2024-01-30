import ctypes
import mss
import numpy as np
import time
import string
import random
import cv2


def file_name():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=5))+'.png'


def detect_screens(screens) -> list:
    screen = []
    for monitor_number, monitors in enumerate(screens.monitors[1:], start=1):
        screen.append(monitors)
    return screen


def capture_screen():

    with mss.mss() as sct:

        detect_screen = detect_screens(sct)

        try:
            while True:
                for scn in detect_screen:
                    # The screen part to capture
                    screenshot = sct.grab(scn)
                    if not screenshot:
                        break

                    img_array = np.array(screenshot)
                    array_to_bytes = img_array.tobytes()

                time.sleep(0.1)

        except KeyboardInterrupt:
            print('Interrupted')



if __name__ == '__main__':
    capture_screen()
