from logging import getLogger
from .VoltageMessage import VoltageMessage
from rcpicar.receive import IReceiveListener, IReceiveService
from rcpicar.util.ConnectionDetails import ConnectionDetails


class VoltageClientService(IReceiveListener):
    def __init__(self, receive_service: IReceiveService) -> None:
        self.logger = getLogger(__name__)
        receive_service.add_receive_listener(self)

    def on_receive(self, message: bytes, details: ConnectionDetails) -> None:
        self.logger.info(f'New measurement: {VoltageMessage.decode(message).voltage}')
