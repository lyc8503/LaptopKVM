import logging
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button


def keys_to_scancode(keys):
    """
    Convert a set of pressed keys to a 8-byte scancode
    """
    scancode = [0x00 for _ in range(8)]
    # fmt: off
    # From https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2
    modifier_mapping = {
        # default to left side
        Key.ctrl: 0x01, Key.shift: 0x02, Key.alt: 0x04, Key.cmd: 0x08,
        # modifier masks
        Key.ctrl_l: 0x01, Key.shift_l: 0x02, Key.alt_l: 0x04, Key.cmd_l: 0x08,
        Key.ctrl_r: 0x10, Key.shift_r: 0x20, Key.alt_r: 0x40, Key.cmd_r: 0x80,
    }

    key_mapping = {
        # without shift
        'a': 0x04, 'b': 0x05, 'c': 0x06, 'd': 0x07, 'e': 0x08, 'f': 0x09, 'g': 0x0a,
        'h': 0x0b, 'i': 0x0c, 'j': 0x0d, 'k': 0x0e, 'l': 0x0f, 'm': 0x10, 'n': 0x11,
        'o': 0x12, 'p': 0x13, 'q': 0x14, 'r': 0x15, 's': 0x16, 't': 0x17, 'u': 0x18,
        'v': 0x19, 'w': 0x1a, 'x': 0x1b, 'y': 0x1c, 'z': 0x1d, '1': 0x1e, '2': 0x1f,
        '3': 0x20, '4': 0x21, '5': 0x22, '6': 0x23, '7': 0x24, '8': 0x25, '9': 0x26,
        '0': 0x27, '-': 0x2d, '=': 0x2e, '[': 0x2f, ']': 0x30, '\\': 0x31, ';': 0x33,
        "'": 0x34, '`': 0x35, ',': 0x36, '.': 0x37, '/': 0x38,
        # with shift
        'A': 0x04, 'B': 0x05, 'C': 0x06, 'D': 0x07, 'E': 0x08, 'F': 0x09, 'G': 0x0a,
        'H': 0x0b, 'I': 0x0c, 'J': 0x0d, 'K': 0x0e, 'L': 0x0f, 'M': 0x10, 'N': 0x11,
        'O': 0x12, 'P': 0x13, 'Q': 0x14, 'R': 0x15, 'S': 0x16, 'T': 0x17, 'U': 0x18,
        'V': 0x19, 'W': 0x1a, 'X': 0x1b, 'Y': 0x1c, 'Z': 0x1d, '!': 0x1e, '@': 0x1f,
        '#': 0x20, '$': 0x21, '%': 0x22, '^': 0x23, '&': 0x24, '*': 0x25, '(': 0x26,
        ')': 0x27, '_': 0x2d, '+': 0x2e, '{': 0x2f, '}': 0x30, '|': 0x31, ':': 0x33,
        '"': 0x34, '~': 0x35, '<': 0x36, '>': 0x37, '?': 0x38,

        Key.enter: 0x28, Key.esc: 0x29, Key.backspace: 0x2a, Key.tab: 0x2b,
        Key.space: 0x2c, Key.caps_lock: 0x39, Key.f1: 0x3a, Key.f2: 0x3b,
        Key.f3: 0x3c, Key.f4: 0x3d, Key.f5: 0x3e, Key.f6: 0x3f, Key.f7: 0x40,
        Key.f8: 0x41, Key.f9: 0x42, Key.f10: 0x43, Key.f11: 0x44, Key.f12: 0x45,
        Key.print_screen: 0x46, Key.scroll_lock: 0x47, Key.pause: 0x48,
        Key.insert: 0x49, Key.home: 0x4a, Key.page_up: 0x4b, Key.delete: 0x4c,
        Key.end: 0x4d, Key.page_down: 0x4e, Key.right: 0x4f, Key.left: 0x50,
        Key.down: 0x51, Key.up: 0x52, Key.num_lock: 0x53,
    }
    # fmt: on

    counter = 0
    for k in keys:
        if isinstance(k, KeyCode):
            k = k.char

        if k in modifier_mapping:
            scancode[0] |= modifier_mapping[k]
        elif k in key_mapping:
            if counter < 6:
                scancode[counter + 2] = key_mapping[k]
                counter += 1
            else:
                # We should send KEY_ERR_OVF
                # But for now, just ignore the extra keys
                continue
        else:
            logging.warning(f"Unknown key: {k}")

    return bytes(scancode)


def mouse_to_relative_event(dx=0, dy=0, buttons=(), scroll=0):
    """
    Convert mouse movement to a 5-byte relative mouse event
    """
    dx = max(-127, min(127, dx))
    dy = max(-127, min(127, dy))
    scroll = max(-127, min(127, scroll))

    event = [0x00 for _ in range(5)]
    event[0] = 0x01
    button_mapping = {Button.left: 0x01, Button.middle: 0x04, Button.right: 0x02}
    # TODO: not in mapping
    for b in buttons:
        event[1] |= button_mapping[b]
    event[2] = dx.to_bytes(1, "big", signed=True)[0]
    event[3] = dy.to_bytes(1, "big", signed=True)[0]
    event[4] = scroll.to_bytes(1, "big", signed=True)[0]

    return bytes(event)
