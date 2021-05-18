import logging
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gdk,GLib,Gio,GdkPixbuf
class GtkStyle:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def verify_style_class(self,widget,style_class_name):
		self._logger.debug('entered verify_style_class, widget class = %s',type(widget).__name__)
		assert isinstance(widget,(Gtk.Frame,Gtk.Image,Gtk.Label,Gtk.MenuBar,Gtk.Box,Gtk.Entry))
		style_context=widget.get_style_context()
		style_classes=style_context.list_classes()
		self._logger.debug('style_classes = %s',style_classes)
		assert len(style_classes)==1
		assert style_classes[0]==style_class_name
	def list_style_classes(self,widget):
		self._logger.debug('entered list_style_classes, widget class = %s',type(widget).__name__)
		style_context=widget.get_style_context()
		style_classes=style_context.list_classes()
		self._logger.debug('style_classes = %s',style_classes)