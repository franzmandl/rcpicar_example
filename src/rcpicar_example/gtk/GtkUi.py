from __future__ import annotations
if True:  # Suppresses style warnings.
    from gi import require_version  # type: ignore
    require_version('Gtk', '3.0')
from gi.repository import Gtk  # type: ignore
from logging import getLogger
from threading import Thread
from typing import Any, Optional, Tuple
from rcpicar.car.CarClientService import CarClientService
from rcpicar.clock import IClock
from rcpicar.gstreamer.GStreamerClientService import GStreamerClientService
from rcpicar.gstreamer.GStreamerVideoListener import GStreamerVideoListener
from rcpicar.reliable import IReliableConnectListener, IReliableService
from rcpicar.service import AbstractServiceManager
from rcpicar.util.Atomic import Atomic
from rcpicar.util.ConnectionDetails import ConnectionDetails
from rcpicar.util.Placeholder import Placeholder
from rcpicar.util.SingleServiceManager import SingleServiceManager
from .GtkVideoService import GtkVideoService
from .HardwareKeycode import HardwareKeycode
from .KeyState import KeyState
from .SemanticKeycode import SemanticKeycode


class GtkUi(GStreamerVideoListener, IReliableConnectListener):
    def __init__(
            self,
            car_service: CarClientService,
            clock: IClock,
            gstreamer_service: GStreamerClientService,
            reliable_service: IReliableService,
            service_manager: AbstractServiceManager,
    ) -> None:
        self.car_service = car_service
        self.gstreamer_service = gstreamer_service.add_gstreamer_video_listener(self)
        self.is_video_loading = Atomic(False)
        self.key_state = Atomic(KeyState())
        self.logger = getLogger(__name__)
        self.service_manager = service_manager
        self.video_service_manager = SingleServiceManager(clock)
        self.xid: Placeholder[int] = Placeholder()
        reliable_service.add_reliable_connect_listener(self)

    def run(self) -> None:
        def on_destroy(window_: Any) -> None:
            self.video_service_manager.stop_all()
            Gtk.main_quit()

        def on_draw(area: Any, context: Any) -> None:
            context.scale(area.get_allocated_width(), area.get_allocated_height())
            context.set_source_rgb(0.7, 0.7, 0.7)
            context.fill()
            context.paint()

        window = Gtk.Window()
        window.connect('destroy', on_destroy)
        window.set_default_size(
            self.gstreamer_service.arguments.settings.get().width,
            self.gstreamer_service.arguments.settings.get().height)
        window.set_title('RCPiCar GTK Client')
        window.maximize()
        drawing_area = Gtk.DrawingArea()
        drawing_area.connect('draw', on_draw)
        window.add(drawing_area)
        window.connect('key-press-event', self.on_key_press_event)
        window.connect('key-release-event', self.on_key_release_event)
        window.show_all()
        self.xid.set(drawing_area.get_property('window').get_xid())
        Gtk.main()

    def on_reliable_connect(self, details: ConnectionDetails) -> None:
        with self.is_video_loading as (is_video_loading, set_is_video_loading):
            if not is_video_loading and not self.video_service_manager.is_service_running():
                self.gstreamer_service.open_video(details.own_address[0])
                set_is_video_loading(True)

    def on_video_available(self, caps: str, port: int) -> None:
        def run() -> None:
            """
            This function might block.
            """
            with self.is_video_loading as (_, set_is_video_loading):
                set_is_video_loading(False)
            self.video_service_manager.stop_all()
            xid = self.xid.get_eventually(self.service_manager).get_blocking()
            if xid is not None:
                GtkVideoService(
                    caps, self.gstreamer_service.arguments.flv_file_path.get(), port, self.video_service_manager, xid)
                self.video_service_manager.start_all()

        Thread(target=run).start()

    def on_key_press_event(self, widget: Any, event: Any) -> None:
        """
        see https://developer.gnome.org/gtk3/stable/GtkWidget.html#GtkWidget-key-press-event
        """
        command: Optional[Tuple[int, int]] = None
        keycode = SemanticKeycode(HardwareKeycode(event.hardware_keycode))
        with self.key_state as (key_state, _):
            if not key_state.is_key_pressed(keycode) and key_state.set_key_pressed(keycode, True):
                command = self.on_key_changed(key_state)
        if command is not None:
            self.car_service.update(*command)

    def on_key_release_event(self, widget: Any, event: Any) -> None:
        """
        see https://developer.gnome.org/gtk3/stable/GtkWidget.html#GtkWidget-key-release-event
        """
        command: Optional[Tuple[int, int]] = None
        keycode = SemanticKeycode(HardwareKeycode(event.hardware_keycode))
        with self.key_state as (key_state, _):
            if key_state.is_key_pressed(keycode) and key_state.set_key_pressed(keycode, False):
                command = self.on_key_changed(key_state)
        if command is not None:
            self.car_service.update(*command)

    @staticmethod
    def on_key_changed(key_state: KeyState) -> Tuple[int, int]:
        if key_state.brake:
            speed = 0
        elif key_state.forward:
            speed = 100
        elif key_state.backward:
            speed = -100
        else:
            speed = 0
        if key_state.left:
            steering = -100
        elif key_state.right:
            steering = 100
        else:
            steering = 0
        return speed, steering
