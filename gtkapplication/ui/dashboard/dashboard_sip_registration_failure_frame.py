import logging
import os.path
import datetime
from gtkapplication.ui.dashboard.dashboard_sip_registration_failure_signal_handler import SipRegistrationFailureSignalHandler
class FrameFactory:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._datetimeformatstring="%a %b %d, %I:%M %p"
	def create_sip_registration_failure_frame(self,gtk_builder,sip_registration_failure_dto):
		self._logger.debug("entered _create_sip_registration_failure_frame")
		glade_file_name="dashboard_sip_registration_failure_frame.glade"
		gtk_builder.add_from_file(__file__,glade_file_name)
		frame=gtk_builder.get_object('frame_sip_registration_failure')
		datetime_label=gtk_builder.get_object("datetime_label")
		datetime_label.set_text(datetime.datetime.now().strftime(self._datetimeformatstring))
		sip_registration_failure_label=gtk_builder.get_object("sip_registration_failure_label")
		sip_registration_failure_label.set_text("Sip Registration Failure\nDetails: {0}".format(sip_registration_failure_dto))
		notification_box=gtk_builder.get_object("notification_box")
		signal_handler=SipRegistrationFailureSignalHandler(notification_box)
		gtk_builder.connect_signals(signal_handler)
		return frame