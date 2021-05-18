import logging
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gdk
class GtkScreen:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def center_window(self,gtk_window):
		display=Gdk.Display.get_default()
		monitor_count=display.get_n_monitors()
		assert monitor_count==1
		monitor=display.get_monitor(0)
		monitor_geometry=monitor.get_geometry()
		self._logger.debug("monitor width is %s, height is %s",monitor_geometry.width,monitor_geometry.height)
		window_geometry=gtk_window.get_size()
		self._logger.debug("monitor width is %s, height is %s",window_geometry.width,window_geometry.height)
		x=(monitor_geometry.width-window_geometry.width)/2
		y=(monitor_geometry.height-window_geometry.height)/2
		self._logger.debug("x = %s, y = %s",x,y)
		gtk_window.move(x,y)