import adafruit_ads1x15.ads1115


class AnalogIn:
    voltage: float

    def __init__(self, ads: adafruit_ads1x15.ads1115.ADS1115, positive_pin: int) -> None:
        ...
