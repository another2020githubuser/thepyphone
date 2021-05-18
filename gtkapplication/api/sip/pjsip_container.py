import logging
class PjSipContainer:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._logger.debug("PjSipContainer constructor")
		self.ep=None
		self.sip_account_list=[]
		self.pjsip_log_writer=None
		self.tone_generator=None
sip_container=None
if sip_container is None:
	sip_container=PjSipContainer()
else:
	raise ValueError("Cannot reinitiailze sip_container")