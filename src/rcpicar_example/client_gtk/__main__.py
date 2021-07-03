#!/usr/bin/env python3
from logging import DEBUG
from rcpicar.client.Client import Client
from rcpicar.log.LogListener import LogListener
from rcpicar.message import message_types
from rcpicar.routed.RoutedReceiveService import RoutedReceiveService
from rcpicar.util.argument import process_arguments
from rcpicar_example.gtk.GtkUiService import GtkUiArguments, GtkUiService
from rcpicar_example.message import custom_message_types
from rcpicar_example.voltage.VoltageClientService import VoltageClientService


def main() -> None:
    client = Client()
    # Optional: Override default values
    client.log_arguments.log_level.set(DEBUG)
    # Optional: Register and process command line arguments
    gtk_ui_arguments = GtkUiArguments(client.gstreamer_arguments.settings)
    process_arguments([
        client.client_arguments,
        client.discovery_arguments,
        client.discovery_arguments.common,
        client.gstreamer_arguments,
        gtk_ui_arguments,
        client.log_arguments,
    ])
    # Configure log
    client.log_arguments.configure_log()
    # Enable services
    custom_unreliable_routed_receive_service = RoutedReceiveService(
        client.unreliable_routed_receive_service.get().create_receive_service(message_types.custom))
    client.latency_service.get()
    ui_service = GtkUiService(
        gtk_ui_arguments, client.car_service.get(), client.gstreamer_service.get(), client.reliable_service.get(),
        client.service_manager.get())
    VoltageClientService(custom_unreliable_routed_receive_service.create_receive_service(custom_message_types.voltage))
    # Optional: Configure log output
    log_listener = LogListener()
    client.reliable_service.get().add_reliable_connect_listener(log_listener)
    client.reliable_service.get().add_reliable_disconnect_listener(log_listener)
    client.reliable_service.get().add_reliable_os_error_listener(log_listener)
    client.unreliable_service.get().add_unreliable_os_error_listener(log_listener)
    # Start and run services
    with client.use_services():
        ui_service.run()


if __name__ == '__main__':
    main()
