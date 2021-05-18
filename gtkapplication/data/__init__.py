import logging
import os
_logger=logging.getLogger(__name__)
def get_data_folder_location():
	return_value=os.path.abspath(os.path.dirname(__file__))
	_logger.debug("__init__.py get_data_folder_location() returning %s",return_value)
	return return_value