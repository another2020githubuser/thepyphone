import logging
import re
import pjsua2 as pj
from gtkapplication.api.sip.pjsip_container_accessor import PjSipContainerAccessor
_logger=logging.getLogger(__name__)
SipUriRegex=re.compile('(sip|sips):([^:;>\@]*)@?([^:;>]*):?([^:;>]*)')
class SipUriParser:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
	def parseSipUri(self,sip_uri_str):
		self._logger.debug('entered parseSipUri')
		self._logger.debug("sip_uri_str = '%s'",sip_uri_str)
		m=SipUriRegex.search(sip_uri_str)
		if not m:
			raise ValueError("SipUriRegex.search failed on '{0}'".format(sip_uri_str))
		scheme=m.group(1)
		user=m.group(2)
		host=m.group(3)
		port=m.group(4)
		if host=='':
			host=user
			user=''
		return SipUri(scheme.lower(),user,host.lower(),port)
class SipUri:
	def __init__(self,scheme,user,host,port):
		self._logger=logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
		self._logger.debug('SipUri constructor')
		self._logger.debug('scheme.lower() = %s',scheme)
		self._logger.debug('user = %s',user)
		self._logger.debug('host.lower() = %s',host)
		self._logger.debug('port = %s',port)
		self.scheme=scheme
		self.user=user
		self.host=host
		self.port=port
	def __eq__(self,sip_uri):
		self._logger.debug('sip_uri = %s',str(sip_uri))
		if self.scheme==sip_uri.scheme and self.user==sip_uri.user and self.host==sip_uri.host:
			self._logger.debug("__eq__ returning True")
			return True
		else:
			self._logger.debug("__eq__ returning False")
			return False
	def __cmp__(self,sip_uri):
		raise NotImplementedError("__cmp__ removed in Python 3")
	def __str__(self):
		s=self.scheme+':'
		if self.user:s+=self.user+'@'
		s+=self.host
		if self.port:s+=':'+self.port
		self._logger.debug('__str__ returning = %s',s)
		return s
	def __repr__(self):
		return_value="scheme='{0}', user='{1}', host='{2}', port='{3}'".format(self.scheme,self.user,self.host,self.port)
		self._logger.debug("__repr__ returning =%s",return_value)
class UriValidator:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
	def validateUri(self,uri):
		self._logger.debug("enter validateUri")
		pjsip_accessor=PjSipContainerAccessor()
		instance=pjsip_accessor.get_pjsip_endpoint()
		validation_result=instance.utilVerifyUri(uri)
		success=validation_result==pj.PJ_SUCCESS
		self._logger.debug('success = %s',success)
		return success
	def validateSipUri(self,uri):
		self._logger.debug('enter validateSipUri')
		pjsip_accessor=PjSipContainerAccessor()
		instance=pjsip_accessor.get_pjsip_endpoint()
		validation_result=instance.utilVerifySipUri(uri)
		self._logger.debug('validation_result = %s',validation_result)
		success=validation_result==pj.PJ_SUCCESS
		self._logger.debug('success = %s',success)
		return success