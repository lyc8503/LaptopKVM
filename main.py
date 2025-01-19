import logging
import threading
from hid.ch9329 import CH9329
from hid.keyboard_capture import capture_and_forward_keyboard
from hid.mouse_capture import capture_and_forward_mouse
import serial
import time
import os


logging.basicConfig(
    format="%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s: %(message)s",
    level=logging.INFO,
)

ch9329_serial = serial.Serial("COM10", 115200, timeout=1)
ch9329_dev = CH9329(ch9329_serial)

kbd_listener = capture_and_forward_keyboard(ch9329_dev)
mouse_listener = capture_and_forward_mouse(ch9329_dev)


import ctypes

# Query DPI Awareness (Windows 10 and 8)
print(ctypes.windll.shcore.SetProcessDpiAwareness(2))

import cv2


class VideoStream(threading.Thread):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        self.cap.set(3, 1920)
        self.cap.set(4, 1080)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            cv2.namedWindow("foo", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("foo", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("foo", frame)
            cv2.waitKey(1)

    def stop(self):
        self.cap.release()
        cv2.destroyAllWindows()


streamer = VideoStream()
streamer.start()

while True:
    if not kbd_listener.is_alive():
        mouse_listener.stop()
        break
    if not mouse_listener.is_alive():
        kbd_listener.stop()
        break
    time.sleep(0.2)

# Force exit without waiting for streamer
os._exit(0)
