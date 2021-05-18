import logging
import datetime
from gtkapplication.ui.dashboard.dashboard_sms_delivery_failure_signal_handler import DashboardSmsDeliveryFailureSignalHandler
import gtkapplication.api.sip.free_buddy_text_delivery_failure
class FrameFactory:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._datetimeformatstring="%a %b %d, %I:%M %p"
	def create_free_buddy_text_delivery_failure_frame(self,gtk_builder,free_buddy_text_delivery_failure_dto):
		self._logger.debug("entered create_sms_delivery_failure_frame")
		assert isinstance(free_buddy_text_delivery_failure_dto,gtkapplication.api.sip.free_buddy_text_delivery_failure.FreeBuddyTextDeliveryFailureDto)
		glade_file_name="dashboard_sms_delivery_failure_frame.glade"
		gtk_builder.add_from_file(__file__,glade_file_name)
		frame=gtk_builder.get_object('frame_sms_delivery_failure')
		datetime_label=gtk_builder.get_object("datetime_label")
		datetime_label.set_text(datetime.datetime.now().strftime(self._datetimeformatstring))
		announcement_label=gtk_builder.get_object("announcement_label")
		contact=free_buddy_text_delivery_failure_dto.contact
		active_contact_point_index=free_buddy_text_delivery_failure_dto.active_contact_point_index
		label_text="Free Buddy Text Failed with Error\n'{0}'\nError Code {1}\n{2}".format(free_buddy_text_delivery_failure_dto.on_instant_message_status_param.reason,free_buddy_text_delivery_failure_dto.on_instant_message_status_param.code,contact.name)
		announcement_label.set_text(label_text)
		message_body_label=gtk_builder.get_object("message_body_label")
		message_body_label.set_text(free_buddy_text_delivery_failure_dto.on_instant_message_status_param.msgBody)
		notification_box=gtk_builder.get_object("notification_box")
		signal_handler=DashboardSmsDeliveryFailureSignalHandler(notification_box,free_buddy_text_delivery_failure_dto)
		gtk_builder.connect_signals(signal_handler)
		return frame