import logging
from tzlocal import get_localzone
class RFC2822Converter:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def to_local(self,twilio_date_time):
		self._logger.debug("entered to_local")
		assert twilio_date_time.tzinfo is not None
		tz_local=get_localzone()
		date_created_local_time=twilio_date_time.astimezone(tz_local)
		self._logger.debug("date_created_local_time = %s",date_created_local_time)
		return date_created_local_time