import logging
import datetime
from gtkapplication.ui.dashboard.dashboard_sms_delivery_failure_signal_handler import DashboardSmsDeliveryFailureSignalHandler
import gtkapplication.api.sip.inbound.sms_delivery_failure_processor
class FrameFactory:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._datetimeformatstring="%a %b %d, %I:%M %p"
	def create_sms_delivery_failure_frame(self,gtk_builder,sms_delivery_failure_dto):
		self._logger.debug("entered create_sms_delivery_failure_frame")
		assert isinstance(sms_delivery_failure_dto,gtkapplication.api.sip.inbound.sms_delivery_failure_processor.SmsDeliveryFailureDto)
		glade_file_name="dashboard_sms_delivery_failure_frame.glade"
		gtk_builder.add_from_file(__file__,glade_file_name)
		frame=gtk_builder.get_object('frame_sms_delivery_failure')
		datetime_label=gtk_builder.get_object("datetime_label")
		datetime_label.set_text(datetime.datetime.now().strftime(self._datetimeformatstring))
		announcement_label=gtk_builder.get_object("announcement_label")
		contact=sms_delivery_failure_dto.contact
		active_contact_point_index=sms_delivery_failure_dto.active_contact_point_index
		contact_point=contact.contact_points[active_contact_point_index]
		label_text="SMS Delivery Failed with Error\n'{0}'\nError Code {1}\n{2} {3}".format(sms_delivery_failure_dto.error_message,sms_delivery_failure_dto.error_code,contact.name,contact_point.uri_string_national)
		announcement_label.set_text(label_text)
		message_body_label=gtk_builder.get_object("message_body_label")
		message_body_label.set_text(sms_delivery_failure_dto.body)
		notification_box=gtk_builder.get_object("notification_box")
		signal_handler=DashboardSmsDeliveryFailureSignalHandler(notification_box,sms_delivery_failure_dto)
		gtk_builder.connect_signals(signal_handler)
		return frame