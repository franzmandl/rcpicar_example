from rcpicar.gpio.IGpioServerService import IGpioServerService
from rcpicar.util.Atomic import Atomic


class TamiyaTt01(IGpioServerService):
    def __init__(self, gpio_service: IGpioServerService) -> None:
        self.gpio_service = gpio_service
        self.last_steering_value = Atomic(0)

    def update(self, motor_value: int, steering_value: int) -> None:
        with self.last_steering_value as (last_steering_value, set_last_steering_value):
            if steering_value == 0:
                steering_value = int(-last_steering_value * 0.05 + 0.5)
            else:
                set_last_steering_value(steering_value)
        self.gpio_service.update(motor_value, steering_value)

    def reset(self) -> None:
        self.gpio_service.reset()
