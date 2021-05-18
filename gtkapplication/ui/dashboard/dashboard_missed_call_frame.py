import logging
import os.path
import datetime
from gtkapplication.ui.dashboard.dashboard_missed_call_signal_handler import DashboardMissedCallSignalHandler
class FrameFactory:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._datetimeformatstring="%a %b %d, %I:%M %p"
	def create_missed_call_frame(self,gtk_builder,contact,active_contact_point_index):
		self._logger.debug("entered _create_missed_call_frame")
		glade_file_name="dashboard_missed_call_frame.glade"
		gtk_builder.add_from_file(__file__,glade_file_name)
		frame=gtk_builder.get_object('frame_missed_call')
		datetime_label=gtk_builder.get_object("datetime_label")
		datetime_label.set_text(datetime.datetime.now().strftime(self._datetimeformatstring))
		missed_call_label=gtk_builder.get_object("missed_call_label")
		contact_point=contact.contact_points[active_contact_point_index]
		label_text=""
		if contact_point.point_type=="x-sip":
			label_text="Missed Free Buddy call from\n{0}".format(contact.name)
		elif contact_point.point_type=="tel":
			label_text="Missed call from\n{0}\n{1} {2}".format(contact.name,contact_point.description,contact_point.uri_string_national)
		else:
			assert contact_point.point_type in ["x-sip","tel"]
		missed_call_label.set_text(label_text)
		notification_box=gtk_builder.get_object("notification_box")
		signal_handler=DashboardMissedCallSignalHandler(notification_box,contact,active_contact_point_index)
		gtk_builder.connect_signals(signal_handler)
		return frame