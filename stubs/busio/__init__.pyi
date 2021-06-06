import adafruit_blinka.microcontroller.generic_linux.libgpiod_pin


class I2C:
    def __init__(
            self,
            scl: adafruit_blinka.microcontroller.generic_linux.libgpiod_pin.Pin,
            sda: adafruit_blinka.microcontroller.generic_linux.libgpiod_pin.Pin,
    ) -> None:
        ...
