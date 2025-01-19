import logging


class CH9329:
    def __init__(self, port):
        self.port = port

    def send_scancode(self, scancode: bytes):
        assert len(scancode) == 8, "Keyboard scancode must be 8 bytes long"
        self.send(b"\x02", scancode)

    def send(self, cmd, data):
        HEAD = b"\x57\xAB"  # frame header
        ADDR = b"\x00"  # address
        LEN = len(data).to_bytes(1)  # data length

        packet = HEAD + ADDR + cmd + LEN + data
        SUM = sum(packet) % 256
        packet += SUM.to_bytes(1)
        logging.debug(f"Serial packet: {packet}")

        # Send packet
        self.port.write(packet)

        # Response from CH9329, 7 bytes
        ret = self.port.read(7)
        assert ret[5] == 0x00, f"ERROR: {ret}"
