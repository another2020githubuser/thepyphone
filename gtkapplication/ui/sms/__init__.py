import datetime
import enum
import gtkapplication.api.contacts.contact
class SmsDirection(enum.IntEnum):
	SENT=1,
	RECEIVED=2
class SmsDto:
	def __init__(self,timestamp,contact,content,mms_links,active_contact_point_index):
		assert isinstance(timestamp,datetime.datetime)
		assert isinstance(contact,gtkapplication.api.contacts.contact.Contact)
		assert isinstance(content,str)
		assert isinstance(mms_links,list)
		assert isinstance(active_contact_point_index,int)
		self._timestamp=timestamp
		self._contact=contact
		self._content=content
		self._mms_links=mms_links
		self._active_contact_point_index=active_contact_point_index
	@property
	def timestamp(self):
		return self._timestamp
	@property
	def contact(self):
		return self._contact
	@property
	def content(self):
		return self._content
	@property
	def mms_links(self):
		return self._mms_links
	@property
	def active_contact_point_index(self):
		return self._active_contact_point_index