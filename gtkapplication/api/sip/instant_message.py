import logging
import mimetypes
import codecs
import collections
import pjsua2 as pj
import gtkapplication.api.contacts.contact_manager
from gtkapplication.api.sip.sipuri import UriValidator
import gtkapplication.ui.gtk.window_manager
import gtkapplication.api.contacts.contact
import gtkapplication.api.contacts.contact_point
import gtkapplication.api.audio.ringer
import gtkapplication.ui.gtk.gtk_dialog
import gtkapplication.api.twilio
import gtkapplication.api.audio.downloader
import gtkapplication.ui.dashboard
import gtkapplication.api.sip.inbound.sms_message_processor
import gtkapplication.api.sip.inbound.missed_call_processor
import gtkapplication.api.sip.inbound.voicemail_message_processor
import gtkapplication.api.sip.inbound.sip_text_message_processor
import gtkapplication.api.sip.free_buddy_text_delivery_failure
import gtkapplication.api.sip.inbound.blocked_call_processor
import gtkapplication.api.sip.inbound.blocked_sms_processor
import gtkapplication.api.sip.inbound.sms_delivery_failure_processor
class InstantMessageHandler:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def send_text(self,buddy,text_data):
		self._logger.debug('entered send_text')
		send_im_param=pj.SendInstantMessageParam()
		send_im_param.content=text_data
		send_im_param.userData=None
		buddy.sendInstantMessage(send_im_param)
		self._logger.debug("sent instant msg %s to %s",text_data,str(buddy))
	def send_file(self,buddy,file_path):
		(mime_type,mime_encoding)=mimetypes.guess_type(file_path)
		self._logger.debug('mime_type = %s',mime_type)
		self._logger.debug('mime_encoding = %s',mime_encoding)
		if mime_type is None:
			self._logger.debug('could not determine mime type for file %s',file_path)
		else:
			with open(file_path,'rb')as file_reader:
				file_contents_bytes=file_reader.read()
				file_reader.close()
			self._logger.debug('len(file_contents_bytes) = %s',file_contents_bytes)
			base64_data=codecs.encode(file_contents_bytes,'base64')
			string_data=base64_data.decode('utf-8')
			send_im_param=pj.SendInstantMessageParam()
			send_im_param.content=string_data
			send_im_param.contentType=mime_type
			buddy.sendInstantMessage(send_im_param)
			self._logger.debug("sent binary instant msg with length %d to %s",len(file_contents_bytes),str(buddy))
			buddy=None
			self._logger.debug('buddy set to None')
	def onInstantMessage(self,prm):
		self._logger.debug('prm.msgBody = %s',prm.msgBody)
		self._logger.debug('prm.contentType = %s',prm.contentType)
		self._logger.debug("new instant message from %s",prm.fromUri)
		sip_uri_validator=UriValidator()
		is_valid_sip_uri=sip_uri_validator.validateSipUri(prm.fromUri)
		if not is_valid_sip_uri:
			self._logger.debug('%s is not a valid sip uri, exiting',prm.fromUri)
			return
		message_body=prm.msgBody
		message_lines=message_body.split('\n')
		message_first_line=message_lines[0]
		if message_first_line.startswith("[x-pyphone-new-voicemail-received]"):
			self._logger.info("New voicemail received")
			message_processor=gtkapplication.api.sip.inbound.voicemail_message_processor.InboundProcessor()
			message_processor.process_voicemail_message(message_body)
		elif message_first_line.startswith("[x-pyphone-missed-call-caller]"):
			self._logger.info("Missed call")
			message_processor=gtkapplication.api.sip.inbound.missed_call_processor.InboundProcessor()
			message_processor.process_missed_call_message(message_body)
		elif message_first_line.startswith("x-pyphone-received-from-number="):
			self._logger.info("New SMS Message")
			message_processor=gtkapplication.api.sip.inbound.sms_message_processor.InboundProcessor()
			message_processor.process_sms_message(message_body)
		elif message_first_line.startswith("[x-pyphone-call-blocked]"):
			self._logger.info("Blocked Call Notification")
			message_processor=gtkapplication.api.sip.inbound.blocked_call_processor.InboundProcessor()
			message_processor.process_blocked_call_message(message_body)
		elif message_first_line.startswith("[x-pyphone-sms-blocked]"):
			self._logger.info("Blocked SMS Notification")
			message_processor=gtkapplication.api.sip.inbound.blocked_sms_processor.InboundProcessor()
			message_processor.process_blocked_sms_message(message_body)
		elif message_first_line.startswith("[x-pyphone-sms-delivery-failed]"):
			message_processor=gtkapplication.api.sip.inbound.sms_delivery_failure_processor.InboundProcessor()
			message_processor.process_sms_delivery_failure(message_body)
		else:
			self._logger.info("Buddy Text Message")
			message_processor=gtkapplication.api.sip.inbound.sip_text_message_processor.InboundProcessor()
			message_processor.process_sip_text_message(prm)
	def onInstantMessageStatus(self,prm):
		self._logger.debug('enter onInstantMessageStatus prm.code = %s, prm.reason = %s',prm.code,prm.reason)
		if prm.code==200:
			self._logger.debug("message delivered to '%s' OK",prm.toUri)
		else:
			self._logger.debug("message delivery failure to '%s', creating failed IM notification",prm.toUri)
			sms_message_delivery_failure_processor=gtkapplication.api.sip.free_buddy_text_delivery_failure.FreeBuddyTextDeliveryFailureProcessor()
			Prm=collections.namedtuple("OnInstantMessageStatusParamType",field_names='toUri msgBody code reason')
			prm_copy=Prm(prm.toUri,prm.msgBody,prm.code,prm.reason)
			sms_message_delivery_failure_processor.process_sip_text_delivery_failure(prm_copy)
	def onTypingIndication(self,prm):
		self._logger.debug('entered onTypingIndication')
		self._logger.debug('prm.fromUri = %s',prm.fromUri)
		self._logger.debug('prm.isTyping = %s',prm.isTyping)