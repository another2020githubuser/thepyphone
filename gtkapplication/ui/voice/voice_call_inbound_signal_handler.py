import logging
import pjsua2
import gtkapplication.ui.gtk.gtk_builder
from gtkapplication.ui.voice.base_voice_signal_handler import BaseVoiceSignalHandler
class VoiceCallInboundSignalHandler(BaseVoiceSignalHandler):
	def __init__(self,gtk_builder,account,prm,frame,parent_call_disconnected_handler):
		self._logger=logging.getLogger(__name__)
		super().__init__(gtk_builder,frame,parent_call_disconnected_handler)
		self._gtk_builder=gtk_builder
		self._call_id=prm.callId
		self._sip_call=gtkapplication.api.sip.sip_call.SipCall(account,self._call_id,on_call_state_change_handler=self.on_call_state_change_handler)
		call_prm=pjsua2.CallOpParam()
		call_prm.statusCode=180
		self._sip_call.answer(call_prm)
		call_info=self._sip_call.getInfo()
		self._logger.debug("incoming call from '%s' to %s",call_info.remoteUri,account.uri)
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		(contact,active_contact_point_index)=contact_manager.find_contact_by_sip_uri(call_info.remoteUri,True)
		self._contact=contact
		self._active_contact_point_index=active_contact_point_index
		self._logger.info("contact = %s, active_contact_point_index = %s",contact,active_contact_point_index)
		contact_point=contact.contact_points[active_contact_point_index]
		assert contact_point.point_type in ["x-sip","tel"]
		if contact_point.point_type=="tel":
			caller_id="Incoming call from {0} ({1})".format(contact.name,contact_point.uri_string_national)
		elif contact_point.point_type=="x-sip":
			caller_id="Free Buddy call from {0}".format(contact.name)
		self._logger.info("caller_id = %s, point_type = %s",caller_id,contact_point.point_type)
		self._caller_id_label.set_text(caller_id)
		self._dialog_button_clicked=False
		gtkapplication.api.sip.sip_call_state.sip_calls[call_info.id]=self._sip_call
	def on_answer_button_clicked(self,button):
		self._logger.debug('entered on_answer_button_clicked')
		self._dialog_button_clicked=True
		if self._sip_call is None:
			self._logger.warning('attempt to answer, but sip_call is None')
		else:
			gtkapplication.api.audio.ringer.stop_ringer()
			self._logger.debug('attempting to answer call from %s',self._contact.name)
			call_prm=pjsua2.CallOpParam()
			call_prm.statusCode=200
			self._logger.debug("About to answer call with ID %d",self._call_id)
			self._sip_call.answer(call_prm)
			self._logger.debug('call answered from %s',self._contact.name)
			button.hide()
	def on_hangup_button_clicked(self,button):
		self._logger.debug('entered on_hangup_button_clicked')
		self._dialog_button_clicked=True
		if self._sip_call is None:
			self._logger.debug('in reject _sip_call() is None')
		else:
			self._logger.debug('sip_call is not None')
			button_label=button.get_label()
			self._logger.debug("button_label = %s",button_label)
			assert button_label in ["Reject","Hang Up"]
			self._logger.debug("button.get_label = %s",button_label)
			if button_label=="Reject":
				self._logger.debug('call rejected from %s.  Call ID = %d',self._contact.name,self._call_id)
				call_prm=pjsua2.CallOpParam()
				call_prm.statusCode=486
				self._sip_call.answer(call_prm)
				self._logger.debug('after answer with 486')
			elif button_label=="Hang Up":
				self._logger.debug("Hang Up action")
				self.hangup()
	def on_call_disconnected_handler(self):
		self._logger.debug("entered on_call_disconnected_handler")
		if self._dialog_button_clicked:
			self._logger.debug("Dialog button clicked, call was answered")
		else:
			self._logger.debug("Dialog button NOT clicked, call not answered, maybe showing missed call notification")
			contact_point=self._contact.contact_points[self._active_contact_point_index]
			assert contact_point.point_type in ["x-sip","tel"]
			if contact_point.point_type=="tel":
				self._logger.debug("contact point is tel, not creating missed call notification")
			elif contact_point.point_type=="x-sip":
				self._logger.debug("missed call from free buddy, creating missed call notification")
				window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
				dashboard_ui=window_manager.get_dashboard_window()
				dashboard_ui.add_missed_call_notification(self._contact,self._active_contact_point_index)
		super().on_call_disconnected_handler()
	def hangup(self):
		self._logger.debug('entered hangup')
		self._logger.debug('before hangup, sip_call = %s',self._sip_call)
		prm=pjsua2.CallOpParam()
		if self._sip_call is not None:
			self._sip_call.hangup(prm)
		self._logger.debug('after sip_call.hangup(),sip_call = %s',self._sip_call)