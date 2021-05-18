import logging
import os.path
import gtkapplication.api.utility.files
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class CommonDialogs:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def show_info_dialog(self,main_text,secondary_text,parent=None,title=None):
		self._logger.debug("entered show_info_dialog")
		dialog_main_text=main_text
		dialog_secondary_text=secondary_text
		flags=0
		parent_window=parent
		dialog=Gtk.MessageDialog(parent_window,flags,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,dialog_main_text)
		if title is not None:
			self._logger.debug("setting title to %s",title)
			dialog.set_title(title)
		dialog.format_secondary_text(dialog_secondary_text)
		dialog.run()
		dialog.destroy()
	def show_ok_cancel_dialog(self,title,main_text,secondary_text,parent=None):
		self._logger.debug("entered show_ok_cancel_dialog")
		dialog_main_text=main_text
		dialog_secondary_text=secondary_text
		flags=0
		parent_window=parent
		dialog=Gtk.MessageDialog(parent_window,flags,Gtk.MessageType.QUESTION,Gtk.ButtonsType.OK_CANCEL,dialog_main_text,title=title)
		dialog.format_secondary_text(dialog_secondary_text)
		response=dialog.run()
		dialog.destroy()
		self._logger.debug("show_ok_cancel_dialog returning %s",response)
		assert response in [Gtk.ResponseType.OK,Gtk.ResponseType.CANCEL]
		return response
	def show_file_save_dialog(self,target_uri,default_path,file_extension,parent):
		default_file_name=gtkapplication.api.utility.files.create_unique_file_name(file_extension)
		self._logger.debug('default_file_name = %s',default_file_name)
		dialog=Gtk.FileChooserDialog("Save File",parent,Gtk.FileChooserAction.SAVE,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_SAVE,Gtk.ResponseType.OK))
		default_path=os.path.expanduser(default_path)
		self._logger.debug('default_path = %s',default_path)
		Gtk.FileChooser.set_current_folder(dialog,default_path)
		Gtk.FileChooser.set_current_name(dialog,default_file_name)
		response=dialog.run()
		if response==Gtk.ResponseType.OK:
			self._logger.debug("OK clicked")
			selected_file_name=dialog.get_filename()
			self._logger.debug("File selected = %s ",selected_file_name)
			gtkapplication.api.utility.files.download_and_save_uri(target_uri,selected_file_name)
		elif response==Gtk.ResponseType.CANCEL:
			self._logger.debug("Cancel clicked")
		dialog.destroy()
	def show_file_open_dialog(self,parent_window):
		self._logger.debug('entered show_file_open_dialog')
		file_open_dialog=Gtk.FileChooserDialog("Open...",parent_window,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN,Gtk.ResponseType.OK))
		dialog_response=file_open_dialog.run()
		self._logger.debug("dialog_response = %s",dialog_response)
		local_file=file_open_dialog.get_filename()
		self._logger.debug("local file: %s",local_file)
		file_open_dialog.destroy()
		return (dialog_response,local_file)