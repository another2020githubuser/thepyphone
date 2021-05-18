import logging
from timeit import default_timer
from datetime import timedelta
import gtkapplication.ui.gtk.gtk_builder
import gtkapplication.logging_config
import gtkapplication.ui.gtk.gtk_css
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gdk,GLib
_logger=gtkapplication.logging_config.Config().initialize_logging()
_logger.debug('logging initialized')
class SplashGlade(Gtk.Window):
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
		self._logger.debug('logging initialized')
		glade_file_name="splash_screen_with_progress_bar.glade"
		gtk_builder=gtkapplication.ui.gtk.gtk_builder.GtkBuilder(__file__,glade_file_name)
		gtk_builder.connect_signals(self)
		self.progress_bar=gtk_builder.get_object('main_progressbar')
		self.window=gtk_builder.get_object('progressbar_window')
		self.start_time=default_timer()
		css_file="splash_screen_with_progress_bar.css"
		css_parser=gtkapplication.ui.gtk.gtk_css.GtkCss()
		css_parser.load_and_apply_css(__file__,css_file)
	def showme(self,timeout):
		GLib.idle_add(self.update_progress_bar,timeout)
		self.window.show_all()
		self.window.maximize()
	def update_progress_bar(self,timeout):
		self._logger.debug("entered update_progress_bar, timeout is %s",timeout)
		current_seconds=int(timedelta(seconds=default_timer()-self.start_time).total_seconds())
		displayed_seconds=int(self.progress_bar.get_fraction()*timeout)
		self._logger.debug("current_seconds = %s, displayed_seconds = %s",current_seconds,displayed_seconds)
		if current_seconds!=displayed_seconds:
			self._logger.debug("current_seconds = %s",current_seconds)
			self.progress_bar.set_text("{0} seconds elapsed out of {1} seconds allowed".format(int(current_seconds),timeout))
		if current_seconds>timeout:
			Gtk.main_quit()
		self.progress_bar.set_fraction(current_seconds/timeout)
		return True
def splash_screen():
	win=SplashGlade()
	win.showme(100)
	Gtk.main()
splash_screen()