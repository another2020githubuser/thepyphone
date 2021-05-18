import logging
import gtkapplication.ui.gtk.gtk_builder
import gtkapplication.api.sip.pjsip_container_accessor
import gtkapplication.api.contacts.contact_manager
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gio
class DiagnosticsUi:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		glade_file_name="diagnostics_ui.glade"
		self._gtk_builder=gtkapplication.ui.gtk.gtk_builder.GtkBuilder(__file__,glade_file_name)
		css_file="diagnostics_ui.css"
		css_parser=gtkapplication.ui.gtk.gtk_css.GtkCss()
		css_parser.load_and_apply_css(__file__,css_file)
		self.gtk_application_window=self._gtk_builder.get_object('diagnostics_window')
		self.gtk_application_window.connect("delete-event",self._onclose)
		self._logger.debug('got window')
	def showme(self):
		self._logger.debug('enter showme')
		accessor=gtkapplication.api.sip.pjsip_container_accessor.PjSipContainerAccessor()
		row=1
		grid=self._gtk_builder.get_object("grid")
		accounts=accessor.get_accounts()
		for account in accounts:
			buddy_info=account.last_reg_stats
			event_type_label=Gtk.Label("Registration (OnRegState)")
			from_uri_label=Gtk.Label("{0} --> {1}".format(account.uri,account.account_config.regConfig.registrarUri))
			data_text_label=Gtk.Label(buddy_info)
			grid.attach(event_type_label,0,row,1,1)
			grid.attach(from_uri_label,1,row,1,1)
			grid.attach(data_text_label,2,row,1,1)
			row+=1
			self.set_style_class([event_type_label,from_uri_label,data_text_label])
		for account in accounts:
			data_dict=account.incoming_subscribe_data
			for from_uri,data_text in data_dict.items():
				event_type_label=Gtk.Label("Presence (OnIncomingSubscribe)")
				from_uri_label=Gtk.Label("{0} --> {1}".format(data_text.fromUri,account.uri))
				data_text_label=Gtk.Label("id = {0} {1} {2}\nlast_updated:{3}".format(data_text.account_id,data_text.code,data_text.reason,data_text.last_updated))
				grid.attach(event_type_label,0,row,1,1)
				grid.attach(from_uri_label,1,row,1,1)
				grid.attach(data_text_label,2,row,1,1)
				row+=1
				self.set_style_class([event_type_label,from_uri_label,data_text_label])
		for account in accounts:
			if account.server_buddy is None:
				self._logger.debug("No server buddy for account %r",account)
			else:
				buddy_info=account.server_buddy.latest_buddy_get_info
				event_type_label=Gtk.Label("Presence (OnBuddyState)")
				from_uri_label=Gtk.Label("{0} --> {1}".format(account.uri,buddy_info.uri))
				buddy_info_text="id = {0} {1} ({2} {3})\nLast Updated: {4}".format(account.getId(),buddy_info.subStateName,buddy_info.subTermCode,buddy_info.subTermReason,buddy_info.last_updated)
				data_text_label=Gtk.Label(buddy_info_text)
				grid.attach(event_type_label,0,row,1,1)
				grid.attach(from_uri_label,1,row,1,1)
				grid.attach(data_text_label,2,row,1,1)
				row+=1
				self.set_style_class([event_type_label,from_uri_label,data_text_label])
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		buddy_contact_list=contact_manager.get_free_buddy_contacts()
		for buddy_contact in buddy_contact_list:
			contact,contact_point_uri_string=buddy_contact
			event_type_label=Gtk.Label("Presence (OnBuddyState)")
			from_uri_label=Gtk.Label("{0} --> {1}".format(contact_point_uri_string,contact.buddy.account.uri))
			buddy_info=contact.buddy.latest_buddy_get_info
			buddy_info_text="id = {0} {1} ({2} {3})\nLast Updated: {4}".format(contact.buddy.account.getId(),buddy_info.subStateName,buddy_info.subTermCode,buddy_info.subTermReason,buddy_info.last_updated)
			data_text_label=Gtk.Label(buddy_info_text)
			grid.attach(event_type_label,0,row,1,1)
			grid.attach(from_uri_label,1,row,1,1)
			grid.attach(data_text_label,2,row,1,1)
			row+=1
			self.set_style_class([event_type_label,from_uri_label,data_text_label])
		self.gtk_application_window.show_all()
		self._logger.debug('window shown')
		self._logger.debug("window size = %s",self.gtk_application_window.get_size())
		self._logger.debug('exit showme')
	def set_style_class(self,labels):
		for label in labels:
			label.get_style_context().add_class("diagnostics_grid_label_style_class")
	def _onclose(self,*args):
		self._logger.debug("entered onclose with %d args",len(args))
		self.gtk_application_window.destroy()