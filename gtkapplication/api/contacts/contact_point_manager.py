import logging
class ContactPointManager:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def find_contact_point_by_uri(self,contact,contact_uri_string):
		for contact_point in contact.contact_points:
			if contact_point.uri_string==contact_uri_string:
				return contact_point
		assert False