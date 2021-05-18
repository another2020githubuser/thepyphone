import logging
import subprocess
import os.path
import datetime
import uuid
import requests
class Downloader:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def download_voicemail(self,recording_link,phone_number):
		self._logger.debug('entered download_voicemail')
		folder="voicemail"
		abs_folder=os.path.abspath(folder)
		self._logger.debug("abs_folder = %s",abs_folder)
		assert os.path.exists(folder)
		formatted_now=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
		file_name="from-phone-number-{0}-{1}-{2}.{3}".format(phone_number,formatted_now,str(uuid.uuid4()),"wav")
		response=requests.get(recording_link)
		if response.status_code==200:
			voicemail_path=os.path.abspath(os.path.join(folder,file_name))
			assert not os.path.exists(voicemail_path)
			fp=open(voicemail_path,'wb')
			fp.write(response.content)
			fp.close()
			return voicemail_path
		else:
			self._logger.warning("Download of '%s' returned http status code %s",recording_link,response.status_code)
			self._logger.warning("response.content = %s",response.content)
			return None