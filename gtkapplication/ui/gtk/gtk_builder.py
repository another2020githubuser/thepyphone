import logging
import os.path
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class GtkBuilder(Gtk.Builder):
	def __init__(self,file_name,glade_file_name):
		Gtk.Builder.__init__(self)
		self._logger=logging.getLogger(__name__)
		self._logger.debug("view_name = %s",self.get_view_name(file_name,glade_file_name))
		self.add_from_file(file_name,glade_file_name)
		self._logger.debug("glade file loaded")
		self._logger.setLevel(logging.INFO)
	def get_object(self,*args,**kwargs):
		assert len(args)==1
		self._logger.debug("looking for object %s",args[0])
		widget=super(GtkBuilder,self).get_object(*args,**kwargs)
		assert widget is not None,"Could not find object {0}".format(args[0])
		return widget
	def add_from_file(self,current_file,glade_file_name):
		self._logger.debug('entered add_from_file')
		view_name=self.get_view_name(current_file,glade_file_name)
		self._logger.debug("view_name is %s",view_name)
		assert os.path.exists(view_name),"Could not find view {0}".format(view_name)
		super(GtkBuilder,self).add_from_file(view_name)
	def get_view_name(self,current_file,glade_file_name):
		self._logger.debug("entered get_view_name")
		target_resolution=os.environ["TARGET_MONITOR_RESOLUTION"]
		self._logger.debug('target_resolution = %s',target_resolution)
		dirname=os.path.dirname(current_file)
		view_name=os.path.join(dirname,"view/{0}/{1}".format(target_resolution,glade_file_name))
		self._logger.debug('view_name = %s',view_name)
		return view_name