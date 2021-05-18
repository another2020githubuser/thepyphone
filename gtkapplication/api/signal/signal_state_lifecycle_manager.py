import logging
from pydbus import SessionBus
import gtkapplication.api.signal.signal_state
import gtkapplication.api.signal.signal_command
class SignalStateLifecycleManager:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def startup(self):
		if gtkapplication.api.signal.signal_state.session_bus is None:
			self._logger.debug("creating session_bus")
			gtkapplication.api.signal.signal_state.session_bus=SessionBus()
			self._logger.debug("created session_bus")
		else:
			raise ValueError("session_bus initialized twice")
		if gtkapplication.api.signal.signal_state.signal is None:
			self._logger.debug("creating signal")
			gtkapplication.api.signal.signal_state.signal=gtkapplication.api.signal.signal_state.session_bus.get('org.asamk.Signal')
			self._logger.debug("created signal")
		else:
			raise ValueError("signal initialized twice")
		gtkapplication.api.signal.signal_state.signal.onMessageReceived=gtkapplication.api.signal.signal_command.onSignalMessageReceived
		self._logger.debug("set onMessageReceived")
	def shutdown(self):
		self._logger.debug("entered shutdown")
		if gtkapplication.api.signal.signal_state.signal is not None:
			gtkapplication.api.signal.signal_state.signal.onMessageReceived=None
			gtkapplication.api.signal.signal_state.signal=None
			gtkapplication.api.signal.signal_state.session_bus=None
			self._logger.debug("finished shutdown")
		else:
			self._logger.debug("gtkapplication.api.signal.signal_state.signal is None")