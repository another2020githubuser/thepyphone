import logging
import gtkapplication.ui.gtk.jump_to_window
import gtkapplication.ui.voice.voice_call_inbound_signal_handler
import gtkapplication.ui.voice.voice_call_outgoing_signal_handler
import gtkapplication.ui.voicemail.dashboard_voicemail_frame
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gio
class VoiceCallUI:
	def __init__(self,window_unique_key):
		self._logger=logging.getLogger(__name__)
		self._window_unique_key=window_unique_key
		glade_file_name="voice_call_ui.glade"
		self._gtk_builder=gtkapplication.ui.gtk.gtk_builder.GtkBuilder(__file__,glade_file_name)
		self.gtk_application_window=self._gtk_builder.get_object("voice_window")
		jump_to_window=gtkapplication.ui.gtk.jump_to_window.JumpToWindowHelper(self._gtk_builder)
		css_file="voice_call.css"
		css_parser=gtkapplication.ui.gtk.gtk_css.GtkCss()
		css_parser.load_and_apply_css(__file__,css_file)
		self._logger.debug("before connecting signals in voice_call_ui")
		self._gtk_builder.connect_signals(self)
		self._logger.debug("after connecting signals in voice_call_ui")
		self.gtk_application_window.connect("delete-event",self._on_close)
		window_size=self.gtk_application_window.get_size()
		self._logger.debug('window_size = %s',window_size)
		self._number_of_calls=0
		self._number_of_voicemails=0
		conference_call_action=Gio.SimpleAction.new("conference_call_action",None)
		conference_call_action.connect("activate",self._on_conference_call_action)
		self.gtk_application_window.add_action(conference_call_action)
	def on_jump_menu_button_toggled(self,button):
		self._logger.debug("entered on_jump_menu_button_toggled, is_active = %s",button.get_active())
		if button.get_active():
			jump_to_window=gtkapplication.ui.gtk.jump_to_window.JumpToWindowHelper(self._gtk_builder)
			self._logger.debug("after jump_to_window()")
			button.show_all()
	def showme(self):
		self._logger.debug("entered showme")
		self.gtk_application_window.show()
		self._logger.debug("Window size: %s",self.gtk_application_window.get_size())
	def _on_close(self,*args):
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
	def add_incoming_call(self,account,prm):
		self._logger.debug("entered add_new_call")
		gtkapplication.api.audio.ringer.start_ringer()
		self._logger.debug("ringer started")
		self.increment_call_count()
		self._create_incoming_call_frame(account,prm)
	def _create_incoming_call_frame(self,account,prm):
		self._logger.debug('entered add_incoming_call_box')
		glade_file_name='incoming_call_frame.glade'
		self._gtk_builder.add_from_file(__file__,glade_file_name)
		frame=self._gtk_builder.get_object("call_frame")
		if self._window_unique_key is None:
			self._logger.debug("window_unique_key is None, not creating signal handler")
		else:
			signal_handler=gtkapplication.ui.voice.voice_call_inbound_signal_handler.VoiceCallInboundSignalHandler(self._gtk_builder,account,prm,frame,self.decrement_call_count)
			self._gtk_builder.connect_signals(signal_handler)
		self.position_frame_in_grid()
	def position_frame_in_grid(self):
		self._logger.debug("entered position_frame_in_grid")
		self._logger.debug("number of calls = %d",self._number_of_calls)
		active_call_grid=self._gtk_builder.get_object("active_call_grid")
		frame=self._gtk_builder.get_object("call_frame")
		row=0
		col=0
		if self._number_of_calls==1:
			row=0
			col=0
		elif self._number_of_calls==2:
			row=1
			col=0
		elif self._number_of_calls==3:
			row=2
			col=0
		elif self._number_of_calls==4:
			row=3
			col=0
		else:
			raise ValueError("{0} is an invalid number of calls".format(self._number_of_calls))
		active_call_grid.attach(frame,col,row,1,1)
	def add_outgoing_call(self,contact,active_contact_point_index):
		self._logger.debug("entered add_outgoing_call")
		self.increment_call_count()
		self._create_outgoing_call_frame(contact,active_contact_point_index)
	def add_voicemail(self,recording_dto,contact,active_contact_point_index):
		self._logger.debug("entered add_voicemail")
		frame_factory=gtkapplication.ui.voicemail.dashboard_voicemail_frame.FrameFactory()
		gtk_window=self._gtk_builder.get_object("voice_window")
		frame=frame_factory.create_voicemail_frame(self._gtk_builder,recording_dto,contact,active_contact_point_index,gtk_window)
		voicemail_container_box=self._gtk_builder.get_object("notification_box")
		voicemail_container_box.pack_start(frame,True,True,0)
		self._increment_voicemail_count()
	def _create_outgoing_call_frame(self,contact,active_contact_point_index):
		self._logger.debug('entered _create_outgoing_call_frame')
		glade_file_name='outgoing_call_frame.glade'
		self._gtk_builder.add_from_file(__file__,glade_file_name)
		caller_id_label=self._gtk_builder.get_object("caller_id_label")
		caller_id_label.set_text("{0} {1}".format(contact.name,contact.contact_points[active_contact_point_index].uri_string_national))
		frame=self._gtk_builder.get_object("call_frame")
		if self._window_unique_key is None:
			self._logger.debug("window_unique_key is None, not creating signal handler")
		else:
			signal_handler=gtkapplication.ui.voice.voice_call_outgoing_signal_handler.VoiceCallOutboundSignalHandler(self._gtk_builder,contact,active_contact_point_index,frame,self.decrement_call_count)
			self._gtk_builder.connect_signals(signal_handler)
		self.position_frame_in_grid()
	def increment_call_count(self):
		self._logger.debug("entered increment_call_count")
		self._number_of_calls+=1
		active_call_count_label=self._gtk_builder.get_object("active_call_count_label")
		if self._number_of_calls==0:
			active_call_count_label.set_text("No Active Calls")
		elif self._number_of_calls==1:
			active_call_count_label.set_text("1 Active Call")
		else:
			active_call_count_label.set_text("{0} Active Calls".format(self._number_of_calls))
	def decrement_call_count(self):
		self._logger.debug("entered decrement_call_count")
		self._number_of_calls-=1
		active_call_count_label=self._gtk_builder.get_object("active_call_count_label")
		if self._number_of_calls==0:
			active_call_count_label.set_text("No Active Calls")
		elif self._number_of_calls==1:
			active_call_count_label.set_text("1 Active Call")
		else:
			active_call_count_label.set_text("{0} Active Calls".format(self._number_of_calls))
	def _increment_voicemail_count(self):
		self._logger.debug("entered _increment_voicemail_count")
		self._number_of_voicemails+=1
		active_call_count_label=self._gtk_builder.get_object("voicemail_count_label")
		if self._number_of_voicemails==0:
			active_call_count_label.set_text("No Voicemail")
		elif self._number_of_voicemails==1:
			active_call_count_label.set_text("1 Voicemail")
		else:
			active_call_count_label.set_text("{0} Voicemails".format(self._number_of_voicemails))
	def _on_conference_call_action(self,action,user_data):
		self._logger.debug("entered _on_conference_call_action")
		sip_calls_dict=gtkapplication.api.sip.sip_call_state.sip_calls
		self._logger.debug("number of calls = %d, len(sip_calls_dict) = %d",self._number_of_calls,len(sip_calls_dict))
		assert self._number_of_calls==len(sip_calls_dict)
		active_call_count_label=self._gtk_builder.get_object("active_call_count_label")
		if self._number_of_calls==0 or self._number_of_calls==1:
			self._logger.debug("0 or 1 call, cannot start conference")
		elif self._number_of_calls==2:
			self._logger.debug("2 calls, starting conference")
			self._logger.debug("sip_calls_dict has %d items",len(sip_calls_dict))
			call_media_0=sip_calls_dict[0].call_media
			self._logger.debug("got call media 0")
			call_media_1=sip_calls_dict[1].call_media
			self._logger.debug("got call media 1")
			call_media_0.startTransmit(call_media_1)
			self._logger.debug("transmit 0 --> 1")
			call_media_1.startTransmit(call_media_0)
			self._logger.debug("transmit 1 --> 0")
			active_call_count_label.set_text("Conference Call with 2 other callers")
		elif self._number_of_calls==3:
			self._logger.debug("3 calls, starting conference")
			call_media_0=sip_calls_dict[0].call_media
			self._logger.debug("got call media 0")
			call_media_1=sip_calls_dict[1].call_media
			self._logger.debug("got call media 1")
			call_media_2=sip_calls_dict[2].call_media
			self._logger.debug("got call media 2")
			call_media_0.startTransmit(call_media_1)
			self._logger.debug("transmit 0 --> 1")
			call_media_0.startTransmit(call_media_2)
			self._logger.debug("transmit 0 --> 2")
			call_media_1.startTransmit(call_media_0)
			self._logger.debug("transmit 1 --> 0")
			call_media_1.startTransmit(call_media_2)
			self._logger.debug("transmit 1 --> 2")
			call_media_2.startTransmit(call_media_0)
			self._logger.debug("transmit 2 --> 0")
			call_media_2.startTransmit(call_media_1)
			self._logger.debug("transmit 2 --> 1")
			active_call_count_label.set_text("Conference Call with 3 other callers")
		elif self._number_of_calls==4:
			call_media_0=sip_calls_dict[0].call_media
			self._logger.debug("got call media 0")
			call_media_1=sip_calls_dict[1].call_media
			self._logger.debug("got call media 1")
			call_media_2=sip_calls_dict[2].call_media
			self._logger.debug("got call media 2")
			call_media_3=sip_calls_dict[3].call_media
			self._logger.debug("got call media 3")
			call_media_0.startTransmit(call_media_1)
			self._logger.debug("transmit 0 --> 1")
			call_media_0.startTransmit(call_media_2)
			self._logger.debug("transmit 0 --> 2")
			call_media_0.startTransmit(call_media_3)
			self._logger.debug("transmit 0 --> 3")
			call_media_1.startTransmit(call_media_0)
			self._logger.debug("transmit 1 --> 0")
			call_media_1.startTransmit(call_media_2)
			self._logger.debug("transmit 1 --> 2")
			call_media_1.startTransmit(call_media_3)
			self._logger.debug("transmit 1 --> 3")
			call_media_2.startTransmit(call_media_0)
			self._logger.debug("transmit 2 --> 0")
			call_media_2.startTransmit(call_media_1)
			self._logger.debug("transmit 2 --> 1")
			call_media_2.startTransmit(call_media_3)
			self._logger.debug("transmit 2 --> 3")
			call_media_3.startTransmit(call_media_0)
			self._logger.debug("transmit 3 --> 0")
			call_media_3.startTransmit(call_media_1)
			self._logger.debug("transmit 3 --> 1")
			call_media_3.startTransmit(call_media_2)
			self._logger.debug("transmit 3 --> 2")
			active_call_count_label.set_text("Conference Call with 4 other callers")
		else:
			raise ValueError("{0} is not a valid number of calls".format(self._number_of_calls))