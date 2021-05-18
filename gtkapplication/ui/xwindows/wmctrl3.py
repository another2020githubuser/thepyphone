import subprocess
import logging
import os
from collections import namedtuple
class Window():
	def __init__(self):
		self._logger=logging.getLogger(__name__)
		self.BaseWindow=namedtuple('Window','id desktop pid x y w h wm_class host wm_name wm_window_role')
	def list(self):
		out=subprocess.check_output(["wmctrl","-l","-G","-p","-x"]).decode("utf-8")
		windows=[]
		for line in out.splitlines():
			parts=line.split(None,len(self.BaseWindow._fields)-2)
			parts=list(map(str.strip,parts))
			parts[1:7]=list(map(int,parts[1:7]))
			parts.append(self._wm_window_role(parts[0]))
			window=self.BaseWindow._make(parts)
			windows.append(window)
		self._logger.debug("list returning %d windows",len(windows))
		return windows
	def by_name(self,name):
		return [win for win in self.list()if win.wm_name==name]
	def by_name_endswith(self,name):
		return [win for win in self.list()if win.wm_name.endswith(name)]
	def by_name_startswith(self,name):
		return [win for win in self.list()if win.wm_name.startswith(name)]
	def by_role(self,role):
		return [win for win in self.list()if win.wm_window_role==role]
	def by_class(self,wm_class):
		return [win for win in self.list()if win.wm_class==wm_class]
	def by_id(self,window_id):
		self._logger.debug("entered by_id, window_id = %s",window_id)
		window_list=[win for win in self.list()if win.id==window_id]
		if len(window_list)==0:
			self._logger.debug("window with id %d not found",window_id)
			return None
		elif len(window_list)==1:
			self._logger.debug("found window with id %d",window_list[0])
			return window_list[0]
		else:
			self._logger.warning("expected only 1 window with id %d, got %d",window_id,len(window_list))
			return None
	def get_active(self):
		out=subprocess.check_output(["xprop","-root","_NET_ACTIVE_WINDOW"])
		parts=out.split()
		try:
			active_window_id=int(parts[-1],16)
		except ValueError:
			return None
		self._logger.debug("active_window_id = %s",active_window_id)
		lst=self.by_id(active_window_id)
		if not lst:
			self._logger.debug("by_id failed for window_id %d",active_window_id)
			return None
		assert len(lst)==1
		return lst[0]
	def activate(self,window_id):
		os.system('wmctrl -id -a %s'%window_id)
	def resize_and_move(self,window_id,x,y,w,h):
		mvarg='0,%d,%d,%d,%d'%(x,y,w,h)
		os.system('wmctrl -i -r %s -e %s'%(window_id,mvarg))
	def set_geometry(self,window_id,geometry):
		dim,pos=geometry.split('+',1)
		w,h=map(int,dim.split('x'))
		x,y=map(int,pos.split('+'))
		self.resize_and_move(window_id,x,y,w,h)
	def set_properties(self,window_id,properties):
		proparg=",".join(properties)
		os.system('wmctrl -i -r %s -b %s'%(window_id,proparg))
	def _wm_window_role(self,winid):
		args=["xprop","-id",winid,"WM_WINDOW_ROLE"]
		out_bytes=subprocess.check_output(args,stderr=subprocess.STDOUT)
		if out_bytes==b'WM_WINDOW_ROLE:  not found.\n':
			return "not found"
		out_str=out_bytes.decode('utf-8')
		_,value=out_str.split(' = ')
		value=value.strip('"\n')
		return value.strip('"\n')