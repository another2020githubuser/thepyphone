import logging
import gtkapplication.ui.gtk.window_manager
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
class JumpToWindowHelper:
	def __init__(self,gtk_builder):
		self._logger=logging.getLogger(__name__)
		self._logger.setLevel(logging.DEBUG)
		self._gtk_builder=gtk_builder
		self._window_manager=gtkapplication.ui.gtk.window_manager.WindowManager()
		self._static_jump_location_list=[["Contacts",[],self._window_manager.get_contacts_window],["Dashboard",[],self._window_manager.get_dashboard_window],["Keypad",[],self._window_manager.get_keypad_window],["Voice",[],self._window_manager.get_voice_window]]
		self._dyanmic_fill_list=[["Free Buddy Text",self._window_manager.get_free_buddy_text_window_keys],["SMS ($)",self._window_manager.get_sms_window_keys],]
		self.update_jump_list()
		treeview=self._gtk_builder.get_object("jump_treeview")
		treeview.connect("row-activated",self.on_treeview_row_clicked)
		treeview_selection=treeview.get_selection()
		treeview_selection.set_mode(Gtk.SelectionMode.SINGLE)
		treeview.expand_all()
	def on_treeview_row_clicked(self,tree_view,path,column):
		self._logger.debug("on_treeview_row_clicked, path is %s",path)
		selection=tree_view.get_selection()
		(model,treeiter)=selection.get_selected()
		value=model.get_value(treeiter,0)
		self._logger.debug('value = %s',value)
		has_children=model.iter_has_child(treeiter)
		self.jump_to_window(path,value,has_children)
		jump_menu_button=self._gtk_builder.get_object("jump_menu_button")
		jump_menu_button.set_active(False)
		self._logger.debug("after jump_menu_button.set_active(False)")
	def jump_to_window(self,path,value,has_children):
		self._logger.debug("entered jump_to_window")
		self._logger.debug("depth = %d",path.get_depth())
		self._logger.debug("path = %s",path)
		indices=path.get_indices()
		depth=path.get_depth()
		self._logger.debug('indices = %s',indices)
		if depth==1 and has_children:
			self._logger.debug("depth = 1 and has children, not invoking jump function")
		elif depth==1 and not has_children:
			index=int(path.to_string())
			jump_to_location=self._static_jump_location_list[index][2]
			jump_to_location()
		elif depth==2:
			self._logger.debug("depth == 2, value = %s",value)
			self._window_manager.get_window_by_key(value,True)
		else:
			raise ValueError("Invalid depth: {0}".format(depth))
	def update_jump_list(self):
		self._logger.debug("entered update_jump_list")
		treestore=self._gtk_builder.get_object("treestore")
		treestore.clear()
		for row in self._static_jump_location_list:
			window_name=row[0]
			self._logger.debug("adding window_name %s",window_name)
			piter=treestore.append(None,[window_name])
		for row in self._dyanmic_fill_list:
			self._logger.debug("invoking function %s",row[1])
			window_unique_keys=row[1]()
			self._logger.debug("function %s returned %s",row[1],window_unique_keys)
			if window_unique_keys==[]:
				self._logger.debug("dynamic window %s has no children",row[0])
			else:
				self._logger.debug("adding dynamic window_name %s",row[0])
				piter=treestore.append(None,[row[0]])
				for window_unique_key in window_unique_keys:
					self._logger.debug("adding dynamic window key %s",window_unique_key)
					treestore.append(piter,[window_unique_key])
		self._logger.debug("treestore filled with %d items, %s",len(treestore),print_tree_store(treestore))
		jump_menu_button=self._gtk_builder.get_object("jump_menu_button")
		if jump_menu_button.get_active():
			i=0
			treeview=self._gtk_builder.get_object("jump_treeview")
			while Gtk.events_pending():
				Gtk.main_iteration_do(False)
				i+=1
			self._logger.debug("%d events processed",i)
_logger=logging.getLogger(__name__)
def print_tree_store(store):
	rootiter=store.get_iter_first()
	print_rows(store,rootiter,"")
def print_rows(store,treeiter,indent):
	while treeiter is not None:
		_logger.debug(indent+str(store[treeiter][:]))
		if store.iter_has_child(treeiter):
			childiter=store.iter_children(treeiter)
			print_rows(store,childiter,indent+"\t")
		treeiter=store.iter_next(treeiter)