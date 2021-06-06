class _CustomMessageTypes:
    def __init__(self) -> None:
        message_type_generator = iter(range(2**8))
        self.voltage = next(message_type_generator)


custom_message_types = _CustomMessageTypes()
