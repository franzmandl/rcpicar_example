#!/usr/bin/env python3
from rcpicar.argument import process_arguments
from rcpicar.client.Client import Client
from rcpicar.log.LogLevel import LogLevel
from rcpicar.log.LogListener import LogListener
from rcpicar.log.util import configure_log
from rcpicar.message import message_types
from rcpicar.routed.RoutedReceiveService import RoutedReceiveService
from rcpicar_example.gtk.GtkUi import GtkUi
from rcpicar_example.voltage.VoltageClientService import VoltageClientService


def main() -> None:
    client = Client()
    # Optional: Override default values
    client.log_arguments.log_level.set(LogLevel.debug)
    # Optional: Register and process command line arguments
    process_arguments([
        client.car_arguments,
        client.discovery_arguments,
        client.discovery_arguments.common,
        client.client_arguments,
        client.gstreamer_arguments,
        client.log_arguments,
    ])
    # Configure log
    configure_log(client.log_arguments.log_file.get(), client.log_arguments.log_level.get())
    # Enable services
    custom_unreliable_routed_receive_service = RoutedReceiveService(
        client.unreliable_routed_receive_service.get().create_receive_service(message_types.custom))
    client.latency_service.get()
    ui = GtkUi(
        client.car_service.get(), client.clock.get(), client.gstreamer_service.get(), client.reliable_service.get(),
        client.service_manager.get())
    VoltageClientService(custom_unreliable_routed_receive_service)
    # Optional: Configure log output
    log_listener = LogListener()
    client.reliable_service.get().add_reliable_connect_listener(log_listener)
    client.reliable_service.get().add_reliable_disconnect_listener(log_listener)
    client.reliable_service.get().add_reliable_os_error_listener(log_listener)
    client.unreliable_service.get().add_unreliable_os_error_listener(log_listener)
    # Start and run services
    with client.service_manager.get():
        ui.run()


if __name__ == '__main__':
    main()
