import logging
import datetime
import gtkapplication.api.signal.signal_state
import gtkapplication.ui.gtk.window_manager
import gtkapplication.api.contacts.contact_manager
import gtkapplication.api.contacts.contact
import gtkapplication.api.contacts.contact_point
import gtkapplication.data.config_data
_logger=logging.getLogger(__name__)
_logger.debug("entering signal_command")
def onSignalMessageReceived(timestamp,source,groupID,message,attachments):
	_logger.debug("entered onSignalMessageReceived")
	_logger.debug("Message '%s' received in group '%s'",message,gtkapplication.api.signal.signal_state.signal.getGroupName(groupID))
	_logger.debug("source = '%s', attachments = '%s', timestamp='%s'",source,attachments,timestamp)
	contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
	(from_contact,active_contact_point_index)=contact_manager.find_contact_by_phone_number(source)
	if from_contact is None:
		from_contact=gtkapplication.api.contacts.contact.Contact("Unknown")
		contact_point=gtkapplication.api.contacts.contact_point.ContactPoint("x-signal","Signal",source)
		from_contact.selected_contact_point=contact_point
		active_contact_point_index=0
	to_contact="me ({0})".format(gtkapplication.data.config_data.PROFILE_DATA['my_phone_number'])
	window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
	sms_window=window_manager.get_sms_window(from_contact,active_contact_point_index,False)
	formatted_message="Date/Time: {0}\nFrom: {1}.\nTo: {2}\nBody:{3}\n\n".format(datetime.datetime.now(),from_contact,to_contact,message)
	_logger.debug("formatted_message = %s",formatted_message)
	sms_window.append_message_to_conversation(formatted_message)
	links=[]
	for attachment in attachments:
		link="file:///"+attachment
		_logger.debug("created link %s",link)
		links.append(link)
	sms_window.add_link_buttons_to_ui(links)
	_logger.debug("added %d links to window",len(links))
def sendSignalTextMessage(text_message,phone_number,attachments=None):
	_logger.debug("entered sendSignalTextMessage, phone number is '%s'",phone_number)
	_logger.debug("text_message is '%s'",text_message)
	if attachments is None:
		attachments=[]
		_logger.debug("No attachments")
	else:
		_logger.debug("attachments = %s",attachments)
	gtkapplication.api.signal.signal_state.signal.sendMessage(text_message,attachments,[phone_number])