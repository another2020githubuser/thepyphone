import logging
import os.path
import datetime
from gtkapplication.ui.dashboard.dashboard_blocked_call_signal_handler import DashboardBlockedCallSignalHandler
class FrameFactory:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._datetimeformatstring="%a %b %d, %I:%M %p"
	def create_blocked_call_frame(self,gtk_builder,contact,active_contact_point_index):
		self._logger.debug("entered _create_blocked_call_frame")
		glade_file_name="dashboard_blocked_call_frame.glade"
		gtk_builder.add_from_file(__file__,glade_file_name)
		frame=gtk_builder.get_object('frame_blocked_call')
		datetime_label=gtk_builder.get_object("datetime_label")
		datetime_label.set_text(datetime.datetime.now().strftime(self._datetimeformatstring))
		blocked_call_label=gtk_builder.get_object("blocked_call_label")
		contact_point=contact.contact_points[active_contact_point_index]
		label_text="Call Blocked from '{0}'".format(contact_point.uri_string)
		blocked_call_label.set_text(label_text)
		notification_box=gtk_builder.get_object("notification_box")
		signal_handler=DashboardBlockedCallSignalHandler(notification_box,contact,active_contact_point_index)
		gtk_builder.connect_signals(signal_handler)
		return frame