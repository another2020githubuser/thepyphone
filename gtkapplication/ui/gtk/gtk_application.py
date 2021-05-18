import logging
import urllib
import time
import gtkapplication.ui.contacts.contacts_ui
import gtkapplication.api.sip.pjsip_lifecycle_manager
import gtkapplication.api.contacts.contact_manager
import gtkapplication.ui.gtk.gtk_dialog
import gtkapplication.data.config_data
import gtkapplication.api.profile.profile_manager
import gtkapplication.api.twilio.recording_command
from gtkapplication.ui.gtk.gtk_app_actions import GtkAppActions
import gtkapplication.ui.gtk.gtk_css
import gtkapplication.api.voicemail.controller
import gtkapplication.ui.global_.view
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gio
class GtkApplication(Gtk.Application):
	def __init__(self,application_id,flags):
		Gtk.Application.__init__(self,application_id=application_id,flags=flags)
		self._logger=logging.getLogger(__name__)
		self._logger.debug("Gtk Version Information: major:%s, minor:%s, micro: %s",Gtk.MAJOR_VERSION,Gtk.MINOR_VERSION,Gtk.MICRO_VERSION)
		self._profile_download_success=False
		self._contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		self.pjsip_manager=gtkapplication.api.sip.pjsip_lifecycle_manager.PjSipLifeCycleManager()
	def wait_for_internet_connection(self,timeout_in_seconds):
		self._logger.debug("entered wait_for_internet_connection")
		for i in range(timeout_in_seconds):
			try:
				response=urllib.request.urlopen('https://www.google.com',timeout=1)
				self._logger.debug("response.info() = %s",response.info())
				return True
			except urllib.request.URLError as error:
				self._logger.error(error)
				time.sleep(1)
		self._logger.warning("Network never came up, failing after %d seconds",timeout_in_seconds)
		return False
	def do_startup(self):
		self._logger.debug('entered GtkApplication::do_startup')
		Gtk.Application.do_startup(self)
		assert isinstance(self,Gtk.Application)
		timeout_in_seconds=90
		network_up=self.wait_for_internet_connection(timeout_in_seconds)
		self._logger.debug("network_up = %s",network_up)
		profile_manager=gtkapplication.api.profile.profile_manager.ProfileManager()
		user_profile=profile_manager.get_profile()
		self._logger.info("Profile loaded OK")
		if user_profile is None:
			self._profile_download_success=False
		else:
			self._profile_download_success=True
			gtkapplication.data.config_data.PROFILE_DATA=user_profile
			self._contact_manager.startup()
			self._logger.info("Contact Manager Started OK")
			self.pjsip_manager.startup()
			self._logger.info('Communication Layer Started OK')
			self._create_app_actions()
			self._logger.debug("after _create_app_actions")
			self._load_global_css()
	def _load_global_css(self):
		self._logger.debug("entered load_global_css")
		css_loader=gtkapplication.ui.gtk.gtk_css.GtkCss()
		css_loader.load_global_css()
		self._logger.debug("global css loaded")
	def do_activate(self,*args):
		self._logger.debug('entered do_activate')
		assert isinstance(self,Gtk.Application)
		if self._profile_download_success:
			window_state_accessor=gtkapplication.ui.gtk.window_state_accessor.WindowStateAccessor()
			window_state_accessor.set_gtk_application(self)
			self._logger.debug('after set_gtk_application')
			recording_command=gtkapplication.api.twilio.recording_command.RecordingCommand()
			twilio_recordings=recording_command.get_mapped_twilio_recordings()
			self._logger.debug("after recording_command.get_recordings_dto()")
			window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
			dashboard_ui=window_manager.get_dashboard_window()
			voicemail_count=0
			for twilio_recording in twilio_recordings:
				(contact,active_contact_point_index)=self._contact_manager.find_contact_by_phone_number(twilio_recording.from_phone_number,True)
				dashboard_ui.add_new_voicemail_notification(twilio_recording,contact,active_contact_point_index)
				self._logger.debug("added voicemail notification %s",twilio_recording.date_created)
				voicemail_count+=1
			dashboard_ui.showme()
			self._logger.debug("after dashboard_ui.showme()")
			self._logger.info("Retrieved %d voicemails OK",voicemail_count)
			voice_ui=window_manager.get_voice_window()
			vm_controller=gtkapplication.api.voicemail.controller.VoicemailController()
			recording_dtos=vm_controller.get_model_from_db()
			for recording_dto in recording_dtos:
				(contact,active_contact_point_index)=self._contact_manager.find_contact_by_phone_number(recording_dto.from_phone_number,True)
				voice_ui.add_voicemail(recording_dto,contact,active_contact_point_index)
			contacts_window=window_manager.get_contacts_window()
			contacts=self._contact_manager.get_contacts()
			for contact in contacts:
				contacts_window.add_new_contact(contact)
			contacts_window.showme()
			self._logger.debug("after contacts_window.showme()")
			self._logger.info("Showed contacts window with %d contacts OK",len(contacts))
		else:
			self._logger.info("profile download failed, skipping gui init")
	def _create_app_actions(self):
		assert isinstance(self,Gtk.Application)
		self._create_app_action("show_about_dialog",self._show_about_dialog)
		self._create_app_action("show_contacts_window",self._show_contacts_window)
		self._create_app_action("show_diagnostic_dialog",self._show_diagnostic_dialog)
		self._create_app_action("show_dashboard",self._show_dashboard)
		self._create_app_action("show_dialpad",self._show_dialpad)
	def _create_app_action(self,action_name,action_target_function):
		self._logger.debug("entered _create_app_action. action_name = %s",action_name)
		simple_action=Gio.SimpleAction.new(action_name)
		simple_action.connect("activate",action_target_function)
		self.add_action(simple_action)
	def _show_about_dialog(self,action,user_data):
		self._logger.debug("entered show_about. action = %s, user_data = %s",action,user_data)
		app_action=GtkAppActions()
		app_action.show_about_dialog()
	def _show_contacts_window(self,action,user_data):
		self._logger.debug("entered show_contacts. action = %s, user_data = %s",action,user_data)
		app_action=GtkAppActions()
		app_action.show_contacts_window()
	def _show_diagnostic_dialog(self,action,user_data):
		self._logger.debug("entered _show_diagnostic_dialog")
		app_action=GtkAppActions()
		app_action.show_diagnostic_dialog()
	def _show_dashboard(self,action,user_data):
		self._logger.debug("entered _show_dashboard")
		app_action=GtkAppActions()
		app_action.show_dashboard()
	def _show_dialpad(self,action,user_data):
		self._logger.debug("entered _show_dialpad")
		app_action=GtkAppActions()
		app_action.show_dialpad()
	def do_shutdown(self):
		self._logger.debug('entered GtkApplication::do_shutdown')
		assert isinstance(self,Gtk.Application)
		Gtk.Application.do_shutdown(self)
		if self._profile_download_success:
			self.pjsip_manager.shutdown()
			self._logger.debug('after pjsip_static.shutdown()')
			self._logger.info('Communication Layer Shutdown OK')
			self._contact_manager.shutDown()
			self._logger.debug("after _contact_manager.shutDown()")
			self._logger.info("Normal shutdown")