import logging

from pynput.keyboard import Key, KeyCode, Listener
from hid.ch9329 import CH9329
from hid.util import keys_to_scancode


def main_pynput(serial_port):
    """
    Main method for control using pynput
    Starting point: https://stackoverflow.com/a/53210441/1681205
    :param serial_port:
    :return:
    """
    ch9329 = CH9329(serial_port)
    keys = set()

    def sync_to_serial():
        scancode = keys_to_scancode(keys)
        ch9329.send_scancode(scancode)

    def on_press(key):
        if key not in keys:
            keys.add(key)
            logging.info(f"On press: {key}, keys: {keys}")

            if Key.ctrl_l in keys and KeyCode(char="[") in keys and len(keys) == 2:
                logging.warning("Ctrl+[ detected, stopping listener")
                keys.clear()
                sync_to_serial()
                listener.stop()

            sync_to_serial()

    def on_release(key):
        if key in keys:
            keys.remove(key)
            logging.info(f"On release: {key}, keys: {keys}")

            sync_to_serial()

    with Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        listener.join()
