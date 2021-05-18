import logging
import datetime
from datetime import timezone
import pjsua2
import gtkapplication.ui.gtk.window_state_accessor
import gtkapplication.ui.contacts.contacts_ui
import gtkapplication.ui.sms.sms_ui
import gtkapplication.ui.dialpad.keypad
import gtkapplication.ui.dashboard.dashboard_ui
import gtkapplication.ui.voice.voice_call_ui
class WindowManager:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def utc_timestamp(self):
		dt=datetime.datetime.now()
		timestamp=dt.replace(tzinfo=timezone.utc).timestamp()
		return timestamp
	def _get_or_create_instance(self,window_unique_key,ui_class):
		self._logger.debug('entered _get_or_create_instance')
		self._logger.debug('unique_key = %s',window_unique_key)
		window_state_accessor=gtkapplication.ui.gtk.window_state_accessor.WindowStateAccessor()
		window_state_accessor.get_gtk_application()
		if window_state_accessor.search_cache_for_window_key(window_unique_key):
			self._logger.debug('found unique key %s in dictionary',window_unique_key)
			ui_instance=window_state_accessor.get_ui_instance_from_cache(window_unique_key)
			assert isinstance(ui_instance,ui_class)
		else:
			self._logger.debug("unique key '%s' NOT found, creating instance",window_unique_key)
			ui_instance=ui_class(window_unique_key)
			window_state_accessor.add_ui_instance_to_cache(window_unique_key,ui_instance)
		assert isinstance(ui_instance,ui_class)
		return ui_instance
	def get_contacts_window(self):
		self._logger.debug('entered get_contacts_window')
		window_unique_key="Contacts Window Unique Key"
		ui_class=gtkapplication.ui.contacts.contacts_ui.ContactsUi
		ui_instance=self._get_or_create_instance(window_unique_key,ui_class)
		ui_instance.gtk_application_window.present_with_time(self.utc_timestamp())
		return ui_instance
	def get_dashboard_window(self,make_window_present=True):
		self._logger.debug('entered get_dashboard_window')
		window_unique_key="Dashboard Window Unique Key"
		self._logger.debug('window_unique_key = %s',window_unique_key)
		ui_class=gtkapplication.ui.dashboard.dashboard_ui.DashboardUI
		ui_instance=self._get_or_create_instance(window_unique_key,ui_class)
		if make_window_present:
			self._logger.debug("making dashboard window present")
			ui_instance.gtk_application_window.present()
		else:
			self._logger.debug("NOT making dashboard window present")
		return ui_instance
	def get_keypad_window(self):
		self._logger.debug("entered get_keypad_window")
		window_unique_key="KeyPad Window Unique Key"
		self._logger.debug('window_unique_key = %s',window_unique_key)
		ui_class=gtkapplication.ui.dialpad.keypad.KeypadUi
		ui_instance=self._get_or_create_instance(window_unique_key,ui_class)
		ui_instance.showme()
		ui_instance.gtk_application_window.present_with_time(self.utc_timestamp())
		return ui_instance
	def get_sms_window(self,contact,active_contact_point_index,make_window_present):
		self._logger.debug('entered get_sms_window')
		contact_point=contact.contact_points[active_contact_point_index]
		window_unique_key=""
		if contact_point.point_type=="tel":
			window_unique_key="SMS - {0} - {1} - {2}".format(contact.name,contact.contact_points[active_contact_point_index].description,contact.contact_points[active_contact_point_index].uri_string_national)
		elif contact_point.point_type=="x-sip":
			window_unique_key="Free Buddy Text - {0}".format(contact.name)
		else:
			assert contact_point.point_type in ["tel","x-sip"]
		self._logger.debug("window_unique_key = '%s'",window_unique_key)
		ui_class=gtkapplication.ui.sms.sms_ui.SmsUi
		ui_instance=self._get_or_create_instance(window_unique_key,ui_class)
		ui_instance.showme(contact,active_contact_point_index)
		if make_window_present:
			self._logger.debug("making sms window present")
			ui_instance.gtk_application_window.present_with_time(self.utc_timestamp())
		else:
			self._logger.debug("NOT making window present")
		return ui_instance
	def get_voice_window(self):
		self._logger.debug("entered get_voice_window")
		window_unique_key="Voice Window Unique Key"
		self._logger.debug('window_unique_key = %s',window_unique_key)
		ui_class=gtkapplication.ui.voice.voice_call_ui.VoiceCallUI
		ui_instance=self._get_or_create_instance(window_unique_key,ui_class)
		ui_instance.showme()
		ui_instance.gtk_application_window.present()
		self._logger.debug("made voice window present()")
		return ui_instance
	def get_window_by_key(self,window_unique_key,make_window_present):
		self._logger.debug('entered get_window_by_key()')
		window_state_accessor=gtkapplication.ui.gtk.window_state_accessor.WindowStateAccessor()
		ui_instance=window_state_accessor.get_ui_instance_from_cache(window_unique_key)
		if make_window_present:
			ui_instance.gtk_application_window.present()
	def _get_all_window_unique_keys(self):
		self._logger.debug('entered _get_all_window_unique_keys')
		window_state_accessor=gtkapplication.ui.gtk.window_state_accessor.WindowStateAccessor()
		return window_state_accessor.get_all_window_unique_keys()
	def get_sms_window_keys(self):
		self._logger.debug('entered get_sms_window_keys')
		all_window_keys=self._get_all_window_unique_keys()
		sms_window_list=[i for i in all_window_keys if i.startswith("SMS")]
		return sms_window_list
	def get_free_buddy_text_window_keys(self):
		self._logger.debug('entered get_free_buddy_text_window_keys')
		all_window_keys=self._get_all_window_unique_keys()
		free_buddy_text_window_list=[i for i in all_window_keys if i.startswith("Free Buddy Text")]
		return free_buddy_text_window_list
	def get_voice_window_keys(self):
		self._logger.debug('entered get_voice_window_keys')
		all_window_keys=self._get_all_window_unique_keys()
		voice_window_list=[i for i in all_window_keys if i.startswith("Voice")]
		return voice_window_list
	def get_free_buddy_voice_window_keys(self):
		self._logger.debug('entered get_free_buddy_voice_window_keys')
		all_window_keys=self._get_all_window_unique_keys()
		voice_window_list=[i for i in all_window_keys if i.startswith("Free Buddy Voice")]
		return voice_window_list
	def present_sms_window_by_key(self,sms_window_key):
		self._logger.debug('entered present_sms_window_by_key, key is %s',sms_window_key)
		window_state_accessor=gtkapplication.ui.gtk.window_state_accessor.WindowStateAccessor()
		window_state_accessor.get_gtk_application()
		assert window_state_accessor.search_cache_for_window_key(sms_window_key)
		self._logger.debug('found unique key %s in dictionary',sms_window_key)
		sms_ui_instance=window_state_accessor.get_ui_instance_from_cache(sms_window_key)
		sms_ui_instance.gtk_application_window.present()