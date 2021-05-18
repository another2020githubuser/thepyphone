import logging
import gtkapplication.ui.dashboard.dashboard_free_buddy_text_delivery_failure_frame
class FreeBuddyTextDeliveryFailureDto:
	def __init__(self,contact,active_contact_point_index,on_instant_message_status_param):
		self._logger=logging.getLogger(__name__)
		self._contact=contact
		self._active_contact_point_index=active_contact_point_index
		self._on_instant_message_status_param=on_instant_message_status_param
	@property
	def contact(self):
		return self._contact
	@property
	def active_contact_point_index(self):
		return self._active_contact_point_index
	@property
	def on_instant_message_status_param(self):
		return self._on_instant_message_status_param
class FreeBuddyTextDeliveryFailureProcessor:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def process_sip_text_delivery_failure(self,on_instant_message_status_param):
		self._logger.debug('entered process_im_delivery_failure')
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		(contact,active_contact_point_index)=contact_manager.find_contact_by_sip_uri(on_instant_message_status_param.toUri,True)
		business_layer=gtkapplication.api.sip.business_layer.BusinessLayer()
		sms_delvery_failure_row_id=business_layer.insert_free_buddy_text_delivery_failure_message(on_instant_message_status_param.toUri,on_instant_message_status_param.msgBody,on_instant_message_status_param.reason,on_instant_message_status_param.code)
		self._logger.debug("after db insert_im_delivery_failure(), sms_delvery_failure_row_id = %d",sms_delvery_failure_row_id)
		free_buddy_text_delivery_failure_dto=FreeBuddyTextDeliveryFailureDto(contact,active_contact_point_index,on_instant_message_status_param)
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		dashboard_ui=window_manager.get_dashboard_window()
		dashboard_ui.add_free_buddy_text_delivery_failure_notification(free_buddy_text_delivery_failure_dto)
		gtkapplication.api.audio.ringer.start_ringer()