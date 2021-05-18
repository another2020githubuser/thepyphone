import logging
import pkg_resources
import gtkapplication.ui.xwindows.wmctrl3
import gtkapplication.ui.gtk.window_manager
import gtkapplication.ui.diagnostics.diagnostics_ui
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gio
class GtkAppActions:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def show_about_dialog(self):
		self._logger.debug("entered show_about_dialog")
		version=pkg_resources.require("gtkapplication")[0].version
		dialog_main_text="PyPhone Version: {0}".format(version)
		phone_number=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
		self._logger.debug("phone_number = %s",phone_number)
		dialog_secondary_text="Phone Number is {0}".format(phone_number)
		dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,dialog_main_text)
		dialog.set_title("About The PyPhone")
		dialog.format_secondary_text(dialog_secondary_text)
		dialog.run()
		dialog.destroy()
	def show_contacts_window(self):
		self._logger.debug("entered show_contacts_window")
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		window_manager.get_contacts_window()
	def show_diagnostic_dialog(self):
		self._logger.debug("entered show_diagnostic_dialog")
		ui=gtkapplication.ui.diagnostics.diagnostics_ui.DiagnosticsUi()
		ui.showme()
	def show_dashboard(self):
		self._logger.debug("entered show_dashboard")
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		window_manager.get_dashboard_window()
	def show_dialpad(self):
		self._logger.debug("entered show_dialpad")
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		window_manager.get_keypad_window()