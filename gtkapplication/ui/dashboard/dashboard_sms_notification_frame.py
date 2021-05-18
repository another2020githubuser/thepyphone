import logging
import os.path
from gtkapplication.ui.dashboard.dashboard_sms_notification_signal_handler import DashboardSmsNotificationSignalHandler
class FrameFactory:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._datetimeformatstring="%a %b %d, %I:%M %p"
	def create_free_buddy_text_notification_ui_item(self,gtk_builder,sms_dto):
		self._logger.debug("entered create_free_buddy_text_notification_ui_item")
		glade_file_name="dashboard_sms_notification_frame.glade"
		gtk_builder.add_from_file(__file__,glade_file_name)
		contact_point=sms_dto.contact.contact_points[sms_dto.active_contact_point_index]
		assert contact_point.point_type=="x-sip"
		if contact_point.description!="PyPhone Buddy":
			self._logger.debug("unexpected contact_point.description = '%s'",contact_point.description)
		assert len(sms_dto.mms_links)==0
		datetime_label=gtk_builder.get_object("datetime_label")
		datetime_label.set_text(sms_dto.timestamp.strftime(self._datetimeformatstring))
		label_text="New Free Buddy Text from\n{0}".format(sms_dto.contact.name)
		sms_from_label=gtk_builder.get_object("new_sms_label")
		sms_from_label.set_text(label_text)
		sms_content_label=gtk_builder.get_object("sms_content_label")
		sms_content_label.set_text(sms_dto.content)
		sms_button=gtk_builder.get_object("sms_button")
		sms_button.set_label("Text")
		frame=gtk_builder.get_object("sms_notification_frame")
		container=gtk_builder.get_object("notification_box")
		signal_hander=DashboardSmsNotificationSignalHandler(container,sms_dto,sms_dto.active_contact_point_index)
		gtk_builder.connect_signals(signal_hander)
		return frame
	def create_sms_notification_ui_item(self,gtk_builder,sms_dto):
		self._logger.debug("entered create_sms_notification_ui_item")
		glade_file_name="dashboard_sms_notification_frame.glade"
		gtk_builder.add_from_file(__file__,glade_file_name)
		datetime_label=gtk_builder.get_object("datetime_label")
		datetime_label.set_text(sms_dto.timestamp.strftime(self._datetimeformatstring))
		contact_point=sms_dto.contact.contact_points[sms_dto.active_contact_point_index]
		num_attachments=len(sms_dto.mms_links)
		if num_attachments>0:
			label_text="New SMS from\n{0}\n{1} {2}\n{3} Attachment(s)".format(sms_dto.contact.name,contact_point.description,contact_point.uri_string_national,num_attachments)
		else:
			label_text="New SMS from\n{0}\n{1} {2}".format(sms_dto.contact.name,contact_point.description,contact_point.uri_string_national)
		sms_from_label=gtk_builder.get_object("new_sms_label")
		sms_from_label.set_text(label_text)
		sms_content_label=gtk_builder.get_object("sms_content_label")
		sms_content_label.set_text(sms_dto.content)
		frame=gtk_builder.get_object("sms_notification_frame")
		container=gtk_builder.get_object("notification_box")
		signal_hander=DashboardSmsNotificationSignalHandler(container,sms_dto,sms_dto.active_contact_point_index)
		gtk_builder.connect_signals(signal_hander)
		return frame