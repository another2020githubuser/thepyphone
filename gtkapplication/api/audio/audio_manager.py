import logging
import subprocess
import os.path
import gtkapplication.api.audio.audio_state
class AudioManager:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._logger.debug("logging initailized")
		self.stop_flag=False
	def stop_play_audio(self):
		self._logger.debug("entered stop_play_audio")
		self.stop_flag=True
		self._logger.debug("stop flag set")
	def play_audio(self,audio_path):
		self._logger.debug("entered play_audio")
		self._logger.debug("audio_path = %s",audio_path)
		assert os.path.exists(audio_path)
		mplayer_args=["mplayer",audio_path]
		result=subprocess.run(mplayer_args,check=True)