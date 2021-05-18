import logging
import uuid
import os.path
import gtkapplication.ui.gtk.gtk_image_resize
import gtkapplication.ui.contacts.contact_list_ui
import gtkapplication.api.twilio.sms_command
class MmsSignalHandler:
	def __init__(self,image_bytes,content_type,file_extension):
		self._logger=logging.getLogger(__name__)
		self._image_bytes=image_bytes
		self._content_type=content_type
		self._file_extension=file_extension
		self._scaled_to_width=True
	def on_mms_image_button_release_event(self,image,user_data):
		self._logger.debug("entered on_mms_image_button_release_event")
		self._logger.debug("self._scaled_to_width = %s",self._scaled_to_width)
		gtk_image_resizer=gtkapplication.ui.gtk.gtk_image_resize.GtkImageResize()
		target_resolution=os.environ["TARGET_MONITOR_RESOLUTION"]
		if self._scaled_to_width:
			self._logger.debug("scaling to height")
			if target_resolution=="800x480":
				pixbuf=gtk_image_resizer.scale_to_height(self._image_bytes,375)
			elif target_resolution=="1366x768":
				pixbuf=gtk_image_resizer.scale_to_height(self._image_bytes,600)
			else:
				raise ValueError("{0} is an unsupported screen resoultion".format(target_resolution))
		else:
			self._logger.debug("scaling to width")
			if target_resolution=="800x480":
				pixbuf=gtk_image_resizer.scale_to_width(self._image_bytes,700)
			elif target_resolution=="1366x768":
				pixbuf=gtk_image_resizer.scale_to_width(self._image_bytes,1200)
			else:
				raise ValueError("{0} is an unsupported screen resoultion".format(target_resolution))
		image.set_from_pixbuf(pixbuf)
		image.show_all()
		self._scaled_to_width= not self._scaled_to_width
		self._logger.debug("after scaling, self._scaled_to_width = %s",self._scaled_to_width)
	def on_forward_image_toolbutton_clicked(self,image):
		self._logger.debug("entered on_forward_image_toolbutton_clicked")
		contacts_list_ui=gtkapplication.ui.contacts.contact_list_ui.ContactList(self.on_forward_button_clicked_handler)
		contacts_list_ui.showme()
	def on_forward_button_clicked_handler(self,contact_point_list):
		self._logger.debug("entered on_forward_button_clicked_handler")
		self._logger.debug("got %d contact points",len(contact_point_list))
		temp_file_name="/tmp/pyphone-forwarded-sms-{0}{1}".format(uuid.uuid4(),self._file_extension)
		self._logger.debug("temp_file_name = %s",temp_file_name)
		if os.path.exists(temp_file_name):
			self._logger.warning("temp file already exists: %s",temp_file_name)
		else:
			self._logger.debug("writing file %s with length %d",temp_file_name,len(self._image_bytes))
			fp=open(temp_file_name,'wb')
			fp.write(self._image_bytes)
			fp.close()
			self._logger.debug("after fp.close()")
			sms_command=gtkapplication.api.twilio.sms_command.SmsCommand()
			from_phone_number=gtkapplication.data.config_data.PROFILE_DATA['my_phone_number']
			for contact_point in contact_point_list:
				self._logger.debug("forwarding mms to %s",contact_point)
				sms_command.send(from_phone_number,contact_point.uri_string,"Forwarded Message",temp_file_name)