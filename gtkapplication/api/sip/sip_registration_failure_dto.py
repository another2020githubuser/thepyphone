import logging
class SipRegistrationFailureDto:
	def __init__(self,account_id,account_uri,status,reason,code):
		self._logger=logging.getLogger(__name__)
		self._account_id=account_id
		self._account_uri=account_uri
		self._status=status
		self._reason=reason
		self._code=code
	@property
	def account_id(self):
		return self._account_id
	@property
	def account_uri(self):
		return self._account_uri
	@property
	def status(self):
		return self._status
	@property
	def reason(self):
		return self._reason
	@property
	def code(self):
		return self._code
	def __str__(self):
		return_value="account_id = {0}\naccount_uri = {1}\nstatus = {2}, reason = {3}, code = {4}".format(self._account_id,self._account_uri,self._status,self._reason,self._code)
		self._logger.debug("return_value = %s",return_value)
		return return_value