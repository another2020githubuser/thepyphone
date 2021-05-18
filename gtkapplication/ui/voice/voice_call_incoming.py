import logging
from timeit import default_timer
import pjsua2
from gtkapplication.ui.voice.base_voice_signal_handler import BaseVoiceSignalHandler
import gtkapplication.api.sip.pjsip_container_accessor
import gtkapplication.ui.gtk.jump_to_window
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gio,GLib
class InboundVoiceProcessor():
	def __init__(self,window_unique_key):
		self._logger=logging.getLogger(__name__)
		self._window_unique_key=window_unique_key
		glade_file_name="voice_ui.glade"
		self._gtk_builder=gtkapplication.ui.gtk.gtk_builder.GtkBuilder(__file__,glade_file_name)
		self.gtk_application_window=self._gtk_builder.get_object("voice_window")
		self.gtk_application_window.connect("delete-event",self._on_close)
		css_file="voice_call.css"
		css_parser=gtkapplication.ui.gtk.gtk_css.GtkCss()
		css_parser.load_and_apply_css(__file__,css_file)
		self._gtk_builder.connect_signals(self)
		self.gtk_application_window.connect("delete-event",self._on_close)
		self.gtk_application_window.show()
	def _on_close(self,*args):
		self._logger.debug('entered onclose, args count = %d',len(args))
		if self._window_unique_key is None:
			self._logger.debug('self._window_unique_key is None, skipping remove_window_from_cache and quitting gtk')
			Gtk.main_quit()
		else:
			stateful_object_accessor=gtkapplication.ui.gtk.window_state_accessor.WindowStateAccessor()
			stateful_object_accessor.remove_window_from_cache(self._window_unique_key)
			self._logger.debug('after remove_window_from_cache')
			self.gtk_application_window.destroy()
			self._logger.debug('window.destroy() called')