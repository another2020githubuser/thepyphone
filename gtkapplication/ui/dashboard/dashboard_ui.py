import logging
import gtkapplication.data.config_data
import gtkapplication.ui.gtk.gtk_builder
import gtkapplication.ui.gtk.window_manager
import gtkapplication.ui.gtk.gtk_css
import gtkapplication.ui.dashboard.dashboard_missed_call_frame
import gtkapplication.ui.voicemail.dashboard_voicemail_frame
from gtkapplication.ui.dashboard.dashboard_ui_signal_handler import DashboardUiSignalHandler
import gtkapplication.ui.dashboard.dashboard_sms_notification_frame
import gtkapplication.ui.dashboard.dashboard_sip_registration_failure_frame
import gtkapplication.ui.dashboard.dashboard_blocked_call_frame
import gtkapplication.ui.dashboard.dashboard_blocked_sms_frame
import gtkapplication.ui.dashboard.dashboard_sms_delivery_failure_frame
import gtkapplication.ui.gtk.jump_to_window
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class DashboardUI():
	def __init__(self,window_unique_key):
		self._logger=logging.getLogger(__name__)
		glade_file_name="dashboard_ui.glade"
		self._gtk_builder=gtkapplication.ui.gtk.gtk_builder.GtkBuilder(__file__,glade_file_name)
		self._menu_button=self._gtk_builder.get_object("menu_button")
		self._gtk_menu=self._gtk_builder.get_object("gtk_menu")
		dashboard_signal_handler=DashboardUiSignalHandler(self._gtk_menu,self._gtk_builder)
		self._gtk_builder.connect_signals(dashboard_signal_handler)
		self.gtk_application_window=self._gtk_builder.get_object('main_window')
		self.gtk_application_window.connect("delete-event",self._onclose)
		self._logger.debug('got window')
		my_phone_number_national=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number_national']
		contact_label_text="My Phone Number: {0}".format(my_phone_number_national)
		self._gtk_builder.get_object("contact_label").set_text(contact_label_text)
		self._notification_box=self._gtk_builder.get_object("notification_box")
		self._window_unique_key=window_unique_key
		self._datetimeformatstring="%a %b %d, %I:%M %p"
		jump_to_window=gtkapplication.ui.gtk.jump_to_window.JumpToWindowHelper(self._gtk_builder)
	def showme(self):
		self._logger.debug('enter showme')
		css_file="dashboard_ui.css"
		css_parser=gtkapplication.ui.gtk.gtk_css.GtkCss()
		css_parser.load_and_apply_css(__file__,css_file)
		self.gtk_application_window.show_all()
		self._logger.debug('window shown')
		self._logger.debug("window size = %s",self.gtk_application_window.get_size())
		if self.gtk_application_window.get_size()!=(800,480):
			self._logger.warning("Unexpected window size: %s",self.gtk_application_window.get_size())
		self._logger.debug('exit showme')
	def _onclose(self,*args):
		self._logger.debug("entered onclose with %d args",len(args))
		if self._window_unique_key is None:
			self._logger.debug('self._window_unique_key is None, skipping remove_window_from_cache')
			Gtk.main_quit()
		else:
			stateful_object_accessor=gtkapplication.ui.gtk.window_state_accessor.WindowStateAccessor()
			stateful_object_accessor.remove_window_from_cache(self._window_unique_key)
			self.gtk_application_window.destroy()
	def add_new_sms_notification(self,sms_dto):
		self._logger.debug("entered add_new_sms_notification")
		assert isinstance(sms_dto,gtkapplication.ui.sms.SmsDto)
		self._create_sms_notification(sms_dto)
	def add_new_free_buddy_text_notification(self,sms_dto):
		self._logger.debug("entered add_new_free_buddy_text_notification")
		assert isinstance(sms_dto,gtkapplication.ui.sms.SmsDto)
		self._create_free_buddy_text_notification(sms_dto)
	def add_new_voicemail_notification(self,recording_dto,contact,active_contact_point_index):
		self._logger.debug("entered add_new_voicemail_notification")
		assert isinstance(recording_dto,gtkapplication.api.twilio.RecordingDto)
		self._create_voicemail_ui_item(recording_dto,contact,active_contact_point_index)
	def add_missed_call_notification(self,contact,active_contact_point_index):
		self._logger.debug("entered add_missed_call_notification")
		assert isinstance(contact,gtkapplication.api.contacts.contact.Contact)
		self._logger.debug("contact = %s",contact)
		self._create_missed_call_ui_item(contact,active_contact_point_index)
	def add_blocked_call_notification(self,contact,active_contact_point_index):
		self._logger.debug("entered add_blocked_call_notification")
		assert isinstance(contact,gtkapplication.api.contacts.contact.Contact)
		self._create_blocked_call_ui_item(contact,active_contact_point_index)
	def add_blocked_sms_notification(self,contact,active_contact_point_index):
		self._logger.debug("entered add_blocked_sms_notification")
		assert isinstance(contact,gtkapplication.api.contacts.contact.Contact)
		self._create_blocked_sms_ui_item(contact,active_contact_point_index)
	def add_sip_registration_failure(self,sip_registration_failure_dto):
		self._logger.debug("entered add_sip_registration_failure")
		self._create_sip_registration_failure_ui_item(sip_registration_failure_dto)
	def add_free_buddy_text_delivery_failure_notification(self,free_buddy_text_delivery_failure_dto):
		self._logger.debug("entered add_free_buddy_text_delivery_failure_notification")
		self._create_free_buddy_text_delivery_failure_notifiction_ui_item(free_buddy_text_delivery_failure_dto)
	def add_sms_delivery_failure_notification(self,sms_delivery_failure_dto):
		self._logger.debug("entered add_sms_delivery_failure_notification")
		self._create_sms_delivery_failure_ui_item(self._gtk_builder,sms_delivery_failure_dto)
	def _create_sms_notification(self,sms_dto):
		self._logger.debug("entered _create_sms_notification")
		frame_factory=gtkapplication.ui.dashboard.dashboard_sms_notification_frame.FrameFactory()
		frame=frame_factory.create_sms_notification_ui_item(self._gtk_builder,sms_dto)
		self._notification_box.pack_end(frame,False,False,0)
	def _create_free_buddy_text_notification(self,sms_dto):
		self._logger.debug("entered _create_sms_notification")
		frame_factory=gtkapplication.ui.dashboard.dashboard_sms_notification_frame.FrameFactory()
		frame=frame_factory.create_free_buddy_text_notification_ui_item(self._gtk_builder,sms_dto)
		self._notification_box.pack_end(frame,False,False,0)
	def _create_voicemail_ui_item(self,recording_dto,contact,active_contact_point_index):
		self._logger.debug("entered _create_voicemail_ui_item")
		frame_factory=gtkapplication.ui.voicemail.dashboard_voicemail_frame.FrameFactory()
		gtk_window=self._gtk_builder.get_object("main_window")
		frame=frame_factory.create_voicemail_frame(self._gtk_builder,recording_dto,contact,active_contact_point_index,gtk_window)
		self._notification_box.pack_end(frame,False,False,0)
	def _create_missed_call_ui_item(self,contact,active_contact_point_index):
		self._logger.debug("entered _create_missed_call_ui_item")
		frame_factory=gtkapplication.ui.dashboard.dashboard_missed_call_frame.FrameFactory()
		frame=frame_factory.create_missed_call_frame(self._gtk_builder,contact,active_contact_point_index)
		self._notification_box.pack_end(frame,False,False,0)
	def _create_blocked_call_ui_item(self,contact,active_contact_point_index):
		self._logger.debug("entered _create_blocked_call_ui_item")
		frame_factory=gtkapplication.ui.dashboard.dashboard_blocked_call_frame.FrameFactory()
		frame=frame_factory.create_blocked_call_frame(self._gtk_builder,contact,active_contact_point_index)
		self._notification_box.pack_end(frame,False,False,0)
	def _create_blocked_sms_ui_item(self,contact,active_contact_point_index):
		self._logger.debug("entered _create_blocked_sms_ui_item")
		frame_factory=gtkapplication.ui.dashboard.dashboard_blocked_sms_frame.FrameFactory()
		frame=frame_factory.create_blocked_sms_frame(self._gtk_builder,contact,active_contact_point_index)
		self._notification_box.pack_end(frame,False,False,0)
	def _create_sip_registration_failure_ui_item(self,sip_registration_failure_dto):
		self._logger.debug("entered _create_sip_registration_failure_ui_item")
		frame_factory=gtkapplication.ui.dashboard.dashboard_sip_registration_failure_frame.FrameFactory()
		frame=frame_factory.create_sip_registration_failure_frame(self._gtk_builder,sip_registration_failure_dto)
		self._notification_box.pack_end(frame,False,False,0)
	def _create_free_buddy_text_delivery_failure_notifiction_ui_item(self,free_buddy_text_delivery_failure_dto):
		frame_factory=gtkapplication.ui.dashboard.dashboard_free_buddy_text_delivery_failure_frame.FrameFactory()
		frame=frame_factory.create_free_buddy_text_delivery_failure_frame(self._gtk_builder,free_buddy_text_delivery_failure_dto)
		self._notification_box.pack_end(frame,False,False,0)
	def _create_sms_delivery_failure_ui_item(self,gtk_builder,sms_delivery_failure_dto):
		frame_factory=gtkapplication.ui.dashboard.dashboard_sms_delivery_failure_frame.FrameFactory()
		frame=frame_factory.create_sms_delivery_failure_frame(gtk_builder,sms_delivery_failure_dto)
		self._notification_box.pack_end(frame,False,False,0)
	def enumerate_frames(self):
		children=self._notification_box.get_children()
		self._logger.debug("%d children",len(children))