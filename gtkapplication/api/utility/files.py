import datetime
import uuid
import logging
import requests
_logger=logging.getLogger(__name__)
def create_unique_file_name(file_extension):
	_logger.debug('entered _create_unique_file_name')
	_logger.debug('file_extension = %s',file_extension)
	assert file_extension[0]=="."
	formatted_now=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
	unique_file_name="{0}-{1}{2}".format(formatted_now,str(uuid.uuid4()),file_extension)
	_logger.debug('unique_file_name = %s',unique_file_name)
	return unique_file_name
def download_and_save_uri(target_uri,selected_file_name):
	_logger.debug('entered download_and_save_uri')
	http_request=requests.get(target_uri)
	assert http_request.status_code!=404
	_logger.debug('http_request.status_code = %s',http_request.status_code)
	download_content=http_request.content
	_logger.debug('len(download_content) = %s',len(download_content))
	file_writer=open(selected_file_name,"wb")
	file_writer.write(download_content)
	file_writer.close()
	_logger.debug('file save successful')