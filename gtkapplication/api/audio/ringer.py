import logging
import os.path
import gtkapplication.api.audio.audio_manager
import gtkapplication.data
_logger=logging.getLogger(__name__)
def start_ringer():
	_logger.debug("entered start_ringer")
	num_active_calls=len(gtkapplication.api.sip.sip_call_state.sip_calls)
	if num_active_calls==0:
		data_path=gtkapplication.data.get_data_folder_location()
		ringer_path=os.path.join(data_path,"ring.mp3")
		assert os.path.exists(ringer_path)
		audio_manager=gtkapplication.api.audio.audio_manager.AudioManager()
		audio_manager.play_audio(ringer_path)
	else:
		_logger.debug("Active voice call count %d, skipping ringer",num_active_calls)
def stop_ringer():
	_logger.debug("entered stop_ringer()")
	audio_manager=gtkapplication.api.audio.audio_manager.AudioManager()
	audio_manager.stop_play_audio()