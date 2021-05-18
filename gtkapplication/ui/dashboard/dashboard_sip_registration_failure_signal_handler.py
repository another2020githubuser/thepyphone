import logging
import gtkapplication.ui.gtk.window_manager
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class SipRegistrationFailureSignalHandler:
	def __init__(self,notification_box):
		self._logger=logging.getLogger(__name__)
		self._notification_box=notification_box
	def on_close_button_click(self,frame,user_data):
		self._logger.debug("entered on_close_button_click")
		assert isinstance(frame,Gtk.Frame)
		self._notification_box.remove(frame)