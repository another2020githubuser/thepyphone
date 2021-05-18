import logging
import gtkapplication.api.sip.pjsip_container
class PjSipContainerAccessor:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def get_accounts(self):
		self._logger.debug("entered get_accounts")
		assert gtkapplication.api.sip.pjsip_container.sip_container is not None
		assert len(gtkapplication.api.sip.pjsip_container.sip_container.sip_account_list)==2
		return gtkapplication.api.sip.pjsip_container.sip_container.sip_account_list
	def get_account_by_name(self,account_name):
		self._logger.debug('entered get_account_by_name')
		self._logger.debug('account_name = %s',account_name)
		assert gtkapplication.api.sip.pjsip_container.sip_container is not None
		assert len(gtkapplication.api.sip.pjsip_container.sip_container.sip_account_list)==2
		account_name=account_name.lower()
		assert account_name in ["sip","twilio"]
		if account_name=="sip":
			return gtkapplication.api.sip.pjsip_container.sip_container.sip_account_list[gtkapplication.api.sip.SIP_ACCOUNT_INDEXES.SIP]
		elif account_name=="twilio":
			return gtkapplication.api.sip.pjsip_container.sip_container.sip_account_list[gtkapplication.api.sip.SIP_ACCOUNT_INDEXES.TWILIO]
		else:
			raise ValueError("Invalid account name: {0}".format(account_name))
	def get_pjsip_endpoint(self):
		assert gtkapplication.api.sip.pjsip_container.sip_container is not None
		assert gtkapplication.api.sip.pjsip_container.sip_container.ep is not None
		pjsip_endpoint=gtkapplication.api.sip.pjsip_container.sip_container.ep
		assert pjsip_endpoint is not None
		return pjsip_endpoint