import logging
import pjsua2
from gtkapplication.api.sip.pjsip_container import sip_container
import gtkapplication.api.sip.sip_call_state
class DtmfTone:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def play_dtmf_tone(self,digit,dtmf_type):
		self._logger.debug("entered play_dtmf_tone, dtmf_type is %s",dtmf_type)
		if dtmf_type=="Off":
			self._logger.debug("DTMF Off, Skipping tone")
		elif dtmf_type=="In Band":
			self._play_dtmf_tone_in_band(digit)
		elif dtmf_type=="Out of Band (RFC 2833)":
			self._play_dtmf_tone_out_of_band_rfc_2833(digit)
		elif dtmf_type=="Out of Band (SIP INFO)":
			self._play_dtmf_tone_out_of_band_sip_info(digit)
		else:
			raise ValueError("Invalid dtmf_type: {0}".format(dtmf_type))
	def _play_dtmf_tone_out_of_band_sip_info(self,digit):
		self._logger.debug("entered play_dtmf_tone_out_of_band_sip_info")
		if len(gtkapplication.api.sip.sip_call_state.sip_calls)==0:
			self._logger.debug("Ignoring attempt to send digit '%s' while sip_call is None",digit)
		else:
			sip_call=gtkapplication.api.sip.sip_call_state.sip_calls[0]
			if sip_call.call_state==pjsua2.PJSIP_INV_STATE_CONFIRMED:
				prm=pjsua2.CallSendDtmfParam()
				prm.digits=digit
				prm.method=pjsua2.PJSUA_DTMF_METHOD_SIP_INFO
				sip_call.sendDtmf(prm)
				self._logger.debug("sent digit '%s' to remote",digit)
			else:
				self._logger.debug("Call state not confirmed, skipping DTMF tone")
	def _play_dtmf_tone_out_of_band_rfc_2833(self,digit):
		self._logger.debug("entered play_dtmf_tone_out_of_band_rfc_2833")
		if len(gtkapplication.api.sip.sip_call_state.sip_calls)==0:
			self._logger.debug("Ignoring attempt to send digit '%s' while sip_call is None",digit)
		else:
			self._logger.debug("active calls, count = %d",len(gtkapplication.api.sip.sip_call_state.sip_calls))
			sip_call=gtkapplication.api.sip.sip_call_state.sip_calls[0]
			self._logger.debug("got sip call")
			if sip_call.call_state==pjsua2.PJSIP_INV_STATE_CONFIRMED:
				self._logger.debug("Call state confirmed, sending DTMF tone")
				prm=pjsua2.CallSendDtmfParam()
				prm.digits=digit
				prm.method=pjsua2.PJSUA_DTMF_METHOD_RFC2833
				sip_call.sendDtmf(prm)
				self._logger.debug("sent digit '%s' to remote",digit)
			else:
				self._logger.debug("Call state not confirmed (%s), skipping DTMF tone",sip_call.call_state)
	def _play_dtmf_tone_in_band(self,digit):
		self._logger.debug("entered play_dtmf_tone")
		endpoint=sip_container.ep
		tone_digit_vector=pjsua2.ToneDigitVector()
		tone_digit=pjsua2.ToneDigit()
		tone_digit.digit=digit
		tone_digit.on_msec=500
		tone_digit_vector.append(tone_digit)
		tone_generator=sip_container.tone_generator
		assert tone_generator is not None,"PJ Sip Not Initialized"
		tone_generator.playDigits(tone_digit_vector,False)
		sink=endpoint.audDevManager().getPlaybackDevMedia()
		tone_generator.startTransmit(sink)
		tone_generator=None
		self._logger.debug("sent digit '%s' to remote",digit)