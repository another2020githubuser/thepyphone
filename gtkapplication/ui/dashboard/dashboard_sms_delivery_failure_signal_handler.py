import logging
import gtkapplication.ui.gtk.window_manager
class DashboardSmsDeliveryFailureSignalHandler:
	def __init__(self,notification_box,sms_delivery_failure_dto):
		self._logger=logging.getLogger(__name__)
		self._notification_box=notification_box
		self._sms_delivery_failure_dto=sms_delivery_failure_dto
	def on_retry_button_clicked(self,button):
		self._logger.debug('entered on_retry_button_click')
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		contact=self._sms_delivery_failure_dto.contact
		self._logger.debug('contact = %s',contact)
		active_contact_point_index=self._sms_delivery_failure_dto.active_contact_point_index
		self._logger.debug('active_contact_point_index = %s',active_contact_point_index)
		message=self._sms_delivery_failure_dto.on_instant_message_status_param.msgBody
		self._logger.debug('message = %s',message)
		sms_window=window_manager.get_sms_window(contact,active_contact_point_index,message)
		self._logger.debug("after get_sms_window()")
		sms_window.send_sms(contact,active_contact_point_index,message)
		self._logger.debug("after sms_window.send_sms()")