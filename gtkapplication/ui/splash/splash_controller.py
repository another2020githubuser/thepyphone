#!/usr/bin/env python3
import logging
import subprocess
import time
import os.path
import sys
log_filename="logs/splash_controller-log.txt"
date_fmt="%Y-%m-%d,%H:%M:%S"
log_format="%(asctime)s.%(msecs)03d %(levelname)s %(threadName)s %(name)s.%(funcName)s %(message)s"
logging.basicConfig(format=log_format,datefmt=date_fmt,level=logging.INFO,filename=log_filename)
logger=logging.getLogger(__name__)
here=os.path.abspath(os.path.dirname(__file__))
logger.debug("here = %s",here)
pyphone_application=sys.argv[1]
logger.debug("application = %s",pyphone_application)
assert os.path.exists(pyphone_application)
splash_screen_application=os.path.join(here,"splash_screen.py")
logger.debug("splash_screen = %s",splash_screen_application)
app_process=subprocess.Popen(["python3",pyphone_application])
app_pid=str(app_process.pid)
logger.debug("after subprocess.Popen([application]), app_pid is %s",app_pid)
splash_process=subprocess.Popen(["python3",splash_screen_application])
splash_pid=str(splash_process.pid)
logger.debug("after subprocess.Popen(['python3', splash_screen]), splash_pid = %s",splash_pid)
while True:
	logger.debug("entered while loop")
	time.sleep(0.5)
	logger.debug("app_pid = %s",app_pid)
	try:
		w_list=subprocess.check_output(["wmctrl","-lp"]).decode("utf-8")
		logger.debug("w_list =\n%s",w_list)
		if app_pid in w_list:
			logger.debug("splash_pid = %s",splash_pid)
			subprocess.Popen(["kill",splash_pid])
			logger.debug("after kill")
			break
	except subprocess.CalledProcessError as error2:
		logger.error(error2)
logger.debug("after while loop")