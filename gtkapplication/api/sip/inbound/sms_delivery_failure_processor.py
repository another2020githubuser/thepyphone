import logging
import gtkapplication.api.contacts.contact_manager
import gtkapplication.api.sip.business_layer
import gtkapplication.api.audio.ringer
import gtkapplication.ui.gtk.window_manager
import gtkapplication.api.contacts
import gtkapplication.api.twilio.sms_command
class SmsDeliveryFailureDto:
	def __init__(self,contact,active_contact_point_index,body,error_code,error_message):
		self._logger=logging.getLogger(__name__)
		self._contact=contact
		self._active_contact_point_index=active_contact_point_index
		self._body=body
		self._error_code=error_code
		self._error_message=error_message
	@property
	def contact(self):
		return self._contact
	@property
	def active_contact_point_index(self):
		return self._active_contact_point_index
	@property
	def body(self):
		return self._body
	@property
	def error_code(self):
		return self._error_code
	@property
	def error_message(self):
		return self._error_message
class InboundProcessor:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def process_sms_delivery_failure(self,message_body):
		self._logger.debug("entered process_sms_delivery_failure")
		assert isinstance(message_body,str)
		message_lines=message_body.split('\n')
		assert len(message_lines)==3
		sid=message_lines[1].split('=')[1]
		status=message_lines[2].split('=')[1]
		self._logger.debug("sid = %s",sid)
		self._logger.debug("status = %s",status)
		sms_command=gtkapplication.api.twilio.sms_command.SmsCommand()
		twilio_message=sms_command.get_message_by_sid(sid)
		assert twilio_message is not None
		db=gtkapplication.api.sip.business_layer.BusinessLayer()
		row_id=db.insert_or_replace_twilio_message_instance(twilio_message)
		self._logger.debug("after db insert_twilio_message_instance(), row_id = %s",row_id)
		gtkapplication.api.audio.ringer.start_ringer()
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		dashboard_ui=window_manager.get_dashboard_window()
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		(contact,active_contact_point_index)=contact_manager.find_contact_by_phone_number(twilio_message.to,True)
		sms_delivery_failure_dto=SmsDeliveryFailureDto(contact,active_contact_point_index,twilio_message.body,twilio_message.error_code,twilio_message.error_message)
		dashboard_ui.add_sms_delivery_failure_notification(sms_delivery_failure_dto)