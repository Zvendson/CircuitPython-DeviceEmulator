import usb_cdc
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

from packets import PacketHeader

MAX_SENDABLE_KEYCODES = 16
MAX_TEXT_LENGTH       = 2048

serial = usb_cdc.data
console = usb_cdc.console

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

def bytecodes_to_list(bytecodes):
    return list(bytecodes)


def handle_send_keycode_packet():
    global kbd

    bytecodes = serial.read(MAX_SENDABLE_KEYCODES)
    codes = bytecodes_to_list(bytecodes)

    kbd.send(*codes)


def handle_press_keycode_packet():
    global kbd

    bytecodes = serial.read(MAX_SENDABLE_KEYCODES)
    codes = bytecodes_to_list(bytecodes)

    kbd.press(*codes)


def handle_release_keycode_packet():
    global kbd

    bytecodes = serial.read(MAX_SENDABLE_KEYCODES)
    codes = bytecodes_to_list(bytecodes)

    kbd.release(*codes)


def handle_write_text_packet():
    global kbd

    bytetext = serial.read(MAX_TEXT_LENGTH)
    text = ""
    try:
        text = bytetext.decode("utf-8")
    except:
        text = ""

    layout.write(text)


while True:
    if serial.in_waiting > 0:
        byteheader = serial.read(1)
        header     = int.from_bytes(byteheader, "big")

        if header == PacketHeader.SendKeycode:
            handle_send_keycode_packet()

        elif header == PacketHeader.PressKeycode:
            handle_press_keycode_packet()

        elif header == PacketHeader.ReleaseKeycode:
            handle_release_keycode_packet()

        elif header == PacketHeader.WriteText:
            handle_write_text_packet()


