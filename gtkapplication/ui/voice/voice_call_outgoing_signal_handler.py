import logging
import pjsua2
from gtkapplication.ui.voice.base_voice_signal_handler import BaseVoiceSignalHandler
import gtkapplication.api.sip.pjsip_container_accessor
import gtkapplication.ui.gtk.jump_to_window
import gtkapplication.api.sip.sip_call_state
import gi
gi.require_version('Gtk','3.0')
from gi.repository import GLib
class VoiceCallOutboundSignalHandler(BaseVoiceSignalHandler):
	def __init__(self,gtk_builder,contact,active_contact_point_index,frame,on_call_disconnected_handler):
		super().__init__(gtk_builder,frame,on_call_disconnected_handler)
		self._logger=logging.getLogger(__name__)
		self._call_id=-999
		self._gtk_builder=gtk_builder
		self._contact=contact
		self._active_contact_point_index=active_contact_point_index
		contact_point=contact.contact_points[active_contact_point_index]
		pjsip_accessor=gtkapplication.api.sip.pjsip_container_accessor.PjSipContainerAccessor()
		account=None
		if contact_point.point_type=='tel':
			self._logger.debug('PSTN call')
			account=pjsip_accessor.get_account_by_name("twilio")
			self._logger.debug('account = %s',account)
			dest_uri=contact_point.uri_string
			self._logger.debug('dest_uri = %s',dest_uri)
			idUri=account.cfg.idUri
			self._logger.debug("idUri = %s",idUri)
			sip_parser=gtkapplication.api.sip.sipuri.SipUriParser()
			parsed_uri=sip_parser.parseSipUri(idUri)
			pstn_sip_domain=parsed_uri.host
			self._logger.debug('pstn_sip_domain = %s',pstn_sip_domain)
			dest_uri="sip:{0}@{1}".format(dest_uri,pstn_sip_domain)
			self._logger.debug("dest_uri after formatting for twilio = %s",dest_uri)
			self._logger.debug('calling dest_uri = %s',dest_uri)
		elif contact_point.point_type=="x-sip":
			self._logger.debug('Buddy call')
			account=pjsip_accessor.get_account_by_name("sip")
			self._logger.debug('account = %r',account)
			dest_uri=contact_point.uri_string
			buddy=contact.buddy
			self._logger.debug("buddy = %r",buddy)
			self._logger.info("free buddy calling from %s to %s",account.uri,buddy.uri)
		else:
			raise ValueError("invalid point_type: {0}".format(contact_point.point_type))
		self._sip_call=gtkapplication.api.sip.sip_call.SipCall(account,pjsua2.PJSUA_INVALID_ID,on_call_state_change_handler=self.on_call_state_change_handler)
		contact_point=contact.contact_points[active_contact_point_index]
		self._logger.debug('point_type = %s',contact_point.point_type)
		self._call_status_label=self._gtk_builder.get_object("call_status_label")
		self._caller_id_label=self._gtk_builder.get_object("caller_id_label")
		self._caller_id_label.set_text("Calling {0}\n{1}".format(contact.name,contact_point.description))
		call_param=pjsua2.CallOpParam()
		call_param.opt.audioCount=1
		call_param.opt.videoCount=0
		self._sip_call.makeCall(dest_uri,call_param)
		call_info=self._sip_call.getInfo()
		self._call_id=call_info.id
		gtkapplication.api.sip.sip_call_state.sip_calls[call_info.id]=self._sip_call
		self._logger.debug('call_id = %s',call_info.id)
	def on_hangup_button_clicked(self,button):
		self._logger.debug('entered on_hangup_button_clicked')
		if self._sip_call is None:
			self._logger.debug('in hangup _sip_call() is None')
		else:
			self._logger.debug("hanging up call")
			prm=pjsua2.CallOpParam()
			self._sip_call.hangup(prm)
			self._logger.debug("after hangup()")
	def on_call_state_change_handler(self,call_state,call_state_text,call_id):
		self._logger.debug("entered on_call_state_change_handler")
		self._logger.debug("call_state = %s, call_state_text = %s, call_id = %s, contact = %s",call_state,call_state_text,call_id,self._contact)
		message="Call Status: {0} ({1})".format(call_state_text,call_state)
		self._call_status_label.set_text(message)
		if call_state==pjsua2.PJSIP_INV_STATE_DISCONNECTED:
			self._logger.debug("Call to %s disconnected, firing handler.",self._contact)
			self.on_call_disconnected_handler()
		self._call_status_label.show_all()