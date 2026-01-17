import logging
from hid.ch9329 import CH9329
from hid.keyboard_capture import capture_and_forward_keyboard
from hid.mouse_capture import capture_and_forward_mouse
import serial
import time


logging.basicConfig(
    format="%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s: %(message)s",
    level=logging.INFO,
)

ch9329_serial = serial.Serial("COM4", 115200, timeout=1)
ch9329_dev = CH9329(ch9329_serial)

mouse_listener = capture_and_forward_mouse(ch9329_dev)
kbd_listener = capture_and_forward_keyboard(ch9329_dev)


while True:
    if not kbd_listener.is_alive():
        mouse_listener.stop()
        break
    if not mouse_listener.is_alive():
        kbd_listener.stop()
        break
    kbd_listener._suppress = mouse_listener._suppress
    time.sleep(0.2)

