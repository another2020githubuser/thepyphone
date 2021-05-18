import logging
import gtkapplication.ui.gtk.gtk_builder
import gtkapplication.api.contacts.contact_manager
import gtkapplication.api.contacts
import gtkapplication.api.contacts.contact
import gtkapplication.ui.contacts.contact_point_signal_handler
import gtkapplication.ui.gtk.gtk_dialog
import gtkapplication.ui.gtk.gtk_css
import gtkapplication.ui.gtk.gtk_menu_xml
import gtkapplication.ui.gtk.jump_to_window
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class ContactsUi():
	def __init__(self,window_unique_key):
		self._logger=logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
		self._datetimeformatstring="%a %b %d, %I:%M %p"
		self._gtk_builder=gtkapplication.ui.gtk.gtk_builder.GtkBuilder(__file__,"contacts_ui.glade")
		self._gtk_builder.connect_signals(self)
		self._logger.debug("signals connected")
		self.gtk_application_window=self._gtk_builder.get_object('main_window')
		self.gtk_application_window.connect("delete-event",self._onclose)
		self._window_unique_key=window_unique_key
		jump_to_window=gtkapplication.ui.gtk.jump_to_window.JumpToWindowHelper(self._gtk_builder)
	def on_jump_menu_button_toggled(self,button):
		self._logger.debug("entered on_jump_menu_button_toggled, is_active = %s",button.get_active())
		if button.get_active():
			jump_to_window=gtkapplication.ui.gtk.jump_to_window.JumpToWindowHelper(self._gtk_builder)
			self._logger.debug("after jump_to_window()")
			button.show_all()
	def showme(self):
		self._logger.debug('enter showme')
		css_parser=gtkapplication.ui.gtk.gtk_css.GtkCss()
		css_file="contacts_ui.css"
		css_parser.load_and_apply_css(__file__,css_file)
		self.gtk_application_window.show_all()
		self._logger.debug('window shown')
		self._logger.debug("window size = %s",self.gtk_application_window.get_size())
		self._logger.debug('exit showme')
	def _onclose(self,*args):
		self._logger.debug("entered onclose with %d args",len(args))
		if self._window_unique_key is None:
			self._logger.debug('self._window_unique_key is None, skipping remove_window_from_cache')
			Gtk.main_quit()
		else:
			stateful_object_accessor=gtkapplication.ui.gtk.window_state_accessor.WindowStateAccessor()
			stateful_object_accessor.remove_window_from_cache(self._window_unique_key)
			self.gtk_application_window.destroy()
	def add_new_contact(self,contact):
		self._logger.debug("entered add_new_contact, contact is %s",contact)
		assert isinstance(contact,gtkapplication.api.contacts.contact.Contact)
		self._gtk_builder.add_from_file(__file__,'contact.glade')
		contact_frame=self._gtk_builder.get_object("contact_frame")
		contact_name_label=self._gtk_builder.get_object("contact_name_label")
		contact_name_label.set_text(contact.name)
		self._logger.debug("added contact %s",contact.name)
		contact_point_container=self._gtk_builder.get_object("contact_point_container")
		i=0
		for contact_point in contact.contact_points:
			self._logger.debug("adding contact point %s to contact %s",contact_point,contact)
			contact_point_item_box=self._add_new_contact_point_item(contact,i)
			contact_point_container.pack_start(contact_point_item_box,False,False,0)
			i+=1
		contact_flowbox=self._gtk_builder.get_object("contact_flowbox")
		contact_flowbox.add(contact_frame)
	def _add_new_contact_point_item(self,contact,active_contact_point_index):
		self._logger.debug("entered _add_new_contact_point_item, contact is %s, active_contact_point_index is %s",contact,active_contact_point_index)
		self._gtk_builder.add_from_file(__file__,'contact_point.glade')
		contact_point_item_box=self._gtk_builder.get_object("contact_point_box")
		contact_point_item_label=self._gtk_builder.get_object("contact_point_item_label")
		contact_point=contact.contact_points[active_contact_point_index]
		assert isinstance(contact_point,gtkapplication.api.contacts.contact_point.ContactPoint)
		label_text="{0}\n{1}".format(contact_point.description,contact_point.uri_string_national)
		contact_point_item_label.set_text(label_text)
		self._logger.debug("label_text = %s",label_text)
		if contact_point.point_type=="x-sip":
			sms_button=self._gtk_builder.get_object("sms_button")
			sms_button.set_label("Text")
			self._logger.debug("set free buddy text label for contact %s",contact.name)
		signal_handler=gtkapplication.ui.contacts.contact_point_signal_handler.ContactPointSignalHandler(contact,active_contact_point_index)
		self._gtk_builder.connect_signals(signal_handler)
		self._logger.debug("signal handler set")
		return contact_point_item_box