class HardwareKeycode:
    def __init__(self, value: int) -> None:
        self.value = value

    def is_up(self) -> bool:
        return self.value == 111

    def is_left(self) -> bool:
        return self.value == 113

    def is_down(self) -> bool:
        return self.value == 116

    def is_right(self) -> bool:
        return self.value == 114

    def is_w(self) -> bool:
        return self.value == 25

    def is_a(self) -> bool:
        return self.value == 38

    def is_s(self) -> bool:
        return self.value == 39

    def is_d(self) -> bool:
        return self.value == 40

    def is_space(self) -> bool:
        return self.value == 65

    def is_shift(self) -> bool:
        return self.value == 50
