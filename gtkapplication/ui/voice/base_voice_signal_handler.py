import logging
from timeit import default_timer
import pjsua2
import gtkapplication.api.sip.pjsip_container_accessor
import gtkapplication.api.sip.sip_call_state
import gtkapplication.api.sip.sip_call
import gtkapplication.api.contacts.contact_manager
import gtkapplication.api.sip.sipuri
import gtkapplication.ui.gtk.window_manager
import gtkapplication.ui.gtk.gtk_css
import gtkapplication.ui.gtk.gtk_builder
import gtkapplication.ui.gtk.window_state_accessor
import gtkapplication.ui.gtk.jump_to_window
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,GLib,Gio
class BaseVoiceSignalHandler:
	def __init__(self,gtk_builder,frame,parent_call_disconnected_handler):
		self._logger=logging.getLogger(__name__)
		self._gtk_builder=gtk_builder
		self._call_status_label=self._gtk_builder.get_object("call_status_label")
		self._call_duration_label=self._gtk_builder.get_object("call_duration_label")
		self._caller_id_label=self._gtk_builder.get_object("caller_id_label")
		self._update_count=0
		self._start_time=default_timer()
		self._source_tag=GLib.timeout_add(500,self._update_call_duration_label)
		self._sip_call=None
		self._frame=frame
		self._parent_call_disconnected_handler=parent_call_disconnected_handler
	def on_jump_menu_button_toggled(self,button):
		self._logger.debug("entered on_jump_menu_button_toggled, is_active = %s",button.get_active())
		if button.get_active():
			jump_to_window=gtkapplication.ui.gtk.jump_to_window.JumpToWindowHelper(self._gtk_builder)
			self._logger.debug("after jump_to_window()")
	def format_seconds(self,elaspsed_time_in_seconds):
		assert isinstance(elaspsed_time_in_seconds,float)
		hours,remainder=divmod(elaspsed_time_in_seconds,3600)
		minutes,seconds=divmod(remainder,60)
		formatted_seconds='{:02}:{:02}:{:02}'.format(int(hours),int(minutes),int(seconds))
		return formatted_seconds
	def on_call_state_change_handler(self,call_state,call_state_text,call_id):
		self._logger.debug("entered on_call_state_change_handler")
		self._logger.debug("call_state = %s, call_state_text = %s, call_id = %s",call_state,call_state_text,call_id)
		message="Call Status: {0} ({1})".format(call_state_text,call_state)
		self._call_status_label.set_text(message)
		if call_state==pjsua2.PJSIP_INV_STATE_DISCONNECTED:
			self._logger.debug("call_info.state == pj.PJSIP_INV_STATE_DISCONNECTED, firing handler")
			self.on_call_disconnected_handler()
		self._call_status_label.show_all()
	def on_keypad_button_clicked(self,button):
		self._logger.debug("entered on_keypad_button_clicked")
		keypad_grid=self._gtk_builder.get_object("keypad_grid")
		if keypad_grid.get_visible():
			keypad_grid.hide()
			self._logger.debug("keypad hidden")
		else:
			keypad_grid.show()
			self._logger.debug("keypad shown")
	def _update_call_duration_label(self):
		self._update_count+=1
		delta_in_seconds=default_timer()-self._start_time
		if self._update_count%10==0:
			self._logger.debug("in _update_call_duration_label, update_count = %d, delta_in_seconds = %d",self._update_count,delta_in_seconds)
		self._call_duration_label.set_text(self.format_seconds(delta_in_seconds))
		return True
	def on_call_disconnected_handler(self):
		self._logger.debug('entered on_call_disconnected')
		call_id=self._sip_call.getInfo().id
		self._logger.debug("disconnecting call_id = %d",call_id)
		self._sip_call=None
		gtkapplication.api.sip.sip_call_state.sip_calls[call_id]=None
		del gtkapplication.api.sip.sip_call_state.sip_calls[call_id]
		GLib.source_remove(self._source_tag)
		self._logger.debug('after GLib.source_remove, tag is %s',self._source_tag)
		active_call_grid=self._gtk_builder.get_object("active_call_grid")
		active_call_grid.remove(self._frame)
		self._logger.debug("after active_call_grid.remove(frame)")
		self._parent_call_disconnected_handler()
		self._logger.debug("after _parent_call_disconnected_handler")