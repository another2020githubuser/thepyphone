import logging
import datetime
from functools import total_ordering
from tzlocal import get_localzone
import pytz
import gtkapplication.api.twilio.twilio_date_converter
@total_ordering
class RecordingDto:
	def __init__(self,date_created,from_phone_number,recording_duration,recording_sid,recording_url,file_name):
		self._logger=logging.getLogger(__name__)
		assert isinstance(date_created,datetime.datetime),"{0} is not a datetime, but type {1}".format(date_created,type(date_created))
		assert date_created.tzinfo is None
		self._date_created=date_created
		self._from_phone_number=from_phone_number
		assert isinstance(recording_duration,int)
		self._recording_duration=recording_duration
		self._recording_sid=recording_sid
		self._recording_url=recording_url
		self._file_name=file_name
	def __eq__(self,other):
		return self.date_created_utc==other.date_created_utc
	def __ne__(self,other):
		return not (self==other)
	def __lt__(self,other):
		return self.date_created_utc<other.date_created_utc
	def __str__(self):
		return "date_created = {0}, from_phone_number = {1}, recording_duration = {2}, recording_sid = {3}, file_name = {4}, recording_url = {5}".format(self._date_created,self._from_phone_number,self._recording_duration,self._recording_sid,self._file_name,self._recording_url)
	@property
	def date_created_utc(self):
		return self._date_created
	@property
	def date_created_localtime(self):
		local_tz=get_localzone()
		local_dt=self._date_created.replace(tzinfo=pytz.utc).astimezone(local_tz)
		self._logger.debug("local_dt = %s",local_dt)
		return local_dt
	@property
	def from_phone_number(self):
		return self._from_phone_number
	@property
	def recording_duration(self):
		return self._recording_duration
	@property
	def recording_sid(self):
		return self._recording_sid
	@property
	def recording_url(self):
		return self._recording_url
	@property
	def file_name(self):
		if self._file_name is None:
			raise ValueError("File Name not yet set")
		else:
			return self._file_name