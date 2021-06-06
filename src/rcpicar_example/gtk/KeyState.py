from .SemanticKeycode import SemanticKeycode


class KeyState:
    def __init__(self) -> None:
        self.forward = False
        self.left = False
        self.backward = False
        self.right = False
        self.brake = False

    def is_key_pressed(self, keycode: SemanticKeycode) -> bool:
        if keycode.is_forward():
            return self.forward
        elif keycode.is_left():
            return self.left
        elif keycode.is_backward():
            return self.backward
        elif keycode.is_right():
            return self.right
        elif keycode.is_brake():
            return self.brake
        else:
            return False

    def set_key_pressed(self, keycode: SemanticKeycode, value: bool) -> bool:
        if keycode.is_forward():
            self.forward = value
            return True
        elif keycode.is_left():
            self.left = value
            return True
        elif keycode.is_backward():
            self.backward = value
            return True
        elif keycode.is_right():
            self.right = value
            return True
        elif keycode.is_brake():
            self.brake = value
            return True
        else:
            return False
