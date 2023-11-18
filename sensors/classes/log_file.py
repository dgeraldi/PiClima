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
from colorama import init, Fore, Style
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

        #reset coloring
        init(autoreset=True)
		
    def log(self, level, message):
        """Log a message with the specified level"""
        log_method = getattr(self.logger, level, None)
        if log_method:
            log_method(message)

    def showMessage(self,symbol,title, message, spacesBefore=False, spacesAfter=True):
        if(spacesBefore):
            print('\r')
        print(Style.BRIGHT + Fore.GREEN + "[" +
              Fore.YELLOW + f"{symbol}" +
              Fore.GREEN + f"] {title}" +
              Fore.WHITE + f" {message}")
        # An empty line between first line and the result(more clear output)
        if(spacesAfter):
            print('\r')

        return

    '''
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