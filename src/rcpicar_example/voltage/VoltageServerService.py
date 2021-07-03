from __future__ import annotations
try:
    from adafruit_ads1x15.ads1115 import ADS1115, P3
    from adafruit_ads1x15.analog_in import AnalogIn
    from board import SCL, SDA
    from busio import I2C

    adafruit_exception = None
except BaseException as exception:
    adafruit_exception = exception
from logging import getLogger
from typing import Optional
from rcpicar.clock import IClock
from rcpicar.send import ISendService
from rcpicar.service import IService, IServiceManager
from rcpicar.timeout.TimeoutSendService import TimeoutSendService
from rcpicar.util.argument import IArguments
from rcpicar.util.Lazy import Lazy
from rcpicar.util.Placeholder import Placeholder
from .VoltageMessage import VoltageMessage


def get_voltage_divider_gain(resistor1: float, resistor2: float) -> float:
    return (resistor1 + resistor2) / resistor2


class VoltageServerArguments(IArguments):
    def __init__(self) -> None:
        self.sender_interval_seconds = Lazy(lambda store: 10.0)
        self.voltage_divider_resistor1 = Lazy(lambda store: 991.0)
        self.voltage_divider_resistor2 = Lazy(lambda store: 471.0)


class VoltageServerService(IService):
    def __init__(
            self,
            arguments: VoltageServerArguments,
            clock: IClock,
            send_service: ISendService,
            service_manager: IServiceManager
    ) -> None:
        TimeoutSendService(
            clock,
            send_service,
            service_manager,
            arguments.sender_interval_seconds.get(),
            self.get_voltage_message,
        )
        self.analog_in: Placeholder[AnalogIn] = Placeholder()
        self.gain = get_voltage_divider_gain(
            arguments.voltage_divider_resistor1.get(), arguments.voltage_divider_resistor2.get())
        self.logger = getLogger(__name__)
        service_manager.add_service(self)

    def get_service_name(self) -> str:
        return __name__

    def join_service(self, timeout_seconds: Optional[float] = None) -> bool:
        return False

    def start_service(self) -> None:
        try:
            if adafruit_exception is not None:
                raise adafruit_exception
            self.analog_in.set(AnalogIn(ADS1115(I2C(SCL, SDA)), P3))
        except BaseException as exception_:
            self.logger.warning(f'Voltage is offline because: {exception_}', exc_info=exception_)

    def get_voltage(self) -> Optional[float]:
        with self.analog_in as (analog_in, _):
            if analog_in is not None:
                return analog_in.voltage * self.gain
            else:
                return None

    def get_voltage_message(self) -> Optional[bytes]:
        voltage = self.get_voltage()
        if voltage is not None:
            return VoltageMessage(voltage).encode()
        else:
            return None

    def stop_service(self) -> None:
        self.analog_in.clear()
