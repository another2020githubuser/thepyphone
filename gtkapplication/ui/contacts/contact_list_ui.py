import logging
import os.path
import collections
import gtkapplication.ui.gtk.gtk_builder
import gtkapplication.ui.gtk.gtk_css
import gtkapplication.api.contacts.contact_manager
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class ContactList:
	def __init__(self,on_forward_button_clicked_handler):
		self._logger=logging.getLogger(__name__)
		glade_file_name="contact_list_ui.glade"
		self._gtk_builder=gtkapplication.ui.gtk.gtk_builder.GtkBuilder(__file__,glade_file_name)
		self._gtk_builder.connect_signals(self)
		self._window=self._gtk_builder.get_object('contact_list_window')
		css_loader=gtkapplication.ui.gtk.gtk_css.GtkCss()
		css_file="contact_list_ui.css"
		css_loader.load_and_apply_css(__file__,css_file)
		self._row_context_list=[]
		self._on_forward_button_clicked_handler=on_forward_button_clicked_handler
	def showme(self):
		self._logger.debug("entered showme")
		listbox=self._gtk_builder.get_object('listbox')
		listbox.set_header_func(self._listbox_header_func)
		glade_file_name="contact_list_ui_contact_row_item.glade"
		contact_manager=gtkapplication.api.contacts.contact_manager.ContactManager()
		contact_point_list=contact_manager.find_contacts_with_cell_numbers()
		self._logger.debug("find_contacts_with_cell_numbers() returned %d entries",len(contact_point_list))
		RowContext=collections.namedtuple("RowContext",field_names='contact contact_point checkbutton')
		for contact,active_contact_point_index in contact_point_list:
			contact_point=contact.contact_points[active_contact_point_index]
			self._gtk_builder.add_from_file(__file__,glade_file_name)
			row_item_box=self._gtk_builder.get_object("row_item_box")
			contact_name_label=self._gtk_builder.get_object('contact_name_label')
			contact_name_label.set_text(contact.name)
			contact_phone_number_label=self._gtk_builder.get_object("contact_phone_number_label")
			contact_phone_number_label.set_text(contact_point.uri_string_national)
			checkbutton=self._gtk_builder.get_object("checkbutton")
			listbox_row=Gtk.ListBoxRow()
			listbox_row.add(row_item_box)
			listbox.add(listbox_row)
			row_context=RowContext(contact,contact_point,checkbutton)
			self._row_context_list.append(row_context)
		self._logger.debug("Created listbox with %d entries",len(contact_point_list))
		self._window.show_all()
		self._logger.debug("after window.show_all()")
	def _listbox_header_func(self,row,before_row):
		if row.get_index()==0:
			box=self._gtk_builder.get_object("header_box")
			row.set_header(box)
			box.show_all()
			self._logger.debug("header set")
	def on_forward_button_clicked(self,button):
		self._logger.debug("entered on_forward_button_clicked")
		contact_point_list=[]
		for row_context in self._row_context_list:
			(contact,contact_point,checkbutton)=row_context
			if checkbutton.get_active():
				self._logger.debug("active checkbutton, contact is %s, contact_point = %s",contact,contact_point)
				contact_point_list.append(contact_point)
		self._on_forward_button_clicked_handler(contact_point_list)
		self._window.destroy()
		self._logger.debug("after window.destroy()")