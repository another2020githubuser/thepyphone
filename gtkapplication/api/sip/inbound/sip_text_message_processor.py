import logging
import datetime
import gtkapplication.api.contacts.contact_manager
import gtkapplication.api.sip.business_layer
import gtkapplication.api.audio.ringer
import gtkapplication.ui.gtk.window_manager
import gtkapplication.api.contacts
from gtkapplication.ui.sms import SmsDirection
class InboundProcessor:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def process_sip_text_message(self,prm):
		self._logger.debug("Entered process_sip_text_message")
		self._logger.debug("prm.fromUri = %s",prm.fromUri)
		self._logger.debug("prm.toUri = %s",prm.toUri)
		self._logger.debug("prm.msgBody = %s",prm.msgBody)
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		(contact,active_contact_point_index)=contact_manager.find_contact_by_sip_uri(prm.fromUri,True)
		self._logger.debug("after find_contact_by_sip_uri")
		db_access=gtkapplication.api.sip.business_layer.BusinessLayer()
		db_access.insert_sms_message(prm.fromUri,prm.msgBody,SmsDirection.RECEIVED)
		self._logger.debug("after db.insert_sms_message")
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		if len(gtkapplication.api.sip.sip_call_state.sip_calls)==0:
			self._logger.debug("no current call, making sms window present")
			sms_window=window_manager.get_sms_window(contact,active_contact_point_index,True)
			dashboard_ui=window_manager.get_dashboard_window(True)
			sms_window.display_sms(prm.msgBody,SmsDirection.RECEIVED,datetime.datetime.now())
			self._logger.debug("after sms_window.display_sms")
			sms_dto=gtkapplication.ui.sms.SmsDto(datetime.datetime.now(),contact,prm.msgBody,[],active_contact_point_index)
			dashboard_ui.add_new_free_buddy_text_notification(sms_dto)
			gtkapplication.api.audio.ringer.start_ringer()
			self._logger.debug("after gtkapplication.api.audio.ringer.start_ringer()")
		else:
			self._logger.debug("current sip call, NOT making windows present")
			sms_window=window_manager.get_sms_window(contact,active_contact_point_index,False)
			dashboard_ui=window_manager.get_dashboard_window(False)
			sms_window.display_sms(prm.msgBody,SmsDirection.RECEIVED,datetime.datetime.now())
			self._logger.debug("after sms_window.display_sms")
			sms_dto=gtkapplication.ui.sms.SmsDto(datetime.datetime.now(),contact,prm.msgBody,[],active_contact_point_index)
			dashboard_ui.add_new_free_buddy_text_notification(sms_dto)
			self._logger.debug("after dashboard_ui.add_new_free_buddy_text_notification")
			window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
			window_manager.get_contacts_window()