from __future__ import annotations
from struct import pack, unpack
from typing import cast, Tuple
from rcpicar.message import IMessage

format_string = '<f'
format_type = Tuple[float]


class VoltageMessage(IMessage):
    def __init__(self, voltage: float) -> None:
        self.voltage = voltage

    def encode(self) -> bytes:
        return pack(format_string, self.voltage)

    @staticmethod
    def decode(message: bytes) -> VoltageMessage:
        voltage, = cast(format_type, unpack(format_string, message))
        return VoltageMessage(voltage)
