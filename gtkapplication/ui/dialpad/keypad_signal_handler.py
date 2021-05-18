import logging
import gtkapplication.api.sip.dtmf_tone
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gio
class KeypadSignalHandler:
	def __init__(self,gtk_builder,parent_close_window_handler):
		self._logger=logging.getLogger(__name__)
		self._gtk_builder=gtk_builder
		self._phone_number_entry=self._gtk_builder.get_object("phone_number_entry")
		self._parent_close_window_handler=parent_close_window_handler
	def on_dialpad_button_clicked(self,button):
		self._logger.debug("enter on_dialpad_button_clicked")
		assert isinstance(self._phone_number_entry,Gtk.Entry)
		self._logger.debug("entry.get_position() = %s",self._phone_number_entry.get_position())
		phone_number=self._phone_number_entry.get_text()
		self._logger.debug('phone_number = %s',phone_number)
		label=button.get_child()
		digit=label.get_text()
		self._logger.debug('digit = %s',digit)
		dtmf_player=gtkapplication.api.sip.dtmf_tone.DtmfTone()
		dtmf_player.play_dtmf_tone(digit,self._get_active_radio_button_label())
		self._phone_number_entry.set_text(self._phone_number_entry.get_text()+digit)
	def on_dtmf_radio_button_toggled(self,radio_button):
		if radio_button.get_active():
			self._logger.debug("active radio button label = %s",self._get_active_radio_button_label())
	def _get_active_radio_button_label(self):
		radio_button_group=self._gtk_builder.get_object("dtmf_off_radio_button").get_group()
		active_buttons=[button for button in radio_button_group if button.get_active()]
		assert len(active_buttons)==1
		active_radio_button_label=active_buttons[0].get_label()
		self._logger.debug('active_radio_button_label = %s',active_radio_button_label)
		return active_radio_button_label
	def on_phone_number_entry_icon_release(self,icon_position,event,entry):
		self._logger.debug("entered on_phone_number_entry_icon_release, icon_position is %s",icon_position)
		self.on_backspace_button_clicked(Gtk.Button())
	def on_dialpad_button_released(self,button,ev,data=None):
		self._logger.debug("entered on_dialpad_button_released, string = %s, keyval=%s",ev.string,ev.keyval)
		KEY_BACKSPACE=65288
		if ev.keyval==KEY_BACKSPACE:
			self.on_backspace_button_clicked(button)
		elif ev.string in ['0','1','2','3','4','5','6','7','8','9','*','#','a','b','c','d']:
			keypad_grid=self._gtk_builder.get_object("keypad_grid")
			if keypad_grid.get_visible():
				digit=ev.string
				current_text=self._phone_number_entry.get_text()
				self._logger.debug("digit = '%s', current_text = %s",digit,current_text)
				num_characters=len(current_text)
				self._phone_number_entry.set_text(current_text+digit)
				self._phone_number_entry.set_position(num_characters+1)
				dtmf_player=gtkapplication.api.sip.dtmf_tone.DtmfTone()
				dtmf_player.play_dtmf_tone(digit,self._get_active_radio_button_label())
			else:
				self._logger.debug("keypad not visible, ignoring keypress %s",ev.string)
		else:
			self._logger.debug("ignoring non-numeric key string = %s, keyval=%s",ev.string,ev.keyval)
		return True
	def on_backspace_button_clicked(self,button):
		self._logger.debug('entered on_backspace_button_clicked')
		phone_number=self._phone_number_entry.get_text()
		self._logger.debug('phone_number = %s',phone_number)
		if phone_number:
			if len(phone_number)==1:
				self._logger.debug("disallowing deleting + sign")
			else:
				phone_number=phone_number[:-1]
				self._phone_number_entry.set_text(phone_number)
		else:
			self._logger.debug('ignoring attempt to delete from empty phone number')
	def on_jump_menu_button_toggled(self,button):
		self._logger.debug("entered on_jump_menu_button_toggled, is_active = %s",button.get_active())
		if button.get_active():
			jump_to_window=gtkapplication.ui.gtk.jump_to_window.JumpToWindowHelper(self._gtk_builder)
			self._logger.debug("after jump_to_window()")
			button.show_all()
	def on_voice_button_clicked(self,button):
		phone_number=self._phone_number_entry.get_text()
		self._logger.debug('phone_number = %s',phone_number)
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		(contact,active_contact_point_index)=contact_manager.find_contact_by_phone_number(phone_number,True)
		self._logger.debug("contact is %s, contact_point is %s",contact,contact.contact_points[active_contact_point_index])
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		voice_window=window_manager.get_voice_window()
		voice_window.add_outgoing_call(contact,active_contact_point_index)
		self._parent_close_window_handler()
	def on_sms_button_clicked(self,button):
		self._logger.debug("entered on_sms_button_clicked")
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		phone_number=self._phone_number_entry.get_text()
		self._logger.debug('phone_number = %s',phone_number)
		(contact,active_contact_point_index)=contact_manager.find_contact_by_phone_number(phone_number,True)
		self._logger.debug("contact is %s, contact_point is %s",contact,contact.contact_points[active_contact_point_index])
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		window_manager.get_sms_window(contact,active_contact_point_index,True)
		self._parent_close_window_handler()