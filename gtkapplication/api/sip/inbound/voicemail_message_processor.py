import logging
import email.utils
import datetime
import gtkapplication.api.twilio.recording_command
import gtkapplication.api.contacts.contact_manager
import gtkapplication.api.voicemail.controller
import gtkapplication.api.audio.ringer
import gtkapplication.ui.gtk.window_manager
import gtkapplication.api.contacts
class InboundProcessor:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def process_voicemail_message(self,message_body):
		self._logger.debug("entered process_voicemail_message")
		message_lines=message_body.split('\n')
		message_body='\n'.join(message_lines[1:])
		assert len(message_lines)==6
		recording_sid=message_lines[1].split('=')[1]
		recording_url=message_lines[2].split('=')[1]
		from_phone_number=message_lines[3].split('=')[1]
		recording_duration=int(message_lines[4].split('=')[1])
		recording_start_time=message_lines[5].split('=')[1]
		date_created=email.utils.parsedate_to_datetime(recording_start_time)+datetime.timedelta(seconds=recording_duration)
		assert isinstance(date_created.tzinfo,datetime.timezone)
		assert date_created.tzinfo==datetime.timezone.utc
		date_created=date_created.replace(tzinfo=None)
		downloader=gtkapplication.api.audio.downloader.Downloader()
		file_name=downloader.download_voicemail(recording_url,from_phone_number)
		if file_name is None:
			self._logger.warning("voicemail download failed for %s",recording_url)
		recording_dto=gtkapplication.api.twilio.RecordingDto(date_created,from_phone_number,recording_duration,recording_sid,recording_url,file_name)
		self._logger.debug("recording_dto = %s",recording_dto)
		db=gtkapplication.api.voicemail.controller.VoicemailController()
		db.insert_voicemail(date_created,from_phone_number,recording_duration,recording_sid,recording_url,file_name)
		self._logger.debug("after db.insert_voicemail()")
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		dashboard_ui=window_manager.get_dashboard_window()
		self._logger.debug("after get_dashboard_window()")
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		(contact,active_contact_point_index)=contact_manager.find_contact_by_phone_number(from_phone_number,True)
		dashboard_ui.add_new_voicemail_notification(recording_dto,contact,active_contact_point_index)
		self._logger.debug("after add new voicemail notification")
		recording_command=gtkapplication.api.twilio.recording_command.RecordingCommand()
		delete_success=recording_command.delete_server_recording(recording_dto.recording_sid)
		assert delete_success,"Unable to delete recording with sid {0}".format(recording_dto.recording_sid)
		self._logger.debug("after recording_command.delete_recording, sid is %s",recording_dto.recording_sid)
		gtkapplication.api.audio.ringer.start_ringer()
		self._logger.debug("started ringer")