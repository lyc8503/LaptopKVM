import logging
from pynput.mouse import Listener
from hid.util import mouse_to_relative_event


from pynput.mouse import Controller


def capture_and_forward_mouse(dev):
    """
    Main method for control using pynput
    This method will capture the mouse input and forward it to the serial port (ch9329)
    :param serial_port:
    :return:
    """
    buttons = set()

    mouse = Controller()
    mouse.position = (0, 0)

    def on_move(x, y):
        delta = (x, y)
        logging.info(f"Mouse moved {delta}")
        dev.send_relative_mouse(mouse_to_relative_event(*delta, buttons=buttons))

    def on_click(x, y, button, pressed):
        logging.info(f"Mouse clicked {button} {'pressed' if pressed else 'released'}")
        if pressed:
            buttons.add(button)
        else:
            buttons.remove(button)
        dev.send_relative_mouse(mouse_to_relative_event(buttons=buttons))

    def on_scroll(x, y, dx, dy):
        logging.info(f"Mouse scrolled ({dx}, {dy})")
        dev.send_relative_mouse(mouse_to_relative_event(scroll=dy, buttons=buttons))

    listener = Listener(
        on_move=on_move, on_click=on_click, on_scroll=on_scroll, suppress=True
    )
    listener.start()
    return listener
