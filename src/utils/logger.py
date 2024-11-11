from loguru import logger
import sys
import os

class Logger:
    def __init__(self, name):
        self.logger = logger
        
        # Configure logger
        log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}"
        
        # Remove default handler
        self.logger.remove()
        
        # Add console handler
        self.logger.add(sys.stderr, format=log_format)
        
        # Add file handler
        log_path = os.path.join("logs", f"{name}.log")
        self.logger.add(log_path, rotation="10 MB", format=log_format)
        
    def info(self, message):
        self.logger.info(message)
        
    def error(self, message):
        self.logger.error(message)
        
    def debug(self, message):
        self.logger.debug(message)
        
    def warning(self, message):
        self.logger.warning(message) 