import logging
import os.path
import datetime
import requests
import pjsua2
import magic
import gtkapplication.ui.gtk.gtk_builder
import gtkapplication.api.twilio.sms_command
import gtkapplication.api.sip.instant_message
import gtkapplication.data.config_data
import gtkapplication.api.sip.pjsip_container_accessor
import gtkapplication.ui.gtk.window_state_accessor
import gtkapplication.api.signal.signal_command
from gtkapplication.ui.sms import SmsDirection
from gtkapplication.ui.sms.sms_onscreen_keyboard_signal_handler import OnScreenKeyboardSignalHandler
from gtkapplication.ui.sms.sms_ui_signal_handler import SmsUiSignalHandler
from gtkapplication.ui.sms.mms_frame_signal_handler import MmsSignalHandler
import gtkapplication.ui.gtk.gtk_image_resize
import gtkapplication.ui.gtk.gtk_dialog
import gtkapplication.ui.gtk.jump_to_window
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gio
class SmsUi():
	def __init__(self,window_unique_key):
		self._logger=logging.getLogger(__name__)
		self._window_unique_key=window_unique_key
		self._logger.debug('window_unique_key = %s',window_unique_key)
		self.gtk_application_window=None
		self._shift_button_clicked=True
		glade_file_name="sms_ui.glade"
		self._gtk_builder=gtkapplication.ui.gtk.gtk_builder.GtkBuilder(__file__,glade_file_name)
		self.gtk_application_window=self._gtk_builder.get_object('main_window')
		self._logger.debug('got window')
		self._textview_textbuffer=self._gtk_builder.get_object("textview_textbuffer")
		buffer_util=gtkapplication.ui.gtk.gtk_textbuffer.GtkTextBuffer()
		self._placeholder_text=buffer_util.get_text(self._textview_textbuffer)
		self._logger.debug("placeholder_text = %s",self._placeholder_text)
		sms_ui_signal_handler=SmsUiSignalHandler(self._on_sms_send_handler,self._on_toggle_onscreen_keyboard_handler,self._on_insert_image_handler,self._gtk_builder)
		self._gtk_builder.connect_signals(sms_ui_signal_handler)
		self._logger.debug("sms_ui_signal_handler set")
		self._content_box=self._gtk_builder.get_object("content_box")
		self._load_keyboard()
		jump_to_window=gtkapplication.ui.gtk.jump_to_window.JumpToWindowHelper(self._gtk_builder)
	def showme(self,contact,active_contact_point_index):
		self._logger.debug('enter showme')
		self._contact=contact
		self._active_contact_point_index=active_contact_point_index
		css_file="sms_ui.css"
		css_parser=gtkapplication.ui.gtk.gtk_css.GtkCss()
		css_parser.load_and_apply_css(__file__,css_file)
		contact_point=contact.contact_points[active_contact_point_index]
		headerbar=self._gtk_builder.get_object("headerbar")
		title_text=self._window_unique_key
		self._logger.debug("title_text = %s",title_text)
		headerbar.set_title(title_text)
		self._logger.debug('got window')
		self.gtk_application_window.connect("delete-event",self._onclose)
		send_mms_action=Gio.SimpleAction.new("send_mms_action",None)
		send_mms_action.connect("activate",self._on_send_mms_action)
		self.gtk_application_window.add_action(send_mms_action)
		toggle_onscreen_keyboard_action=Gio.SimpleAction.new("toggle_onscreen_keyboard",None)
		toggle_onscreen_keyboard_action.connect("activate",self._on_toggle_onscreen_keyboard_action)
		self.gtk_application_window.add_action(toggle_onscreen_keyboard_action)
		self.gtk_application_window.show_all()
		if self.gtk_application_window.get_size()!=(800,480):
			self._logger.info("Unexpected Window Size: %s",self.gtk_application_window.get_size())
		self._logger.debug('window shown, size is %s',self.gtk_application_window.get_size())
	def on_menu_item_activate(self,menu_item):
		self._logger.debug("entered on_menu_item_activate")
	def display_sms(self,message_body,message_direction,timestamp):
		self._logger.debug('entered display_sms')
		frame=self._create_sms_frame(message_body,message_direction,timestamp)
		self._content_box.pack_start(frame,False,False,0)
	def display_mms(self,image_url,message_direction,timestamp,content_type,file_extension):
		self._logger.debug('entered display_mms')
		self._logger.debug("image_url = %s",image_url)
		response=requests.get(image_url)
		assert response.status_code==200
		image_bytes=response.content
		gtk_image_resizer=gtkapplication.ui.gtk.gtk_image_resize.GtkImageResize()
		target_resolution=os.environ["TARGET_MONITOR_RESOLUTION"]
		if target_resolution=="800x480":
			pixbuf=gtk_image_resizer.scale_to_width(image_bytes,700)
		elif target_resolution=="1366x768":
			pixbuf=gtk_image_resizer.scale_to_width(image_bytes,1200)
		else:
			raise ValueError("{0} is an unsupported screen resoultion".format(target_resolution))
		frame=self._create_mms_frame(message_direction,timestamp)
		mms_image=self._gtk_builder.get_object('mms_image')
		mms_image.set_from_pixbuf(pixbuf)
		frame.connect("size-allocate",self._frame_size_allocate)
		self._content_box.pack_start(frame,False,False,0)
		signal_handler=MmsSignalHandler(image_bytes,content_type,file_extension)
		self._gtk_builder.connect_signals(signal_handler)
		frame.show_all()
	def _frame_size_allocate(self,frame,gdk_rectangle):
		self._logger.debug("entered _frame_size_allocate")
		self._logger.debug("width = %s, height = %s",gdk_rectangle.width,gdk_rectangle.height)
	def _on_insert_image_handler(self):
		self._logger.debug("entered _on_insert_image_handler")
		self._send_mms()
	def _on_send_mms_action(self,action,user_data):
		self._logger.debug("entered _on_send_mms_action")
		self._send_mms()
	def _on_toggle_onscreen_keyboard_action(self,action,user_data):
		self._logger.debug("entered _on_toggle_onscreen_keyboard_action")
		self._toggle_onscreen_keyboard_visiblity()
	def _on_toggle_onscreen_keyboard_handler(self):
		self._logger.debug("entered _on_toggle_onscreen_keyboard_action")
		self._toggle_onscreen_keyboard_visiblity()
	def send_sms(self,contact,active_contact_point_index,text_message_content):
		self._logger.debug("entered send_sms")
		self._logger.debug("point_type = %s",contact.contact_points[active_contact_point_index].point_type)
		self._logger.debug("text_message_content = '%s'",text_message_content)
		if len(text_message_content)==0:
			common_dialogs=gtkapplication.ui.gtk.gtk_dialog.CommonDialogs()
			main_text="Empty SMS"
			secondary_text="Cannot send empty SMS.  Please input some text and try again."
			common_dialogs.show_info_dialog(main_text,secondary_text,self.gtk_application_window)
		else:
			if self._contact.contact_points[self._active_contact_point_index].point_type=='x-sip':
				buddy=contact.buddy
				self._logger.debug("buddy uri = %s",buddy.uri)
				if buddy.latest_buddy_get_info.subState==pjsua2.PJSIP_EVSUB_STATE_ACTIVE:
					self._logger.debug('sending message via SIP to buddy %r',buddy)
					instant_message_command=gtkapplication.api.sip.instant_message.InstantMessageHandler()
					instant_message_command.send_text(buddy,text_message_content)
				else:
					common_dialog=gtkapplication.ui.gtk.gtk_dialog.CommonDialogs()
					main_text="Free Buddy Temporarily Off Line, Try Again Later"
					secondary_text="Status: {0}".format(buddy.latest_buddy_get_info.subStateName)
					common_dialog.show_info_dialog(main_text,secondary_text,self.gtk_application_window,"Buddy Off Line")
					return
			elif contact.contact_points[active_contact_point_index].point_type=='tel':
				self._logger.debug('sending message via Twilio')
				sms_command=gtkapplication.api.twilio.sms_command.SmsCommand()
				phone_number_from=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
				phone_number_to=contact.contact_points[active_contact_point_index].uri_string
				self._logger.debug('sending sms from %s to %s',phone_number_from,phone_number_to)
				assert phone_number_to is not None
				assert phone_number_from!=phone_number_to
				message_sid=sms_command.send(phone_number_from,phone_number_to,text_message_content)
				self._logger.debug('sms sent, message_sid = %s',message_sid)
			elif contact.contact_points[active_contact_point_index].point_type=='x-signal':
				phone_number_to=contact.contact_points[active_contact_point_index].uri_string
				gtkapplication.api.signal.signal_command.sendSignalTextMessage(text_message_content,phone_number_to)
			else:
				raise ValueError('Unknown point_type = {0}'.format(self._contact.contact_points[self._active_contact_point_index].point_type))
			self.display_sms(text_message_content,SmsDirection.SENT,datetime.datetime.now())
			self._textview_textbuffer.set_text("")
	def _send_sms(self):
		self._logger.debug("entered _send_sms")
		self._logger.debug("point_type = %s",self._contact.contact_points[self._active_contact_point_index].point_type)
		textbuffer_util=gtkapplication.ui.gtk.gtk_textbuffer.GtkTextBuffer()
		assert isinstance(self._textview_textbuffer,Gtk.TextBuffer)
		text_message_content=textbuffer_util.get_text(self._textview_textbuffer)
		self._logger.debug("text_message_content = '%s'",text_message_content)
		if len(text_message_content)==0 or text_message_content==self._placeholder_text:
			common_dialogs=gtkapplication.ui.gtk.gtk_dialog.CommonDialogs()
			main_text="Empty SMS"
			secondary_text="Cannot send empty SMS.  Please input some text and try again."
			common_dialogs.show_info_dialog(main_text,secondary_text,self.gtk_application_window)
		else:
			self.send_sms(self._contact,self._active_contact_point_index,text_message_content)
	def _on_sms_send_handler(self):
		self._logger.debug("entered _on_sms_send_handler")
		self._send_sms()
	def _load_keyboard(self):
		self._logger.debug("entered load_keyboard")
		glade_file_name="sms_onscreen_keyboard.glade"
		self._gtk_builder.add_from_file(__file__,glade_file_name)
		self._keyboard=self._gtk_builder.get_object("keyboard_box")
		keyboard_signal_handler=OnScreenKeyboardSignalHandler(self._textview_textbuffer,self._shift_button_clicked,self._on_sms_send_handler,self.on_keyboard_toggle_button_clicked)
		self._gtk_builder.connect_signals(keyboard_signal_handler)
		self._logger.debug("keyboard_signal_handler set")
		keyboard_container=self._gtk_builder.get_object("keyboard_container")
		keyboard_container.pack_start(self._keyboard,False,False,0)
		self._keyboard_visible=True
		self._logger.debug("keyboard loaded and visible")
	def _toggle_onscreen_keyboard_visiblity(self):
		self._logger.debug("entered _toggle_onscreen_keyboard_visiblity")
		if self._keyboard is None:
			self._load_keyboard()
		else:
			if self._keyboard_visible:
				self._logger.debug("keyboard visible, hiding")
				self._keyboard.hide()
			else:
				self._logger.debug("keyboard hidden, making visible")
				self._keyboard.hide()
				self._keyboard.show_all()
			self._keyboard_visible= not self._keyboard_visible
			self._logger.debug("toggled self._keyboard_visible to %s",self._keyboard_visible)
	def on_keyboard_toggle_button_clicked(self):
		self._logger.debug("entered on_keyboard_toggle_button_clicked")
		self._toggle_onscreen_keyboard_visiblity()
	def _onclose(self,*args):
		self._logger.debug('entered onclose, args count = %d',len(args))
		if self._window_unique_key is None:
			self._logger.debug('self._window_unique_key is None, skipping remove_window_from_cache and quitting gtk')
			Gtk.main_quit()
		else:
			stateful_object_accessor=gtkapplication.ui.gtk.window_state_accessor.WindowStateAccessor()
			stateful_object_accessor.remove_window_from_cache(self._window_unique_key)
			self._logger.debug('after remove_window_from_cache')
			self.gtk_application_window.destroy()
			self._logger.debug('window.destroy() called')
	def _create_sms_frame(self,message_body,message_direction,timestamp):
		self._logger.debug('entered display_sms')
		glade_file_name="sms_frame.glade"
		self._gtk_builder.add_from_file(__file__,glade_file_name)
		frame=self._gtk_builder.get_object('sms_frame')
		timestamp_label=self._gtk_builder.get_object('timestamp_label')
		assert isinstance(timestamp,datetime.datetime)
		current_time=timestamp.strftime('%a %b %d, %H:%M %p')
		if message_direction==SmsDirection.SENT:
			frame.set_label_align(0.99,0.02)
			label_text="Sent on {0}".format(current_time)
			timestamp_label.set_text(label_text)
			ctx=frame.get_style_context()
			ctx.add_class("sms_sent_style_class")
		elif message_direction==SmsDirection.RECEIVED:
			frame.set_label_align(0.02,0.99)
			label_text="Received on {0}".format(current_time)
			timestamp_label.set_text(label_text)
			ctx=frame.get_style_context()
			ctx.add_class("sms_received_style_class")
		else:
			raise ValueError("Bad value for message_direction: {0}".format(message_direction))
		inner_label=self._gtk_builder.get_object('sms_contents_label')
		inner_label.set_text(message_body)
		return frame
	def _create_mms_frame(self,message_direction,timestamp):
		self._logger.debug('entered _create_mms_frame')
		glade_file_name="mms_frame.glade"
		self._gtk_builder.add_from_file(__file__,glade_file_name)
		frame=self._gtk_builder.get_object('mms_frame')
		timestamp_label=self._gtk_builder.get_object('timestamp_label')
		assert isinstance(timestamp,datetime.datetime)
		current_time=timestamp.strftime('%a %b %d, %H:%M %p')
		if message_direction==SmsDirection.SENT:
			frame.set_label_align(0.99,0.02)
			label_text="Sent on {0}".format(current_time)
			timestamp_label.set_text(label_text)
			ctx=frame.get_style_context()
			ctx.add_class("sms_sent_style_class")
		elif message_direction==SmsDirection.RECEIVED:
			frame.set_label_align(0.02,0.99)
			label_text="Received on {0}".format(current_time)
			timestamp_label.set_text(label_text)
			ctx=frame.get_style_context()
			ctx.add_class("sms_received_style_class")
		else:
			raise ValueError("Bad value for message_direction: {0}".format(message_direction))
		return frame
	def _send_mms(self):
		self._logger.debug('entered _send_mms')
		common_dialogs=gtkapplication.ui.gtk.gtk_dialog.CommonDialogs()
		(dialog_response,local_file)=common_dialogs.show_file_open_dialog(self.gtk_application_window)
		file_extension=os.path.splitext(local_file)[1]
		content_type=magic.from_file(local_file,mime=True)
		self._logger.debug("link has content_type %s",content_type)
		self._logger.debug("link has extension %s",file_extension)
		if dialog_response==Gtk.ResponseType.OK:
			if self._contact.contact_points[self._active_contact_point_index].point_type=='x-sip':
				raise NotImplementedError("Sending files by SIP not implemented")
			elif self._contact.contact_points[self._active_contact_point_index].point_type=='tel':
				sms_command=gtkapplication.api.twilio.sms_command.SmsCommand()
				phone_number_from=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
				phone_number_to=self._contact.contact_points[self._active_contact_point_index].uri_string
				assert phone_number_from!=phone_number_to
				self._logger.debug('sending sms to %s',phone_number_to)
				msg=""
				(message_sid,vps_url)=sms_command.send(phone_number_from,phone_number_to,msg,local_file)
				self._logger.debug('message_sid = %s',message_sid)
				self.display_mms(vps_url,SmsDirection.SENT,datetime.datetime.now(),content_type,file_extension)
			elif self._contact.contact_points[self._active_contact_point_index].point_type=='x-signal':
				self._logger.debug("signal sending file %s",local_file)
				phone_number_to=self._contact.contact_points[self._active_contact_point_index].uri_string
				gtkapplication.api.signal.signal_command.sendSignalTextMessage("",phone_number_to,[local_file])
			else:
				raise ValueError('unknown protocol: {0}'.format(self._contact.contact_points[self._active_contact_point_index].point_type))
		else:
			self._logger.debug('user cancelled')