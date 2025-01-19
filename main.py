import logging
from hid.capture import main_pynput
import serial
import time

logging.basicConfig(
    format="%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s: %(message)s",
    level=logging.INFO,
)


ch9329dev = serial.Serial("COM10", 115200, timeout=1)
main_pynput(ch9329dev)
