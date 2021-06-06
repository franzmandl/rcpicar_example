from logging import getLogger
from .VoltageMessage import VoltageMessage
from rcpicar.routed.IRoutedReceiveListener import IRoutedReceiveListener
from rcpicar.routed.RoutedReceiveService import RoutedReceiveService
from rcpicar.util.ConnectionDetails import ConnectionDetails
from ..message import custom_message_types


class VoltageClientService(IRoutedReceiveListener):
    def __init__(self, routed_send_service: RoutedReceiveService) -> None:
        self.logger = getLogger(__name__)
        routed_send_service.add_receive_listener(custom_message_types.voltage, self)

    def on_routed_receive(self, message_type: int, message: bytes, details: ConnectionDetails) -> None:
        self.logger.info(f'New measurement: {VoltageMessage.decode(message).voltage}')
