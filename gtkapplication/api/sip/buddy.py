import logging
import datetime
import collections
import pjsua2 as pj
class Buddy(pj.Buddy):
	def __init__(self,sip_account):
		pj.Buddy.__init__(self)
		self._logger=logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
		self.sip_account=sip_account
		self._logger.debug("account = %r",self.sip_account)
		self._latest_buddy_get_info=None
		self._last_updated=None
	def __repr__(self):
		buddy_info=self.getInfo()
		return "uri: {0}, status: {1}, subStateName: {2}, subTermReason: {3}, account_id = {4}".format(buddy_info.uri,buddy_info.presStatus.statusText,buddy_info.subStateName,buddy_info.subStateName,self.sip_account.getId())
	def __str__(self):
		self._logger.debug("entered __str__")
		if self.isValid():
			buddy_info=self.getInfo()
			status_text=buddy_info.presStatus.statusText
			self._logger.debug("status_text = %s",status_text)
			self._logger.debug("buddy = %r",self)
			return status_text
		else:
			self._logger.debug("self.isValid() is false")
			return None
	@property
	def account(self):
		return self.sip_account
	@property
	def latest_buddy_get_info(self):
		return self._latest_buddy_get_info
	@property
	def last_updated(self):
		return self._last_updated
	@property
	def uri(self):
		if self.isValid():
			buddy_info=self.getInfo()
			return buddy_info.uri
		else:
			self._logger.debug("self.isValid() is false")
			return None
	def status_text(self):
		buddy_info=self.getInfo()
		self._logger.debug('bi.subStateName = %s',buddy_info.subStateName)
		self._logger.debug('bi.uri = %s',buddy_info.uri)
		self._logger.debug('bi.subTermReason = %s',buddy_info.subTermReason)
		status="{0} ({1})".format(buddy_info.subStateName,buddy_info.subTermReason)
		if buddy_info.subState==pj.PJSIP_EVSUB_STATE_ACTIVE:
			if buddy_info.presStatus.status==pj.PJSUA_BUDDY_STATUS_ONLINE:
				status=buddy_info.presStatus.statusText
				if not status:
					status='Online'
			elif buddy_info.presStatus.status==pj.PJSUA_BUDDY_STATUS_OFFLINE:
				status='Offline'
			else:
				status='Unknown'
		return status
	def onBuddyState(self):
		self._logger.debug("enter onBuddyState")
		buddy_info=self.getInfo()
		self._logger.debug('bi.subStateName = %s',buddy_info.subStateName)
		self._logger.debug('bi.uri = %s',buddy_info.uri)
		self._logger.debug('bi.subTermReason = %s',buddy_info.subTermReason)
		self._logger.debug("Buddy %s has status %s",buddy_info.uri,buddy_info.presStatus.statusText)
		LatestBuddyInfoNamedTuple=collections.namedtuple("LatestBuddyInfoNamedTuple",field_names="uri contact presMonitorEnabled subState subStateName subTermCode subTermReason last_updated")
		latest_buddy_info=LatestBuddyInfoNamedTuple(buddy_info.uri,buddy_info.contact,buddy_info.presMonitorEnabled,buddy_info.subState,buddy_info.subStateName,buddy_info.subTermCode,buddy_info.subTermReason,datetime.datetime.now())
		self._latest_buddy_get_info=latest_buddy_info