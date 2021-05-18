import logging
import gtkapplication.api.sip.business_layer
import gtkapplication.ui.gtk.window_manager
import gtkapplication.api.sip.sip_registration_failure_dto
class InboundProcessor:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def process_sip_registration_failure(self,account_id,account_uri,status,reason,code):
		self._logger.debug("Entered process_sip_registration_failure")
		db=gtkapplication.api.sip.business_layer.BusinessLayer()
		db.insert_sip_registration_failure_message(account_id,account_uri,status,reason,code)
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		dashboard_ui=window_manager.get_dashboard_window()
		dto=gtkapplication.api.sip.sip_registration_failure_dto.SipRegistrationFailureDto(account_id,account_uri,status,reason,code)
		dashboard_ui.add_sip_registration_failure(dto)