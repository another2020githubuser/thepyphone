import logging
import pjsua2 as pj
from gtkapplication.api.sip.pjsip_container_accessor import PjSipContainerAccessor
import gtkapplication.api.sip.instant_message
import gtkapplication.api.audio.player
import gtkapplication.api.audio.audio_manager
import gtkapplication.data
class PjSipRoleE:
	PJSIP_ROLE_UAC=0,
	PJSIP_ROLE_UAS=1
class SipCall(pj.Call):
	def __init__(self,acc,call_id,on_call_disconnected_handler=None,on_call_state_change_handler=None):
		pj.Call.__init__(self,acc,call_id)
		self._logger=logging.getLogger(__name__)
		self._account=acc
		self._on_call_disconnected_handler=on_call_disconnected_handler
		self._on_call_state_change_handler=on_call_state_change_handler
		self._active_call_media_count=0
		self._total_media_count=0
		self._call_state=None
		self._call_media=None
	@property
	def call_state(self):
		return self._call_state
	@property
	def total_media_count(self):
		return self._total_media_count
	@property
	def active_media_count(self):
		return self._active_call_media_count
	@property
	def call_media(self):
		return self._call_media
	def __repr__(self):
		ci=self.getInfo()
		return "ci.state = {0}({1}), hasMedia = {2}, isActive = {3}".format(ci.stateText,ci.state,self.hasMedia(),self.isActive())
	def onStreamCreated(self,prm):
		self._logger.debug('entered onStreamCreated')
		self._logger.debug('prm.streamIdx = %s',prm.streamIdx)
		self._logger.debug('prm.destroyPort = %s',prm.destroyPort)
		self._logger.debug('state = %s',self)
	def onStreamDestroyed(self,prm):
		self._logger.debug('entered onStreamDestroyed')
		self._logger.debug('prm.streamIdx = %s',prm.streamIdx)
		self._logger.debug('state = %s',self)
	def onCallState(self,prm):
		self._logger.debug('entered onCallState')
		call_info=self.getInfo()
		self._on_call_state_change_handler(call_info.state,call_info.stateText,call_info.id)
		self._logger.debug("after _on_call_state_change_handler")
		self._total_media_count=len(call_info.media)
		self._logger.debug('len(ci.media) = %s',self._total_media_count)
		self._call_state=call_info.state
	def onCallMediaState(self,prm):
		self._logger.debug('enter onCallMediaState')
		ci=self.getInfo()
		self._logger.debug('state on enter= %s',self)
		self._logger.debug('%d total media',len(ci.media))
		audio_manager=gtkapplication.api.audio.audio_manager.AudioManager()
		audio_manager.stop_play_audio()
		pjsip_accessor=PjSipContainerAccessor()
		ep=pjsip_accessor.get_pjsip_endpoint()
		aud_dev_mgr=ep.audDevManager()
		mic=aud_dev_mgr.getCaptureDevMedia()
		call_media_list=self.enumerate_active_call_media()
		self._active_call_media_count=len(call_media_list)
		self._logger.debug("%d active call media",self._active_call_media_count)
		assert len(call_media_list)==1
		self._call_media=call_media_list[0]
		speaker=aud_dev_mgr.getPlaybackDevMedia()
		mic.startTransmit(self._call_media)
		self._call_media.startTransmit(speaker)
	def enumerate_active_call_media(self):
		self._logger.debug("entered enumerate_active_call_media")
		active_audio_media=[]
		ci=self.getInfo()
		media_count=0
		for mi in ci.media:
			media_count+=1
			if mi.type==pj.PJMEDIA_TYPE_AUDIO and mi.status==pj.PJSUA_CALL_MEDIA_ACTIVE:
				self._logger.debug('active audio media at index %d',mi.index)
				media=self.getMedia(mi.index)
				audio_media=pj.AudioMedia.typecastFromMedia(media)
				active_audio_media.append(audio_media)
		self._logger.debug("Total autio media count = %d, active audio media count = %d",media_count,len(active_audio_media))
		return active_audio_media
	def onInstantMessage(self,prm):
		self._logger.debug('enter onInstantMessage, account_id = %d, prm.fromUri = %s, prm.toUri = %s',self._account.getId(),prm.fromUri,prm.toUri)
		self._logger.debug('prm.msgBody = %s',prm.msgBody)
		self._logger.debug('prm.contentType = %s',prm.contentType)
		instant_message_handler=gtkapplication.api.sip.instant_message.InstantMessageHandler()
		instant_message_handler.onInstantMessage(prm)
	def onInstantMessageStatus(self,prm):
		self._logger.debug('enter onInstantMessageStatus prm.code = %s, prm.reason = %s, call = %s',prm.code,prm.reason,self)
		instant_message_handler=gtkapplication.api.sip.instant_message.InstantMessageHandler()
		instant_message_handler.onInstantMessageStatus(prm)
	def onTypingIndication(self,prm):
		self._logger.debug('entered onTypingIndication')
		instant_message_handler=gtkapplication.api.sip.instant_message.InstantMessageHandler()
		instant_message_handler.onTypingIndication(prm)
	def onDtmfDigit(self,prm):
		self._logger.info('entered onDtmfDigit')
		self._logger.info('prm.digit = %s',prm.digit)
	def onCallSdpCreated(self,prm):
		self._logger.debug("entered onCallSdpCreated")
		self._logger.debug("sdp = %s",prm.sdp.wholeSdp)
		self._logger.debug("remote sdp = %s",prm.remSdp.wholeSdp)
	def stateText(self,state):
		if state==0:
			return "PJSUA_MED_TP_NULL"
		elif state==1:
			return "PJSUA_MED_TP_CREATING"
		elif state==2:
			return "PJSUA_MED_TP_IDLE"
		elif state==3:
			return "PJSUA_MED_TP_INIT"
		elif state==4:
			return "PJSUA_MED_TP_RUNNING"
		elif state==4:
			return "PJSUA_MED_TP_DISABLED"
		else:
			raise ValueError("Invalid value for pjsua_med_tp_st: {0}".format(state))
	def onCallMediaTransportState(self,prm):
		self._logger.debug('entered onCallMediaTransportState, medIdx = %d, state is %s (%d)',prm.medIdx,self.stateText(prm.state),prm.state)
		assert prm.status==0
		assert prm.sipErrorCode==0