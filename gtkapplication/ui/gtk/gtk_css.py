import logging
import os.path
import gtkapplication.ui.global_
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gdk
class GtkCss:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def load_global_css(self):
		self._logger.debug("entered load_global_css")
		global_css_path=gtkapplication.ui.global_.get_folder_location()+"/"
		self.load_and_apply_css(global_css_path,"global.css")
	def load_and_apply_css(self,file_name,css_file_path):
		self._logger.debug("entered _load_and_apply_css")
		self._logger.debug("css_file_path = %s",css_file_path)
		gtk_css_file_path=self.get_css_file_name(file_name,css_file_path)
		self._logger.debug('gtk_css_file_path = %s',gtk_css_file_path)
		self._read_and_load_css(gtk_css_file_path)
	def _read_and_load_css(self,gtk_css_file_path):
		self._logger.debug("entered _read_and_load_css")
		if os.path.exists(gtk_css_file_path):
			with open(gtk_css_file_path,'rb')as fhandle:
				css=fhandle.read()
			self._logger.debug("css file read from disk")
			css_provider=Gtk.CssProvider()
			css_provider.load_from_data(css)
			context=Gtk.StyleContext()
			screen=Gdk.Screen.get_default()
			context.add_provider_for_screen(screen,css_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
			self._logger.debug("css provider added")
		else:
			self._logger.warning("css file '%s' not found")
	def get_css_file_name(self,current_file,css_file_name):
		self._logger.debug("entered get_css_file_name")
		target_resolution=os.environ["TARGET_MONITOR_RESOLUTION"]
		self._logger.debug('target_resolution = %s',target_resolution)
		dirname=os.path.dirname(current_file)
		full_path=os.path.join(dirname,"view/{0}/{1}".format(target_resolution,css_file_name))
		self._logger.debug('full_path = %s',full_path)
		assert os.path.exists(full_path)
		return full_path