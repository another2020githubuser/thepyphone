import logging
import gtkapplication.ui.gtk.window_manager
import gtkapplication.ui.gtk.jump_to_window
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class DashboardUiSignalHandler:
	def __init__(self,gtk_menu,gtk_builder):
		self._logger=logging.getLogger(__name__)
		self._gtk_menu=gtk_menu
		self._gtk_builder=gtk_builder
	def on_jump_menu_button_toggled(self,button):
		self._logger.debug("entered on_jump_menu_button_toggled, is_active = %s",button.get_active())
		if button.get_active():
			jump_to_window=gtkapplication.ui.gtk.jump_to_window.JumpToWindowHelper(self._gtk_builder)
			self._logger.debug("after jump_to_window()")
			button.show_all()
	def on_menu_activate(self,menu_item):
		self._logger.debug("entered on_menu_activate")
		sms_window_key=menu_item.get_label()
		self._logger.debug("sms_window_key = %s",sms_window_key)
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		window_manager.present_sms_window_by_key(sms_window_key)