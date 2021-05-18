import logging
import logging.handlers
import coloredlogs
import sys
class Config:
	def initialize_logging(self):
		log_filename="logs/gtkapplication-log.txt"
		date_fmt="%Y-%m-%d,%H:%M:%S"
		log_level=logging.DEBUG
		log_format="%(asctime)s.%(msecs)03d %(levelname)s %(threadName)s %(name)s.%(funcName)s %(message)s"
		stderr_handler=logging.StreamHandler(sys.stderr)
		stderr_handler.setLevel(logging.WARNING)
		timed_rotating_file_logging_handler=logging.handlers.TimedRotatingFileHandler(log_filename,when="D",backupCount=93)
		timed_rotating_file_logging_handler.setLevel(log_level)
		formatter=logging.Formatter(fmt=log_format,datefmt=date_fmt)
		timed_rotating_file_logging_handler.setFormatter(formatter)
		logging.basicConfig(format=log_format,datefmt=date_fmt,level=log_level)
		logger=logging.getLogger(__name__)
		coloredlogs.install(fmt=log_format,level=log_level)
		root_logger=logging.getLogger()
		root_logger.addHandler(timed_rotating_file_logging_handler)
		root_logger.addHandler(stderr_handler)
		logger.debug("Effective Logging Level is %s",logging.getLevelName(logging.getLogger(__name__).getEffectiveLevel()))
		logger.debug("Loggers = %s",logging.Logger.manager.loggerDict.keys())
		logger.debug('Executing Name %s in file %s',__name__,__file__)
		return root_logger