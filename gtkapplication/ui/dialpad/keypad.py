import logging
import gtkapplication.ui.gtk.gtk_dialog
import gtkapplication.ui.gtk.window_manager
import gtkapplication.ui.gtk.gtk_builder
import gtkapplication.api.contacts.contact
import gtkapplication.api.contacts.contact_manager
import gtkapplication.ui.gtk.gtk_menubar_css
import gtkapplication.ui.gtk.gtk_style
import gtkapplication.ui.dialpad.keypad_signal_handler
import gtkapplication.api.sip.dtmf_tone
import gtkapplication.ui.gtk.jump_to_window
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class KeypadUi:
	def __init__(self,window_unique_key):
		self._logger=logging.getLogger(__name__)
		self.gtk_application_window=None
		self._window_unique_key=window_unique_key
		glade_file_name="keypad.glade"
		self._gtk_builder=gtkapplication.ui.gtk.gtk_builder.GtkBuilder(__file__,glade_file_name)
		signal_handler=gtkapplication.ui.dialpad.keypad_signal_handler.KeypadSignalHandler(self._gtk_builder,self._onclose)
		self._gtk_builder.connect_signals(signal_handler)
		self._phone_number_entry=self._gtk_builder.get_object("phone_number_entry")
		self.gtk_application_window=self._gtk_builder.get_object('keypad_window')
		self._logger.debug('got window')
		css_file="keypad.css"
		css_parser=gtkapplication.ui.gtk.gtk_css.GtkCss()
		css_parser.load_and_apply_css(__file__,css_file)
		jump_to_window=gtkapplication.ui.gtk.jump_to_window.JumpToWindowHelper(self._gtk_builder)
		self._logger.debug("after jump_to_window()")
	def showme(self):
		self._logger.debug('enter showme')
		self.gtk_application_window.connect("delete-event",self._onclose)
		self.gtk_application_window.show_all()
		self._logger.debug('window shown')
		window_size=self.gtk_application_window.get_size()
		self._logger.debug("window_size = %s",window_size)
		if window_size!=(400,479):
			self._logger.warning("unexpected window size: %s",self.gtk_application_window.get_size())
	def _onclose(self,*args):
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