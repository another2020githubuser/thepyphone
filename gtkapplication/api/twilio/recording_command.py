import logging
import os
import os.path
import wave
import datetime
import twilio.rest
import pyaudio
import gtkapplication.api.twilio.voice_command
import gtkapplication.api.twilio.twilio_date_converter
import gtkapplication.api.utility.files
class RecordingCommand:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self.twilio_account_sid=gtkapplication.data.config_data.PROFILE_DATA['twilio_account_sid']
		self.twilio_auth_token=gtkapplication.data.config_data.PROFILE_DATA['twilio_auth_token']
		self._logger.debug("twilio version is %s",twilio.__version__)
	def delete_server_recording(self,recording_sid):
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		success=twilio_client.api.v2010.accounts(sid=self.twilio_account_sid).recordings(recording_sid).delete()
		if success:
			self._logger.debug("deleted recording sid %s ok",recording_sid)
		else:
			self._logger.warning("failed deleting recording sid %s",recording_sid)
		return success
	def get_recordings_list(self):
		self._logger.debug('entered get_recordings_list')
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		all_recordings_list=twilio_client.api.v2010.accounts(sid=self.twilio_account_sid).recordings.list()
		recordings_count=len(all_recordings_list)
		self._logger.debug('recordings_count = %s',recordings_count)
		return all_recordings_list
	def get_recordings_generator(self):
		self._logger.debug('entered get_recordings_generator')
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		recordings_generator=twilio_client.api.v2010.accounts(sid=self.twilio_account_sid).recordings.stream()
		return recordings_generator
	def get_mapped_twilio_recordings(self):
		self._logger.debug('entered get_recordings_dto')
		twilio_recordings=self.get_recordings_generator()
		recordings_dto=[]
		for twilio_recording in twilio_recordings:
			if twilio_recording.status=="absent":
				self.delete_server_recording(twilio_recording.sid)
				self._logger.debug("deleted recording with absent status and sid %s",twilio_recording.sid)
			else:
				recording_dto=self._twilio_recording_field_mapper(twilio_recording)
				if recording_dto is None:
					self._logger.debug("mapping layer returned none, ignoring")
				else:
					recordings_dto.append(recording_dto)
		return sorted(recordings_dto)
	def _twilio_recording_field_mapper(self,twilio_recording):
		self._logger.debug('status: %s, dateSent: %s, source: %s, duration: %s, sid = %s, uri = %s',twilio_recording.status,twilio_recording.date_created,twilio_recording.source,twilio_recording.duration,twilio_recording.sid,twilio_recording.uri)
		if twilio_recording.status=="absent":
			self._logger.warning("Unexpected code execution:  twilio_recording.status == absent, skipping voicemail download for sid %s",twilio_recording.sid)
			return None
		assert twilio_recording.date_created.tzinfo.zone=="UTC"
		date_created=twilio_recording.date_created.replace(tzinfo=None)
		call_sid=twilio_recording.call_sid
		voice_command=gtkapplication.api.twilio.voice_command.VoiceCommand()
		(from_phone_number,to_phone_number)=voice_command.get_contact_number_by_call_sid(call_sid)
		my_phone_number=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
		if to_phone_number!=my_phone_number:
			self._logger.debug("to_phone_number =%s, my_phone_number = %s, ignoring recording",to_phone_number,my_phone_number)
			return None
		recording_url="https://api.twilio.com/{0}".format(twilio_recording.uri).replace(".json","")
		self._logger.debug("recording_url = %s",recording_url)
		downloader=gtkapplication.api.audio.downloader.Downloader()
		file_name=downloader.download_voicemail(recording_url,from_phone_number)
		if file_name is None:
			self._logger.warning("voicemail download failed for uri %s",recording_url)
			return None
		db=gtkapplication.api.voicemail.controller.VoicemailController()
		db.insert_voicemail(date_created,from_phone_number,twilio_recording.duration,twilio_recording.sid,recording_url,file_name)
		self._logger.debug("after db.insert_voicemail()")
		recording_dto=gtkapplication.api.twilio.RecordingDto(date_created=date_created,from_phone_number=from_phone_number,recording_duration=int(twilio_recording.duration),recording_sid=twilio_recording.sid,recording_url=recording_url,file_name=file_name)
		self._logger.debug("recording_dto = %s",recording_dto)
		assert isinstance(recording_dto.date_created_utc,datetime.datetime)
		assert isinstance(recording_dto.recording_duration,int)
		self.delete_server_recording(twilio_recording.sid)
		return recording_dto
	def get_recordings_generator_for_call(self,call_sid):
		self._logger.debug("entered get_recordings_generator_for_call")
		self._logger.debug("call_sid = %s",call_sid)
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		recordings_generator=twilio_client.recordings.stream(call_sid=call_sid)
		return recordings_generator
	def get_recording_by_recording_sid(self,recording_sid):
		self._logger.debug("entered get_recording_by_recording_sid")
		self._logger.debug("recording_sid = %s",recording_sid)
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		recording=twilio_client.recordings(recording_sid).fetch()
		return recording
	def get_recording_details_formatted(self,recording_sid):
		self._logger.debug('entered get_recording_details_formatted')
		self._logger.debug('recording_sid = %s',recording_sid)
		twilio_rest_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		twilio_recording=twilio_rest_client.recordings(sid=recording_sid).fetch()
		call_properties=vars(twilio_recording)['_properties']
		recording_properties_string=""
		for key,val in sorted(call_properties.items()):
			recording_properties_string+="{0} = {1}\n".format(key,val)
		self._logger.debug('recording_properties_string = %s',recording_properties_string)
		return recording_properties_string
	def get_voicemail_dto_for_call(self,call_sid):
		self._logger.debug('entered get_voicemail_dto_for_call')
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		twilio_recordings_list=twilio_client.recordings.list(call_sid=call_sid)
		voice_mail_list=[]
		for voice_mail_dto in map(self._map_twilio_recording_to_voicemail_dto,twilio_recordings_list):
			voice_mail_list.append(voice_mail_dto)
		return voice_mail_list
	def _map_twilio_recording_to_voicemail_dto(self,twilio_recording):
		date_localizer=gtkapplication.api.twilio.twilio_date_converter.RFC2822Converter()
		date_created_local_time=date_localizer.to_local(twilio_recording.date_created)
		self._logger.debug('date_created_local_time = %s',date_created_local_time)
		recording_uri="https://api.twilio.com/{0}".format(twilio_recording.uri.replace('.json',''))
		self._logger.debug('recording_uri = %s',recording_uri)
		self._logger.debug('recording.duration = %s seconds',twilio_recording.duration)
		recording_duration="{0} seconds".format(twilio_recording.duration)
		recording_sid=twilio_recording.sid
		voice_mail_dto=gtkapplication.api.twilio.voice_mail_dto.VoiceMailDto(date_created_local_time,recording_duration,recording_uri,recording_sid)
		return voice_mail_dto
	def download_and_save_url(self,url):
		self._logger.debug('entered download_and_save_url')
		self._logger.debug('url = %s',url)
		unique_file_name=gtkapplication.api.utility.files.create_unique_file_name(".wav")
		self._logger.debug('unique_file_name = %s',unique_file_name)
		gtkapplication.api.utility.files.download_and_save_uri(url,unique_file_name)
		return unique_file_name
	def play_url(self,url):
		self._logger.debug('entered play_url')
		self._logger.debug('url = %s',url)
		unique_file_name=self.download_and_save_url(url)
		self._logger.debug('unique_file_name = %s',unique_file_name)
		self.play_wav_file(unique_file_name)
		self._logger.debug('after _play_wav_file')
		os.remove(unique_file_name)
		self._logger.debug('removed file %s',unique_file_name)
	def play_wav_file(self,wav_file_path):
		self._logger.debug('entered play_wav_file')
		self._logger.debug('wav_file_path = %s',wav_file_path)
		assert os.path.exists(wav_file_path)
		wav_file=wave.open(wav_file_path,"rb")
		self._logger.debug('wav file opened')
		pyaudio_player=pyaudio.PyAudio()
		self._logger.debug('pyaudio player created')
		stream=pyaudio_player.open(format=pyaudio_player.get_format_from_width(wav_file.getsampwidth()),channels=wav_file.getnchannels(),rate=wav_file.getframerate(),output=True)
		self._logger.debug('stream opened')
		stream_chunk_size=1024
		self._logger.debug('stream_chunk_size = %s',stream_chunk_size)
		data=wav_file.readframes(stream_chunk_size)
		self._logger.debug('got 1st chunk')
		chunk_counter=0
		while data:
			stream.write(data)
			data=wav_file.readframes(stream_chunk_size)
			chunk_counter+=1
		self._logger.debug('done playing, played %d chunks, cleaning up',chunk_counter)
		stream.stop_stream()
		stream.close()
		self._logger.debug('stream closed')
		pyaudio_player.terminate()
		self._logger.debug('after pyaudio terminate()')
		wav_file.close()
		self._logger.debug('after wav_file.close()')