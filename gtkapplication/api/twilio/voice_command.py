import logging
import datetime
import operator
from dateutil import tz
from tzlocal import get_localzone
import twilio.rest
import twilio.twiml.voice_response
import gtkapplication.data.config_data
import gtkapplication.api.twilio.voice_mail_dto
import gtkapplication.api.audio.player
class VoiceCommand(object):
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self.twilio_account_sid=gtkapplication.data.config_data.PROFILE_DATA['twilio_account_sid']
		self.twilio_auth_token=gtkapplication.data.config_data.PROFILE_DATA['twilio_auth_token']
		self._logger.debug("twilio version is %s",twilio.__version__)
	def get_incomplete_calls_count(self):
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		phone_number_to=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
		calls_list=twilio_client.api.v2010.accounts(sid=self.twilio_account_sid).calls.list(to=phone_number_to)
		total_calls_count=len(calls_list)
		self._logger.debug('total calls_count = %s',total_calls_count)
		incomplete_calls_sid_list=[call.sid for call in calls_list if call.status!="completed"]
		self._logger.debug('len(incomplete_calls_sid_list) = %s',len(incomplete_calls_sid_list))
		return len(incomplete_calls_sid_list)
	def get_sent_calls_count(self):
		self._logger.debug("entered get_sent_calls_count")
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		my_phone_number=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
		calls_list=twilio_client.api.v2010.accounts(sid=self.twilio_account_sid).calls.list(from_=my_phone_number)
		sent_calls_count=len(calls_list)
		self._logger.debug("sent_calls_count = %s",sent_calls_count)
		return sent_calls_count
	def get_received_calls_count(self):
		self._logger.debug("entered get_received_calls_count")
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		my_phone_number=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
		calls_list=twilio_client.api.v2010.accounts(sid=self.twilio_account_sid).calls.list(to=my_phone_number)
		received_calls_count=len(calls_list)
		self._logger.debug("received_calls_count = %s",received_calls_count)
		return received_calls_count
	def get_voicemail_dto(self,from_number,to_number):
		self._logger.debug('entered get_voicemail')
		self._logger.debug('from_number = %s',from_number)
		self._logger.debug('to_number = %s',to_number)
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		all_recordings_list=twilio_client.api.v2010.accounts(sid=self.twilio_account_sid).recordings.list()
		recordings_count=len(all_recordings_list)
		self._logger.debug('recordings_count = %s',recordings_count)
		all_recording_call_sid_list=[recording.call_sid for recording in all_recordings_list]
		all_recording_call_data_list=[(recording.call_sid,recording.sid,recording.uri,recording.duration,recording.date_created,recording.status) for recording in all_recordings_list]
		self._logger.debug('recordings count = %d',len(all_recording_call_data_list))
		calls_list=twilio_client.api.v2010.accounts(sid=self.twilio_account_sid).calls.list(from_=from_number,to=to_number)
		calls_count=len(calls_list)
		self._logger.debug('calls count = %s',calls_count)
		calls_sid_list=[call.sid for call in calls_list]
		call_recording_sids_list=list(set(all_recording_call_sid_list)&set(calls_sid_list))
		self._logger.debug('%d calls with recordings',len(call_recording_sids_list))
		tz_local=get_localzone()
		vm_list=[]
		for call_recording_sid in call_recording_sids_list:
			self._logger.debug('examining call_sid %s',call_recording_sid)
			for recording_call_data in all_recording_call_data_list:
				if recording_call_data[5]!="completed":
					self._logger.debug('call recording not completed, omitting call sid %s with status = %s',call_recording_sid,recording_call_data[5])
				else:
					if recording_call_data[0]==call_recording_sid:
						self._logger.debug('matched call sid, creating voice mail dto')
						recording_sid=recording_call_data[1]
						recording_uri="https://api.twilio.com/{0}".format(recording_call_data[2].replace('.json',''))
						recording_duration=recording_call_data[3]+" seconds"
						date_created_rfc_2822=recording_call_data[4]
						date_created_local_time=date_created_rfc_2822.astimezone(tz_local).strftime("%Y-%m-%d %I:%M %p")
						voice_mail_dto=gtkapplication.api.twilio.voice_mail_dto.VoiceMailDto(date_created_local_time,recording_duration,recording_uri,recording_sid)
						self._logger.debug('voice_mail time stamp = %s, recording_sid = %s',date_created_local_time,recording_sid)
						vm_list.append(voice_mail_dto)
		sorted_vm_list=sorted(vm_list,reverse=True,key=operator.attrgetter('date_created_local_time'))
		self._logger.debug('voice mail count = %d',len(sorted_vm_list))
		self._logger.debug("vm list = %s",sorted_vm_list)
		return sorted_vm_list
	def get_voicemail_original(self,from_number,to_number,start_date):
		self._logger.debug('entered get_voicemail_original')
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		calls_list=twilio_client.api.v2010.accounts(sid=self.twilio_account_sid).calls.list(from_=from_number,to=to_number,start_time_after=start_date)
		calls_count=len(calls_list)
		self._logger.info('calls_count = %s',calls_count)
		tz_local=get_localzone()
		voice_mail_list=[]
		for call in calls_list:
			num_recordings=len(call.recordings.list())
			self._logger.debug('%d recordings',num_recordings)
			if num_recordings>0:
				for recording in call.recordings.list():
					date_created_rfc_2822=recording.date_created
					date_created_local_time=date_created_rfc_2822.astimezone(tz_local)
					self._logger.debug('date_created_local_time = %s',date_created_local_time)
					recording_uri="https://api.twilio.com/{0}".format(recording.uri.replace('.json',''))
					self._logger.debug('recording_uri = %s',recording_uri)
					self._logger.debug('recording.duration = %s seconds',recording.duration)
					recording_duration="{0} seconds".format(recording.duration)
					recording_sid=recording.sid
					voice_mail_dto=gtkapplication.api.twilio.voice_mail_dto.VoiceMailDto(date_created_local_time,recording_duration,recording_uri,recording_sid)
					voice_mail_list.append(voice_mail_dto)
		self._logger.info('%d messages',len(voice_mail_list))
		sorted_vm_list=sorted(voice_mail_list,reverse=True,key=operator.attrgetter('date_created_local_time'))
		for voice_mail in sorted_vm_list:
			self._logger.info('sorted voice_mail = %s',voice_mail)
		return sorted_vm_list
	def _create_elapsed_time_string(self,date_created_local_time):
		message_created_timedelta=datetime.datetime.now().replace(tzinfo=tz.tzlocal())-date_created_local_time
		days=message_created_timedelta.days
		secs=message_created_timedelta.seconds
		hours,remainder=divmod(secs,3600)
		minutes,seconds=divmod(remainder,60)
		elapsed_time_string='{0} day(s) {1} hours {2} minutes {3} seconds ago'.format(days,hours,minutes,seconds)
		self._logger.debug('elapsed_time_string = %s',elapsed_time_string)
		return elapsed_time_string
	def delete_voicemail(self,voicemail_sid):
		self._logger.debug('entered delete_voicemail')
		self._logger.debug('voicemail_sid = %s',voicemail_sid)
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		twilio_client.recordings(sid=voicemail_sid).delete()
		self._logger.debug('after recording.delete()')
	def get_contact_name_by_call_sid(self,call_sid):
		self._logger.debug('entered get_call_by_call_sid')
		self._logger.debug('call_sid = %s',call_sid)
		twilio_rest_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		twilio_call=twilio_rest_client.calls(sid=call_sid).fetch()
		calling_number=twilio_call.from_
		self._logger.debug('calling_number = %s',calling_number)
		calling_party=self.format_contact_for_display(calling_number)
		self._logger.debug('calling_party = %s',calling_party)
		return calling_party
	def format_contact_for_display(self,phone_number):
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		(contact,active_contact_point_index)=contact_manager.find_contact_by_phone_number(phone_number)
		self._logger.debug("contact = %s",contact)
		if contact is None:
			return phone_number
		else:
			return "{0}({1})".format(contact.name,contact.selected_contact_point.description)
	def get_contact_number_by_call_sid(self,call_sid):
		self._logger.debug('entered get_call_by_call_sid')
		self._logger.debug('call_sid = %s',call_sid)
		twilio_rest_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		twilio_call=twilio_rest_client.calls(sid=call_sid).fetch()
		from_phone_number=twilio_call.from_
		to_phone_number=twilio_call.to
		self._logger.debug('from_phone_number = %s, to_phone_number = %s',from_phone_number,to_phone_number)
		return (from_phone_number,to_phone_number)
	def get_recordings_count(self):
		twilio_rest_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		all_recordings=twilio_rest_client.recordings.list()
		return len(all_recordings)