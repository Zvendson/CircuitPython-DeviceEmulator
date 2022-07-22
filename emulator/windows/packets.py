import ctypes
from enum import Enum

# const
MAX_SENDABLE_KEYCODES = 16
MAX_TEXT_LENGTH       = 2048

# internal c types
_CHAR  = ctypes.c_char
_BYTE  = ctypes.c_byte
_WORD  = ctypes.c_ushort
_DWORD = ctypes.c_ulong


class PacketHeader(Enum):
    SendKeycode = 0x1
    PressKeycode = 0x2
    ReleaseKeycode = 0x3
    WriteText = 0x4


class BasePacket(ctypes.Structure):
    _fields_ = [
        ("Header", _BYTE)
    ]

    def __init__(self, header, *args, **kw):
        super().__init__(header.value, *args, **kw)

    def get_bytes(self):
        return bytes(self)


class SendKeycodePacket(BasePacket):
    _fields_ = [
        ("Codes", _BYTE * MAX_SENDABLE_KEYCODES)
    ]

    def __init__(self, code):
        super().__init__(PacketHeader.SendKeycode, code)


class PressKeycodePacket(BasePacket):
    _fields_ = [
        ("Codes", _BYTE * MAX_SENDABLE_KEYCODES)
    ]

    def __init__(self, code):
        super().__init__(PacketHeader.PressKeycode, code)


class ReleaseKeycodePacket(BasePacket):
    _fields_ = [
        ("Codes", _BYTE * MAX_SENDABLE_KEYCODES)
    ]

    def __init__(self, code):
        super().__init__(PacketHeader.ReleaseKeycode, code)


class WriteTextPacket(BasePacket):
    _fields_ = [
        ("Text", _CHAR * MAX_TEXT_LENGTH)
    ]

    def __init__(self, text: str):
        super().__init__(PacketHeader.WriteText, text.encode('utf-8'))
