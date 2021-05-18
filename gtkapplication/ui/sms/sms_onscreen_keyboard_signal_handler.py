import logging
import gtkapplication.ui.gtk.gtk_textbuffer
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class OnScreenKeyboardSignalHandler:
	def __init__(self,buffer,shift_button_clicked,send_sms_handler,toggle_keyboard_handler):
		self._logger=logging.getLogger(__name__)
		assert isinstance(buffer,Gtk.TextBuffer)
		self._buffer=buffer
		self.shift_button_clicked=shift_button_clicked
		self._send_sms_handler=send_sms_handler
		self._toggle_keyboard_handler=toggle_keyboard_handler
	def on_keyboard_toggle_button_clicked(self,button):
		self._logger.debug("entered on_keyboard_toggle_button_clicked")
		self._toggle_keyboard_handler()
		self._logger.debug("keyboard visibility toggled")
	def on_keybooard_button_space_clicked(self,widget):
		self._logger.debug("entered on_button_space_clicked")
		buffer_util=gtkapplication.ui.gtk.gtk_textbuffer.GtkTextBuffer()
		current_text=buffer_util.get_text(self._buffer)
		current_text+=" "
		self._buffer.set_text(current_text)
	def on_keyboard_shift_button_clicked(self,button):
		self._logger.debug("entered on_shift_button_clicked")
		self._logger.debug("shift_button_clicked = %s",self.shift_button_clicked)
		if self.shift_button_clicked:
			self._logger.debug("shift button clicked twice")
			self.shift_button_clicked=False
		else:
			self.shift_button_clicked=True
	def on_keyboard_button_backspace_clicked(self,widget):
		self._logger.debug("entered button_backspace_clicked")
		buffer_util=gtkapplication.ui.gtk.gtk_textbuffer.GtkTextBuffer()
		current_text=buffer_util.get_text(self._buffer)
		self._buffer.set_text(current_text[:-1])
	def on_keyboard_button_clicked(self,button):
		self._logger.debug("entered on_keyboard_button_clicked")
		new_character=button.get_child().get_text()
		self._logger.debug("new_character is %s",new_character)
		if self.shift_button_clicked:
			new_character=new_character.upper()
			self._logger.debug("shift_button_clicked, upper cased is %s",new_character)
			self.shift_button_clicked=False
		buffer_util=gtkapplication.ui.gtk.gtk_textbuffer.GtkTextBuffer()
		current_text=buffer_util.get_text(self._buffer)
		if current_text=="Type Message Here":
			self._buffer.set_text("")
			current_text=""
		current_text+=new_character
		self._buffer.set_text(current_text)
	def on_keyboard_button_return_clicked(self,widget):
		self._logger.debug("entered on_keyboard_button_clicked")
		self._send_sms_handler()