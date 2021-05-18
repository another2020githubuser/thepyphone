import logging
import pickle
import os.path
import gtkapplication.api.twilio.sms_command
import gtkapplication.api.twilio.voice_command
import gtkapplication.data
class TwilioStateManager:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._pickle_file_name='twilio_state_dictionary.pickle'
		self.pickle_file_path=os.path.join(gtkapplication.data.get_data_folder_location(),self._pickle_file_name)
		self._logger.debug("pickle_file_path = %s",self.pickle_file_path)
	def unpickle_twilio_state(self):
		self._logger.debug("entered unpickle_twilio_state")
		self._logger.debug("pickle_file_path = %s",self.pickle_file_path)
		if os.path.exists(self.pickle_file_path):
			self._logger.debug("pickle file exists")
			file_handle=open(self.pickle_file_path,'rb')
			twilio_state_dictionary=pickle.load(file_handle)
			file_handle.close()
			self._logger.debug("twilio_state_dictionary = %s",twilio_state_dictionary)
			return twilio_state_dictionary
		else:
			raise FileNotFoundError("{0} does not exist".format(os.path.abspath(self.pickle_file_path)))
	def get_twilio_state_dictionary(self):
		self._logger.debug("entered get_twilio_state_dictionary")
		sms_command=gtkapplication.api.twilio.sms_command.SmsCommand()
		voice_command=gtkapplication.api.twilio.voice_command.VoiceCommand()
		sms_sent_count=sms_command.get_sent_sms_count()
		self._logger.debug("sms_sent_count = %d",sms_sent_count)
		recording_count=voice_command.get_recordings_count()
		self._logger.debug("recording_count = %d",recording_count)
		voice_count=voice_command.get_sent_calls_count()
		self._logger.debug("voice_count = %d",voice_count)
		twilio_state_dictionary={"sms_count":sms_sent_count,"recording_count":recording_count,"voice_count":voice_count}
		self._logger.debug("twilio_state_dictionary = %s",twilio_state_dictionary)
		return twilio_state_dictionary
	def get_twilio_state_string(self):
		self._logger.debug("entered get_twilio_state_dictionary2")
		sms_command=gtkapplication.api.twilio.sms_command.SmsCommand()
		voice_command=gtkapplication.api.twilio.voice_command.VoiceCommand()
		sms_sent_count=sms_command.get_sent_sms_count()
		return_string='Sent SMS Count: {0}\n'.format(sms_sent_count)
		self._logger.debug("sms_sent_count = %d",sms_sent_count)
		sms_received_count=sms_command.get_received_sms_count()
		return_string+='Received SMS Count: {0}\n'.format(sms_received_count)
		self._logger.debug("sms_received_count = %d",sms_received_count)
		voice_sent_count=voice_command.get_sent_calls_count()
		return_string+='Sent Voice Count: {0}\n'.format(voice_sent_count)
		self._logger.debug("voice_sent_count = %d",voice_sent_count)
		voice_received_count=voice_command.get_received_calls_count()
		return_string+='Received Voice Count: {0}\n'.format(voice_received_count)
		self._logger.debug("voice_received_count = %d",voice_received_count)
		recording_count=voice_command.get_recordings_count()
		return_string+='Recordings Count: {0}'.format(recording_count)
		all_zero= not sms_sent_count and not sms_received_count and not voice_sent_count and not voice_received_count and not recording_count
		return (all_zero,return_string)
	def pickle_twilio_state(self):
		self._logger.debug("entered pickle_twilio_state")
		twilio_state_dictionary=self.get_twilio_state_dictionary()
		file_handle=open(self.pickle_file_path,'wb')
		pickle.dump(twilio_state_dictionary,file_handle)
		file_handle.close()
	def get_twilio_state_changed(self):
		self._logger.debug("entered get_twilio_state_changed")
		twilio_new_state_dictionary=self.get_twilio_state_dictionary()
		twilio_old_state_dictionary=self.unpickle_twilio_state()
		return_value= not (twilio_new_state_dictionary==twilio_old_state_dictionary)
		self._logger.debug("return_value = %s",return_value)
		return return_value