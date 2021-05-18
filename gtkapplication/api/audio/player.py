import wave
import datetime
import os.path
import logging
import uuid
import requests
import pyaudio
import gtkapplication.data
import gtkapplication.api.sip.pjsip_container
import gi
gi.require_version('Gtk','3.0')
from gi.repository import GObject
_logger=logging.getLogger(__name__)
def play_wav_file_non_blocking(wav_file_path):
	_logger.debug("entered play_wav_file_non_blocking")
	def pyaudio_stream_callback(in_data,frame_count,time_info,status):
		_logger.debug("in_data =%s, frame_count =%s, time_info =%s, status =%s",in_data,frame_count,time_info,status)
		data=wav_file.readframes(frame_count)
		_logger.debug("data length = %d, status =%s",len(data),status)
		return (data,pyaudio.paContinue)
	def _gobject_delay():
		GObject.timeout_add(100,_gobject_delay)
	_logger.debug("after internal function definitions")
	py_audio=pyaudio.PyAudio()
	_logger.debug("created py_audio")
	assert os.path.exists(wav_file_path)
	_logger.debug("wav_file_path = '%s'",wav_file_path)
	wav_file=wave.open(wav_file_path,'rb')
	_logger.debug("before py_audio.open")
	pyaudio_stream=py_audio.open(format=py_audio.get_format_from_width(wav_file.getsampwidth()),channels=wav_file.getnchannels(),rate=wav_file.getframerate(),output=True,stream_callback=pyaudio_stream_callback)
	_logger.debug("after py_audio.open")
	pyaudio_stream.start_stream()
	_logger.debug("after start_stream()")
	while pyaudio_stream.is_active():
		_gobject_delay()
	_logger.debug("after stream.is_active()")
	pyaudio_stream.stop_stream()
	_logger.debug("after stop_stream()")
	pyaudio_stream.close()
	_logger.debug("after pyaudio_stream.close()")
	wav_file.close()
	_logger.debug("after wav_file.close()")
	py_audio.terminate()
	_logger.debug("after py_audio.terminate()")
def play_wav_file_blocking(wav_file_path):
	_logger.debug('entered play_wav_file')
	_logger.debug('wav_file_path = %s',wav_file_path)
	assert os.path.exists(wav_file_path)
	wav_file=wave.open(wav_file_path,"rb")
	_logger.debug('wav file opened')
	pyaudio_player=pyaudio.PyAudio()
	_logger.debug('pyaudio player created')
	stream=pyaudio_player.open(format=pyaudio_player.get_format_from_width(wav_file.getsampwidth()),channels=wav_file.getnchannels(),rate=wav_file.getframerate(),output=True)
	_logger.debug('stream opened')
	stream_chunk_size=1024
	_logger.debug('stream_chunk_size = %s',stream_chunk_size)
	data=wav_file.readframes(stream_chunk_size)
	_logger.debug('got 1st chunk')
	chunk_counter=0
	while data:
		stream.write(data)
		data=wav_file.readframes(stream_chunk_size)
		chunk_counter+=1
	_logger.debug('done playing, played %d chunks, cleaning up',chunk_counter)
	stream.stop_stream()
	stream.close()
	_logger.debug('stream closed')
	pyaudio_player.terminate()
	_logger.debug('after pyaudio terminate()')
	wav_file.close()
	_logger.debug('after wav_file.close()')
def play_url(url):
	_logger.debug('entered play_url')
	_logger.debug('url = %s',url)
	unique_file_name=_download_and_save_url(url)
	_logger.debug('unique_file_name = %s',unique_file_name)
	play_wav_file_blocking(unique_file_name)
	_logger.debug('after _play_wav_file')
	os.remove(unique_file_name)
	_logger.debug('removed file %s',unique_file_name)
def _download_and_save_url(url):
	_logger.debug('entered download_and_save_url')
	_logger.debug('url = %s',url)
	http_request=requests.get(url)
	assert http_request.status_code!=404
	download_content=http_request.content
	_logger.debug('len(download_content) = %s',len(download_content))
	unique_file_name=create_unique_file_name("wav")
	_logger.debug('unique_file_name = %s',unique_file_name)
	full_path=os.path.join(os.path.dirname(__file__),unique_file_name)
	_logger.debug('full_path = %s',full_path)
	file_writer=open(full_path,"wb")
	file_writer.write(download_content)
	file_writer.close()
	return full_path
def create_unique_file_name(file_extension):
	_logger.debug('entered create_unique_file_name')
	_logger.debug('file_extension = %s',file_extension)
	formatted_now=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
	unique_file_name="{0}-{1}.{2}".format(formatted_now,str(uuid.uuid4()),file_extension)
	_logger.debug('unique_file_name = %s',unique_file_name)
	return unique_file_name