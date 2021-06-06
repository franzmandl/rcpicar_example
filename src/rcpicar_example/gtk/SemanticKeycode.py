from .HardwareKeycode import HardwareKeycode


class SemanticKeycode:
    def __init__(self, value: HardwareKeycode) -> None:
        self.value = value

    def is_forward(self) -> bool:
        return self.value.is_up() or self.value.is_w()

    def is_left(self) -> bool:
        return self.value.is_left() or self.value.is_a()

    def is_backward(self) -> bool:
        return self.value.is_down() or self.value.is_s()

    def is_right(self) -> bool:
        return self.value.is_right() or self.value.is_d()

    def is_brake(self) -> bool:
        return self.value.is_space()
