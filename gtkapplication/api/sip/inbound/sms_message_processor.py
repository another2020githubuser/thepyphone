import logging
import re
import datetime
import mimetypes
import requests
import gtkapplication.api.contacts.contact_manager
from gtkapplication.ui.sms import SmsDirection
import gtkapplication.api.sip.business_layer
import gtkapplication.api.audio.ringer
import gtkapplication.ui.gtk.window_manager
import gtkapplication.api.contacts
class InboundProcessor:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def process_sms_message(self,message_body):
		self._logger.debug("entered process_sms_message")
		message_lines=message_body.split('\n')
		message_first_line=message_lines[0]
		message_body='\n'.join(message_lines[1:])
		from_phone_number=message_first_line.split('=')[1]
		self._logger.debug('from_phone_number = %s',from_phone_number)
		(message_stripped_of_links,links)=self._extract_links(message_body)
		message_body=message_stripped_of_links.strip()
		self._logger.debug("message_body after strip() = '%s'",message_body)
		db=gtkapplication.api.sip.business_layer.BusinessLayer()
		sms_message_row_id=db.insert_sms_message(from_phone_number,message_body,SmsDirection.RECEIVED)
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		(contact,active_contact_point_index)=contact_manager.find_contact_by_phone_number(from_phone_number,True)
		window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		sms_window=window_manager.get_sms_window(contact,active_contact_point_index,True)
		dashboard_ui=window_manager.get_dashboard_window(True)
		if message_body!="":
			self._logger.debug("display_sms with message body %s",message_body)
			sms_window.display_sms(message_body,SmsDirection.RECEIVED,datetime.datetime.now())
		if len(links)>0:
			for link in links:
				self._logger.debug("processing link %s",link)
				content_type=self._get_content_type(link)
				file_extension=mimetypes.guess_extension(content_type)
				self._logger.debug("link has content_type %s",content_type)
				self._logger.debug("link has extension %s",file_extension)
				db.insert_mms_link(sms_message_row_id,link,content_type)
				if content_type in ['image/jpeg','image/gif','image/png']:
					self._logger.debug("auto displaying picture")
					sms_window.display_mms(link,SmsDirection.RECEIVED,datetime.datetime.now(),content_type,file_extension)
				else:
					self._logger.debug("not a supported picture, not auto displaying link.  Content type: '%s', link: '%s'",content_type,link)
					sms_window.display_sms("Content Type : "+content_type+"\n"+link,SmsDirection.RECEIVED,datetime.datetime.now())
		sms_dto=gtkapplication.ui.sms.SmsDto(datetime.datetime.now(),contact,message_body,links,active_contact_point_index)
		dashboard_ui.add_new_sms_notification(sms_dto)
		gtkapplication.api.audio.ringer.start_ringer()
	def _extract_links(self,message_body):
		self._logger.debug('entered extract_links')
		self._logger.debug("looking for links in message body '%s'",message_body)
		re_pattern=r"(https://api.twilio.com/.*?)\n"
		links=re.findall(re_pattern,message_body)
		self._logger.debug('found %d links',len(links))
		message_stripped_of_links=re.sub(re_pattern,'',message_body)
		self._logger.debug('removed links from message body')
		return (message_stripped_of_links,links)
	def _get_content_type(self,link):
		self._logger.debug("entered _get_content_type, link is '%s'",link)
		response=requests.head(link,allow_redirects=True)
		assert response is not None
		self._logger.debug("response.status_code=%s",response.status_code)
		assert response.status_code==200
		content_type=response.headers['Content-Type']
		self._logger.debug("content_type = %s",content_type)
		return content_type