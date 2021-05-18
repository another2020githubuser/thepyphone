import gtkapplication.logging_config
_logger=gtkapplication.logging_config.Config().initialize_logging()
_logger.debug('logging initialized')
from gtkapplication.ui.gtk.gtk_application import GtkApplication
import gtkapplication.ui.gtk.window_state_accessor
import gtkapplication.data
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gio
GTK_APPLICATION_NAME="pi-client.thepyphone.com"
def main():
	_logger.debug("entering main")
	gtk_application=GtkApplication(GTK_APPLICATION_NAME,Gio.ApplicationFlags.FLAGS_NONE)
	_logger.debug("created gtk_application")
	gtk_application.run()
	_logger.debug("after gtk_application.run()")
if __name__=="__main__":
	_logger.debug("before main()")
	main()
	_logger.debug("after main()")