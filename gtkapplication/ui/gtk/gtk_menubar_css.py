import logging
import gtkapplication.ui.gtk.gtk_style
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class GtkMenuBarCss:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def apply_css(self,menu_bar):
		self._logger.debug('entered set_font')
		assert menu_bar is not None
		gtk_style=gtkapplication.ui.gtk.gtk_style.GtkStyle()
		gtk_style.verify_style_class(menu_bar,"menubar")
		css=b'''
            .menubar {
            font-family: FreeSans;
            font-weight: normal;
            font-size: 26px;
            padding: 10px 10px 10px 10px;
            }
        '''
		css_provider=Gtk.CssProvider()
		css_provider.load_from_data(css)
		style_context=menu_bar.get_style_context()
		class_list=style_context.list_classes()
		self._logger.debug("class_list = %s",class_list)
		assert len(class_list)==1
		assert class_list[0]=="menubar"
		style_context.add_provider(css_provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)