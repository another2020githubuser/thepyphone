import logging
class GtkTextBuffer:
	def __init__(self):
		self._logger=logging.getLogger(__name__)
	def get_text(self,text_buffer):
		contents=str(text_buffer.get_text(text_buffer.get_start_iter(),text_buffer.get_end_iter(),True))
		self._logger.debug("contents = '%s'",contents)
		assert isinstance(contents,str)
		return contents