#!/usr/bin/python

"""Generate log Files

	Execution
		Called by each class and script

	Return
		None
"""
__title__ = 'PiClima - LogFile'
__author__ = 'Daniel Geraldi'
__license__ = 'MIT'

import logging
from logging.handlers import RotatingFileHandler
#from pathlib import Path

class LogFile:
    def __init__(self, sensor_name, log_directory='/var/log/PiClima'):
        """Initialize the logger"""
        self.log_file = f'{log_directory}/sensor_{sensor_name}.log'
        self.logger = logging.getLogger(sensor_name)
        self.logger.setLevel(logging.INFO)
        
        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) - %(message)s', "%d-%m-%Y %H:%M:%S")
        log_handler = RotatingFileHandler(self.log_file, mode='a', maxBytes=5 * 1024 * 1024, backupCount=3, encoding=None, delay=0)
        log_handler.setFormatter(log_formatter)
        log_handler.setLevel(logging.INFO)
        self.logger.addHandler(log_handler)
		
    def log(self, level, message):
        """Log a message with the specified level"""
        log_method = getattr(self.logger, level, None)
        if log_method:
            log_method(message)

    '''def __init__(self,sensorName):
        """Init all variables"""  

        #Create rotating log files, alternating between 5 files when the file reaches 5MB
        logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)d) - %(message)s',"%d-%m-%Y %H:%M:%S")
        logFile = f'/var/log/PiClima/sensor_{sensorName}.log'
        logHandler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=3, encoding=None, delay=0)
        logHandler.setFormatter(logFormatter)
        logHandler.setLevel(logging.INFO)

        self.logger = logging.getLogger(sensorName)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logHandler)
		
    def log(self, level, message):

        if level == 'debug':
            self.logger.debug(message)
        elif level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)'''