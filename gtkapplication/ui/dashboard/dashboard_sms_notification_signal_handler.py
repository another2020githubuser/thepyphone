import logging
import gtkapplication.ui.gtk.window_manager
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class DashboardSmsNotificationSignalHandler:
	def __init__(self,container,sms_dto,active_contact_point_index):
		self._logger=logging.getLogger(__name__)
		self._container=container
		self._sms_dto=sms_dto
		self._active_contact_point_index=active_contact_point_index
	def on_close_button_click(self,frame,user_data):
		self._logger.debug("entered on_close_button_click")
		assert isinstance(frame,Gtk.Frame)
		self._container.remove(frame)
	def on_sms_button_clicked(self,button):
		self._logger.debug("entered on_sms_button_clicked")
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		window_manager.get_sms_window(self._sms_dto.contact,self._active_contact_point_index,True)
	def on_call_button_clicked(self,button):
		self._logger.debug("entered on_call_button_clicked")
		self._logger.debug("contact is %s, contact_point is %s",self._sms_dto.contact,self._active_contact_point_index)
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		voice_window=window_manager.get_voice_window()
		voice_window.add_outgoing_call(self._sms_dto.contact,self._active_contact_point_index)