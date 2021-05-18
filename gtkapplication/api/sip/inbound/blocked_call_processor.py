import logging
import gtkapplication.api.contacts.contact_manager
import gtkapplication.api.sip.business_layer
import gtkapplication.api.audio.ringer
import gtkapplication.ui.gtk.window_manager
import gtkapplication.api.contacts
class InboundProcessor:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def process_blocked_call_message(self,message_body):
		self._logger.debug("entered process_missed_call_message")
		assert isinstance(message_body,str)
		message_lines=message_body.split('\n')
		assert len(message_lines)==2
		from_phone_number=message_lines[1].split('=')[1]
		self._logger.debug("from_phone_number = %s",from_phone_number)
		db=gtkapplication.api.sip.business_layer.BusinessLayer()
		db.insert_blocked_call_message(from_phone_number)
		self._logger.debug("after db insert_blocked_call_message()")
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		dashboard_ui=window_manager.get_dashboard_window()
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		(contact,active_contact_point_index)=contact_manager.find_contact_by_phone_number(from_phone_number,True)
		dashboard_ui.add_blocked_call_notification(contact,active_contact_point_index)