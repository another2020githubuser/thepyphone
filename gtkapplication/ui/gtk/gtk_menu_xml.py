import logging
import os.path
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class GtmMenuButtonXmlParser:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def load_menu_button_actions_xml(self,menu_xml_file_path,gtk_builder):
		self._logger.debug("entered _load_menu_button")
		assert os.path.exists(menu_xml_file_path)
		with open(menu_xml_file_path,'r')as fhandle:
			menu_xml=fhandle.read()
		gtk_builder.add_from_string(menu_xml)
		self._logger.debug("menu xml read")
		appmenu=gtk_builder.get_object("appmenu")
		menu_button=gtk_builder.get_object("menu_button")
		assert isinstance(menu_button,Gtk.MenuButton)
		menu_button.set_menu_model(appmenu)
		self._logger.debug("after set_menu_model")