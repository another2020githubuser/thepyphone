import logging
import gtkapplication.ui.gtk.window_state
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class WindowStateAccessor:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self.main_window_lookup_unique_key="Contacts"
		self.voicemail_window_lookup_unique_key="Voice Mail"
		self.keypad_lookup_unique_key="KeyPad"
	def get_gtk_application(self):
		self._logger.debug('entered get_gtk_application')
		assert isinstance(gtkapplication.ui.gtk.window_state.g_gtk_application,Gtk.Application)
		return gtkapplication.ui.gtk.window_state.g_gtk_application
	def set_gtk_application(self,gtk_application):
		self._logger.debug('entered set_gtk_application')
		assert gtk_application is not None
		assert isinstance(gtk_application,Gtk.Application)
		gtkapplication.ui.gtk.window_state.g_gtk_application=gtk_application
	def search_cache_for_window_key(self,window_lookup_unique_key):
		return window_lookup_unique_key in gtkapplication.ui.gtk.window_state.g_window_dict
	def get_all_window_unique_keys(self):
		self._logger.debug("entered get_all_window_unique_keys")
		window_lookup_keys=gtkapplication.ui.gtk.window_state.g_window_dict.keys()
		self._logger.debug("got %d keys",len(window_lookup_keys))
		return list(window_lookup_keys)
	def add_ui_instance_to_cache(self,window_lookup_unique_key,user_interface_instance):
		self._logger.debug("entered add_ui_instance_to_cache, key is '%s'",window_lookup_unique_key)
		gtk_window=user_interface_instance.gtk_application_window
		assert isinstance(gtk_window,(Gtk.ApplicationWindow,Gtk.Dialog))
		gtk_application=self.get_gtk_application()
		gtk_application.add_window(gtk_window)
		gtk_window_id=gtk_window.get_id()
		assert gtk_window_id!=0
		windows=gtk_application.get_windows()
		gtkapplication.ui.gtk.window_state.g_window_dict[window_lookup_unique_key]=(gtk_window_id,user_interface_instance)
		self._logger.debug('created window with id = %d, dict window count = %d, get_windows() count = %d',gtk_window_id,len(gtkapplication.ui.gtk.window_state.g_window_dict),len(windows))
		self._logger.debug('associated window id %d with unique_key = %s',gtk_window_id,window_lookup_unique_key)
		self._logger.debug('get_windows() count = %d, window_id = %d',len(windows),gtk_window.get_id())
	def get_ui_instance_from_cache(self,window_unique_key):
		self._logger.debug("entered get_ui_instance_from_cache, key is '%s",window_unique_key)
		gtk_application=self.get_gtk_application()
		(gtk_window_id,ui_instance)=gtkapplication.ui.gtk.window_state.g_window_dict[window_unique_key]
		self._logger.debug('window_id = %s',gtk_window_id)
		assert ui_instance is not None
		windows=gtk_application.get_windows()
		self._logger.debug('found window with id = %d, dict window count = %d, get_windows() count = %d',gtk_window_id,len(gtkapplication.ui.gtk.window_state.g_window_dict),len(windows))
		return ui_instance
	def remove_window_from_cache(self,window_lookup_unique_key):
		self._logger.debug("entered remove_window_from_cache, key is '%s'",window_lookup_unique_key)
		(gtk_window_id,ui_window)=gtkapplication.ui.gtk.window_state.g_window_dict[window_lookup_unique_key]
		gtk_application=self.get_gtk_application()
		gtk_window=gtk_application.get_window_by_id(gtk_window_id)
		self._logger.debug("removing unique_key '%s' from g_window_dict",window_lookup_unique_key)
		del gtkapplication.ui.gtk.window_state.g_window_dict[window_lookup_unique_key]
		gtk_application.remove_window(gtk_window)
		windows=gtk_application.get_windows()
		ui_window=None
		self._logger.debug('removed window id = %d, dict window count = %d, get_windows() count = %d',gtk_window_id,len(gtkapplication.ui.gtk.window_state.g_window_dict),len(windows))