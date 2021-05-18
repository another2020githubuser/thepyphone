import logging
import gtkapplication.ui.gtk.window_manager
import pjsua2
import gtkapplication.api.sip.pjsip_container_accessor
class ContactPointSignalHandler:
	def __init__(self,contact,active_contact_point_index):
		self._logger=logging.getLogger(__name__)
		self._contact=contact
		self._active_contact_point_index=active_contact_point_index
	def on_sms_button_clicked(self,button):
		self._logger.debug("entered on_sms_button_clicked")
		contact_point=self._contact.contact_points[self._active_contact_point_index]
		self._logger.debug("contact is %s, contact_point is %s",self._contact,contact_point)
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		window_manager.get_sms_window(self._contact,self._active_contact_point_index,True)
	def on_call_button_clicked(self,button):
		self._logger.debug("entered on_call_button_clicked")
		self._logger.debug("contact is %s, contact_point is %s",self._contact,self._contact.contact_points[self._active_contact_point_index])
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		voice_window=window_manager.get_voice_window()
		voice_window.add_outgoing_call(self._contact,self._active_contact_point_index)