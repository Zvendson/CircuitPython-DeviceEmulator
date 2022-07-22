import time

import hexdump as hexdump
import serial.tools.list_ports

from keycode import Keycode
from packets import *


class DeviceEmulator:

    def __init__(self, port):
        self._port = port
        self._serial = serial.Serial(port.name)

    @classmethod
    def get_first(cls):
        pico_ports = list()

        for port in list(serial.tools.list_ports.comports()):
            if port.pid == 33012 and port.vid == 9114:
                pico_ports.append(port)

        if len(pico_ports) == 2:
            return cls(pico_ports[1])

        elif len(pico_ports) == 1:
            return cls(pico_ports[0])

        return None

    def _send_packet(self, packet):
        hexdump.hexdump(packet.get_bytes())  # debug
        self._serial.write(packet.get_bytes())

    def send(self, *keycodes: int):
        packet = SendKeycodePacket(keycodes)
        self._send_packet(packet)

    def press(self, *keycodes: int):
        packet = PressKeycodePacket(keycodes)
        self._send_packet(packet)

    def release(self, *keycodes: int):
        packet = ReleaseKeycodePacket(keycodes)
        self._send_packet(packet)

    def write(self, text: str):
        packet = WriteTextPacket(text)
        self._send_packet(packet)


if __name__ == '__main__':
    emu = DeviceEmulator.get_first()
    if emu is None:
        print("No raspberry pi pico device found.")
        exit(1)

    emu.write("Hello")

