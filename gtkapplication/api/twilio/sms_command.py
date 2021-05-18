import logging
import datetime
import uuid
import os.path
import requests
import twilio.rest
import gtkapplication.data.config_data
class SmsCommand(object):
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self.twilio_account_sid=gtkapplication.data.config_data.PROFILE_DATA['twilio_account_sid']
		self.twilio_auth_token=gtkapplication.data.config_data.PROFILE_DATA['twilio_auth_token']
		self._logger.debug("twilio version is %s",twilio.__version__)
	def delete_message(self,message_sid):
		self._logger.debug("entered delete_message")
		self._logger.debug("message sid = %s",message_sid)
		twilio_rest_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		twilio_rest_client.messages(message_sid).delete()
	def delete_media(self,message_sid,media_sid):
		raise NotImplementedError()
	def get_message_by_sid(self,message_sid):
		self._logger.debug("entered get_message_by_sid")
		twilio_rest_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		message=twilio_rest_client.messages(message_sid).fetch()
		return message
	def get_undelivered_sms_count(self):
		twilio_rest_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		phone_number_from=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
		all_messages=twilio_rest_client.messages.list(from_=phone_number_from)
		message_success_final_states=['received','delivered']
		failed_messages=[message.sid for message in all_messages if message.status not in message_success_final_states]
		self._logger.debug('%d failed messages out of %d total messages',len(failed_messages),len(all_messages))
		return len(failed_messages)
	def get_sent_sms_count(self):
		self._logger.debug('entered get_sent_sms_count')
		twilio_rest_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		my_phone_number=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
		sent_messages=twilio_rest_client.messages.list(from_=my_phone_number)
		self._logger.debug('%d sent messages',len(sent_messages))
		return len(sent_messages)
	def get_received_sms_count(self):
		self._logger.debug('entered get_received_sms_count')
		twilio_rest_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		my_phone_number=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
		received_messages=twilio_rest_client.messages.list(to=my_phone_number)
		self._logger.debug('%d received messages',len(received_messages))
		return len(received_messages)
	def send(self,from_phone_number,to_phone_number,sms_body,local_file_name=None):
		self._logger.debug('enter send')
		self._logger.debug('from_phone_number = %s',from_phone_number)
		self._logger.debug('to_phone_number = %s',to_phone_number)
		self._logger.debug('sms_body = %s',sms_body)
		self._logger.debug('local_file_name = %s',local_file_name)
		media_url=None
		if local_file_name is not None:
			media_url=self._upload_image_and_return_url(local_file_name)
		self._logger.debug('media_url = %s',media_url)
		status_update_url=gtkapplication.data.config_data.PROFILE_DATA['sms_status_update_url']
		self._logger.debug("status_update_url = %s",status_update_url)
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		message=twilio_client.messages.create(body=sms_body,to=to_phone_number,from_=from_phone_number,media_url=media_url,status_callback=status_update_url)
		self._logger.debug('message_sid = %s',message.sid)
		self._logger.debug('SMS Sent')
		return (message.sid,media_url)
	def _upload_image_and_return_url(self,local_file_path):
		self._logger.debug("entered _upload_image")
		selected_file_extension=os.path.splitext(local_file_path)[1]
		self._logger.debug('selected_file_extension = %s',selected_file_extension)
		formatted_now=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
		remote_file_name="{0}-{1}{2}".format(formatted_now,str(uuid.uuid4()),selected_file_extension)
		self._logger.debug('remote_file_name = %s',remote_file_name)
		if os.path.exists(local_file_path):
			fp=open(local_file_path,'rb')
			image_data=fp.read()
			fp.close()
			files={remote_file_name:image_data,}
			username=os.environ['USERNAME']
			password=os.environ['PASSWORD']
			credentials={'username':username,'password':password}
			putimage_url=gtkapplication.data.config_data.PROFILE_DATA['putimage_url']
			self._logger.debug('putimage_url = %s',putimage_url)
			response=requests.post(putimage_url,files=files,data=credentials)
			if response.status_code==200:
				getimage_url=gtkapplication.data.config_data.PROFILE_DATA['getimage_url']
				twilio_url="{0}/{1}".format(getimage_url,remote_file_name)
				self._logger.debug("twilio_url = %s",twilio_url)
				return twilio_url
			else:
				self._logger.warning("put_image service returned http status %s",response.status_code)
				return None
		else:
			self._logger.error("local_file_path '%s' not found",local_file_path)
			return None
	def get_messages_from_today(self):
		self._logger.debug('entered get_messages_from_today')
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		todays_date=datetime.date.today()
		messages=twilio_client.messages.list(date_sent=todays_date,)
		return messages
	def receive_from(self,from_phone_number,to_phone_number):
		self._logger.debug('enter receive_from')
		self._logger.debug('from_phone_number = %s',from_phone_number)
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		sms_messages=twilio_client.api.v2010.accounts(sid=self.twilio_account_sid).messages.list(from_=from_phone_number,to=to_phone_number)
		message_count=len(sms_messages)
		self._logger.debug('found %d sms_messages',message_count)
		return sms_messages
	def receive_to(self,to_phone_number):
		self._logger.debug('enter receive_to')
		self._logger.debug('to_phone_number = %s',to_phone_number)
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		sms_messages=twilio_client.api.v2010.accounts(sid=self.twilio_account_sid).messages.list(to=to_phone_number)
		message_count=len(sms_messages)
		self._logger.debug('found %d sms_messages',message_count)
		return sms_messages
	def receive_conversation(self,phone_number_1,phone_number_2):
		sms_messages_1=self.receive_from(phone_number_1,phone_number_2)
		self._logger.debug('%d total sms messages from %s to %s',len(sms_messages_1),phone_number_1,phone_number_2)
		self._logger.debug('dir(sms_message) = %s',dir(sms_messages_1[0]))
		self._logger.debug('type(sms_message) = %s',type(sms_messages_1[0]))
		sms_messages=self.receive_from(phone_number_2,phone_number_1)
		self._logger.debug('%d total sms messages from %s to %s',len(sms_messages),phone_number_2,phone_number_1)
		sms_messages.extend(sms_messages_1)
		self._logger.debug('receive_conversation has %d total messages',len(sms_messages))
		sms_messages.sort(key=lambda x:x.date_created,reverse=True)
		return sms_messages
	def get_sent_messages(self,page_size=20):
		twilio_rest_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		phone_number_from=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
		sent_messages=twilio_rest_client.messages.list(from_=phone_number_from,page_size=page_size)
		return sent_messages
	def get_media_list_for_message(self,message_sid):
		twilio_client=twilio.rest.Client(self.twilio_account_sid,self.twilio_auth_token)
		media_list=twilio_client.api.v2010.messages(message_sid).media.list()
		return media_list
	def get_media_urls_for_message(self,message_sid):
		self._logger.debug('enter get_media_urls_for_message')
		media_list=self.get_media_list_for_message(message_sid)
		self._logger.debug('media list contains = %d items',len(media_list))
		media_urls=[]
		for media in media_list:
			media_uri="https://api.twilio.com/{0}".format(media.uri)
			media_url=media_uri.replace('.json','')
			self._logger.debug('media.sid = %s',media.sid)
			self._logger.debug('media_url = %s',media_url)
			media_urls.append(media_url)
		return media_urls