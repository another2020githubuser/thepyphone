import logging
import pjsua2
class Contact:
	def __init__(self,name,buddy=None):
		self._logger=logging.getLogger(__name__)
		self._name=name
		self.contact_points=[]
		self._buddy=buddy
	@property
	def name(self):
		return self._name
	@property
	def buddy(self):
		return self._buddy
	@buddy.setter
	def buddy(self,pj_buddy):
		assert isinstance(pj_buddy,pjsua2.Buddy)
		self._buddy=pj_buddy
	def destroy_buddy(self):
		assert isinstance(self._buddy,pjsua2.Buddy)
		self._buddy=None
	def __eq__(self,other):
		return self.name==other.name
	def __repr__(self):
		return self._name