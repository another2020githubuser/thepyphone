import logging
import gtkapplication.ui.gtk.gtk_textbuffer
import gtkapplication.ui.gtk.jump_to_window
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gdk
class SmsUiSignalHandler:
	def __init__(self,on_sms_send_handler,on_keyboard_toggle_handler,on_insert_image_handler,gtk_builder):
		self._logger=logging.getLogger(__name__)
		self._gtk_builder=gtk_builder
		self._on_sms_send_handler=on_sms_send_handler
		self._on_keyboard_toggle_handler=on_keyboard_toggle_handler
		self._on_insert_image_handler=on_insert_image_handler
		self._textview_textbuffer=gtk_builder.get_object("textview_textbuffer")
		buffer_util=gtkapplication.ui.gtk.gtk_textbuffer.GtkTextBuffer()
		self._placeholder_text=buffer_util.get_text(self._textview_textbuffer)
		self._input_textview=gtk_builder.get_object("input_textview")
	def on_send_sms_button_clicked(self,widget):
		self._logger.debug("entered on_send_sms_button_clicked")
		self._on_sms_send_handler()
	def on_image_button_clicked(self,widget):
		self._logger.debug("entered on_image_button_clicked")
		self._on_insert_image_handler()
	def on_keyboard_toggle_button_clicked(self,button):
		self._logger.debug("entered on_keyboard_toggle_button_clicked")
		self._on_keyboard_toggle_handler()
	def on_input_textview_focus_in_event(self,textbuf,user_data):
		self._logger.debug("entered on_input_textview_focus_in_event")
		buffer_util=gtkapplication.ui.gtk.gtk_textbuffer.GtkTextBuffer()
		contents=buffer_util.get_text(textbuf)
		if contents==self._placeholder_text:
			textbuf.set_text("")
		return False
	def on_input_textview_focus_out_event(self,textbuf,user_data):
		self._logger.debug("entered on_input_textview_focus_out_event")
		buffer_util=gtkapplication.ui.gtk.gtk_textbuffer.GtkTextBuffer()
		contents=buffer_util.get_text(textbuf)
		if contents=="":
			textbuf.set_text(self._placeholder_text)
		return False
	def on_menu_button_clicked(self,button):
		self._logger.debug('entered on_menu_button_clicked')
	def on_main_window_set_focus(self,window,user_data):
		self._logger.debug("entered on_main_window_set_focus")
	def on_main_window_window_state_event(self,window,event):
		window_presented=int(event.changed_mask) and Gdk.WindowState.FOCUSED==Gdk.WindowState.FOCUSED
		if window_presented:
			self._logger.debug("window %s presented",window.get_title())
	def on_jump_menu_button_toggled(self,button):
		self._logger.debug("entered on_jump_menu_button_toggled, is_active = %s",button.get_active())
		if button.get_active():
			jump_to_window=gtkapplication.ui.gtk.jump_to_window.JumpToWindowHelper(self._gtk_builder)
			self._logger.debug("after jump_to_window()")