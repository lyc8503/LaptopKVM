import logging
from pynput.mouse import Listener
from hid.util import mouse_to_absolute_event


from pynput.mouse import Controller


def capture_and_forward_mouse(dev):
    """
    Main method for control using pynput
    This method will capture the mouse input and forward it to the serial port (ch9329)
    :param serial_port:
    :return:
    """
    buttons = set()

    main_size = (1920, 1080)
    secondary_size = (1920, 1080)
    secondary_max = (4095, 4095)
    secondary_loc = [0, 0]

    mouse = Controller()

    def on_move(x, y):
        delta = (x - mouse.position[0], y - mouse.position[1])
        logging.info(f"Mouse moved {delta} pos {(x, y)}")

        if x > main_size[0]:
            listener._suppress = True
        
        if listener._suppress:
            # Mouse is on secondary screen
            secondary_loc[0] += delta[0]
            secondary_loc[1] += delta[1]
            if secondary_loc[0] < 0:
                listener._suppress = False

            secondary_loc[0] = max(0, min(secondary_size[0], secondary_loc[0]))
            secondary_loc[1] = max(0, min(secondary_size[1], secondary_loc[1]))
            logging.info(f"Mouse on secondary screen {secondary_loc}")
            dev.send_absolute_mouse(
                mouse_to_absolute_event(
                    x=secondary_loc[0] * secondary_max[0] // secondary_size[0],
                    y=secondary_loc[1] * secondary_max[1] // secondary_size[1],
                    buttons=buttons,
                    max_x=secondary_max[0],
                    max_y=secondary_max[1],
                )
            )
        

    def on_click(x, y, button, pressed):
        logging.info(f"Mouse clicked {button} {'pressed' if pressed else 'released'}")
        if not listener._suppress:
            return
        if pressed:
            buttons.add(button)
        else:
            buttons.remove(button)
        dev.send_absolute_mouse(mouse_to_absolute_event(buttons=buttons))

    def on_scroll(x, y, dx, dy):
        logging.info(f"Mouse scrolled ({dx}, {dy})")
        if not listener._suppress:
            return
        dev.send_absolute_mouse(mouse_to_absolute_event(scroll=dy, buttons=buttons))

    listener = Listener(
        on_move=on_move, on_click=on_click, on_scroll=on_scroll
    )
    listener.start()
    return listener
