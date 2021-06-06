from __future__ import annotations
from typing import Optional
if True:  # Suppresses style warnings.
    from gi import require_version  # type: ignore
    require_version('Gst', '1.0')
    require_version('GstVideo', '1.0')
from gi.repository import GstVideo, Gst  # type: ignore
from logging import getLogger
from typing import Any
from rcpicar.service import AbstractService, AbstractServiceManager

Gst.init(None)
str(GstVideo)  # Marking GstVideo as used. Importing GstVideo is required for msg.src.set_window_handle!


class GtkVideoService(AbstractService):
    def __init__(
            self,
            caps: str,
            flv_file_path: Optional[str],
            port: int,
            service_manager: AbstractServiceManager,
            xid: int,
    ) -> None:
        super().__init__(service_manager)
        self.logger = getLogger(__name__)
        self.pipeline = Gst.Pipeline()
        self.xid = xid

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::error', self.on_video_pipeline_error)

        bus.enable_sync_message_emission()
        bus.connect('sync-message::element', self.on_sync_message)

        udp_src = Gst.ElementFactory.make('udpsrc', None)
        udp_src.set_property('port', port)
        self.pipeline.add(udp_src)

        caps_filter = Gst.ElementFactory.make('capsfilter', None)
        caps_filter.set_property('caps', Gst.Caps.from_string(caps))
        self.pipeline.add(caps_filter)
        udp_src.link(caps_filter)

        rtph264depay = Gst.ElementFactory.make('rtph264depay', None)
        self.pipeline.add(rtph264depay)
        caps_filter.link(rtph264depay)

        if flv_file_path is not None:
            tee = Gst.ElementFactory.make('tee', None)
            self.pipeline.add(tee)
            rtph264depay.link(tee)

            queue1 = Gst.ElementFactory.make('queue', None)
            self.pipeline.add(queue1)
            tee.link(queue1)

            flv_mux = Gst.ElementFactory.make('flvmux', None)
            self.pipeline.add(flv_mux)
            queue1.link(flv_mux)

            file_sink = Gst.ElementFactory.make('filesink', None)
            file_sink.set_property('location', flv_file_path)
            self.pipeline.add(file_sink)
            flv_mux.link(file_sink)

            queue2 = Gst.ElementFactory.make('queue', None)
            self.pipeline.add(queue2)
            tee.link(queue2)
            parent = queue2
        else:
            parent = rtph264depay

        avdec_h264 = Gst.ElementFactory.make('avdec_h264', None)
        self.pipeline.add(avdec_h264)
        parent.link(avdec_h264)

        video_convert = Gst.ElementFactory.make('videoconvert', None)
        self.pipeline.add(video_convert)
        avdec_h264.link(video_convert)

        auto_video_sink = Gst.ElementFactory.make('autovideosink', None)
        auto_video_sink.set_property('sync', False)
        self.pipeline.add(auto_video_sink)
        video_convert.link(auto_video_sink)

    def get_service_name(self) -> str:
        return __name__

    def join_service(self, timeout_seconds: Optional[float] = None) -> bool:
        return False

    def start_service(self) -> None:
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop_service(self) -> None:
        self.pipeline.set_state(Gst.State.NULL)

    def on_sync_message(self, bus: Any, msg: Any) -> None:
        if msg.get_structure().get_name() == 'prepare-window-handle':
            self.logger.info('on_sync_message(): prepare-window-handle')
            msg.src.set_property('force-aspect-ratio', True)
            msg.src.set_window_handle(self.xid)

    def on_video_pipeline_error(self, bus: Any, msg: Any) -> None:
        self.logger.error(f'on_video_pipeline_error(): {msg.parse_error()}')
