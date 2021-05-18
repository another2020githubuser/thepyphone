import logging
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,GLib,Gio,GdkPixbuf,Gdk
class GtkImageResize:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def scale_to_width(self,image_bytes,desired_width):
		self._logger.debug("entered scale_to_width")
		glib_bytes=GLib.Bytes(image_bytes)
		memory_stream=Gio.MemoryInputStream.new_from_bytes(glib_bytes)
		pixbuf=GdkPixbuf.Pixbuf.new_from_stream(memory_stream,None)
		width=pixbuf.get_width()
		height=pixbuf.get_height()
		self._logger.debug("original image width = %d, height = %d",width,height)
		if width>desired_width:
			self._logger.debug("image too wide.  width = %s, desired_width = %s",width,desired_width)
		rescale_factor=desired_width/width
		self._logger.debug("rescale_factor = %s",rescale_factor)
		width=width*rescale_factor
		height=height*rescale_factor
		self._logger.debug("after scaling, width = %s, height = %s",width,height)
		pixbuf=pixbuf.scale_simple(width,height,GdkPixbuf.InterpType.BILINEAR)
		return pixbuf
	def scale_to_height(self,image_bytes,desired_height):
		self._logger.debug("entered scale_to_height")
		glib_bytes=GLib.Bytes(image_bytes)
		memory_stream=Gio.MemoryInputStream.new_from_bytes(glib_bytes)
		pixbuf=GdkPixbuf.Pixbuf.new_from_stream(memory_stream,None)
		width=pixbuf.get_width()
		height=pixbuf.get_height()
		self._logger.debug("original image width = %d, height = %d",width,height)
		if height>desired_height:
			self._logger.debug("image too tall.  width = %s, desired_height = %s",width,desired_height)
		rescale_factor=desired_height/height
		self._logger.debug("rescale_factor = %s",rescale_factor)
		width=width*rescale_factor
		height=height*rescale_factor
		self._logger.debug("after scaling, width = %s, height = %s",width,height)
		pixbuf=pixbuf.scale_simple(width,height,GdkPixbuf.InterpType.BILINEAR)
		return pixbuf