import logging
class ContactPoint:
	def __init__(self,point_type,description,uri_string,uri_string_national=None):
		self._logger=logging.getLogger(__name__)
		self._logger.setLevel(logging.INFO)
		self._point_type=point_type
		self._description=description
		self._uri_string=uri_string
		self._uri_string_national=uri_string_national
	def __repr__(self):
		return "{0} {1} {2}".format(self._description,self._uri_string,self._point_type)
	def __eq__(self,other):
		self._logger.debug('entered __eq__')
		are_equal=self._description==other.description and self._uri_string==other.uri_string
		self._logger.debug('__eq__ returning = %s',are_equal)
		return are_equal
	@property
	def point_type(self):
		return self._point_type
	@point_type.setter
	def point_type(self,value):
		self._point_type=value
	@property
	def description(self):
		return self._description
	@property
	def uri_string(self):
		return self._uri_string
	@property
	def uri_string_national(self):
		return self._uri_string_national