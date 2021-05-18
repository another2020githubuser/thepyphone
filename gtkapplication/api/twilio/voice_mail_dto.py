class VoiceMailDto:
	def __init__(self,date_created_local_time,recording_duration,recording_uri,recording_sid):
		self._date_created_local_time=date_created_local_time
		self._recording_sid=recording_sid
		self._recording_uri=recording_uri
		self._recording_duration=recording_duration
	@property
	def date_created_local_time(self):
		return self._date_created_local_time
	@property
	def recording_uri(self):
		return self._recording_uri
	@property
	def recording_sid(self):
		return self._recording_sid
	@property
	def recording_duration(self):
		return self._recording_duration
	def __getitem__(self,key):
		if key==0:
			return self._date_created_local_time
		elif key==1:
			return self._recording_duration
		elif key==2:
			return self._recording_uri
		elif key==3:
			return self._recording_sid
		else:
			raise ValueError("Invalid index for slice: {0}".format(key))
	def __repr__(self):
		return "date: {0}, duration: {1}, uri: {2}, sid: {3}".format(self._date_created_local_time,self._recording_duration,self._recording_uri,self._recording_sid)