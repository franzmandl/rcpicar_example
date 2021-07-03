#!/usr/bin/env python3
from logging import DEBUG
from rcpicar.log.LogListener import LogListener
from rcpicar.message import message_types
from rcpicar.routed.RoutedSendService import RoutedSendService
from rcpicar.server.Server import Server
from rcpicar.util.argument import create_value_argument, process_arguments
from rcpicar_example.gpio.TamiyaTt01 import TamiyaTt01
from rcpicar_example.message import custom_message_types
from rcpicar_example.voltage.VoltageServerService import VoltageServerArguments, VoltageServerService


def main() -> None:
    server = Server()
    # Optional: Override default values
    server.gpio_arguments.pwm_motor_maximum.set(12)
    server.gpio_arguments.pwm_motor_minimum.set(-20)
    server.gpio_arguments.pwm_steering_maximum.set(75)
    server.gpio_arguments.pwm_steering_offset.set(-8)
    server.gpio_arguments.pwm_steering_invert.set(True)
    server.log_arguments.log_level.set(DEBUG)
    # Optional: Register and process command line arguments
    voltage_arguments = VoltageServerArguments()
    process_arguments([
        server.discovery_arguments,
        server.discovery_arguments.common,
        server.gpio_arguments,
        create_value_argument(
            server.gpio_arguments.pwm_motor_maximum, '--pwm-motor-maximum', int, 'Throttle max forward speed.'),
        create_value_argument(
            server.gpio_arguments.pwm_motor_minimum, '--pwm-motor-minimum', int, 'Throttle max backward speed.'),
        server.gstreamer_arguments,
        server.latency_arguments,
        server.log_arguments,
        server.server_arguments,
        server.throttle_arguments,
        voltage_arguments,
    ])
    # Configure log
    server.log_arguments.configure_log()
    # Optional: Override default values
    server.gpio_service.set(TamiyaTt01(server.gpio_service.get()))
    # Enable services
    custom_unreliable_routed_send_service = RoutedSendService(
        server.unreliable_routed_send_service.get().create_send_service(message_types.custom))
    server.car_service.get()
    server.discovery_service.get()
    server.gstreamer_service.get()
    stop_service = server.stop_service.get()
    VoltageServerService(
        voltage_arguments, server.clock.get(),
        custom_unreliable_routed_send_service.create_send_service(custom_message_types.voltage),
        server.service_manager.get())
    # Optional: Configure log output
    log_listener = LogListener()
    server.reliable_service.get().add_reliable_connect_listener(log_listener)
    server.reliable_service.get().add_reliable_disconnect_listener(log_listener)
    server.reliable_service.get().add_reliable_os_error_listener(log_listener)
    server.unreliable_service.get().add_unreliable_os_error_listener(log_listener)
    # Start and run services
    with server.use_services():
        stop_service.wait()


if __name__ == '__main__':
    main()
