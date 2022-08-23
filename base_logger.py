import logging
import os

# setting up the logger
logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

console_handler_format = '%(asctime)s | %(levelname)s: %(message)s'
console_handler.setFormatter(logging.Formatter(console_handler_format))
logger.addHandler(console_handler)

# the second handler is a file handler
file_handler = logging.FileHandler(os.path.join(os.getcwd(), 'logger_file.log'))
file_handler.setLevel(logging.INFO)
file_handler_format = '%(asctime)s | %(levelname)s | %(lineno)d: %(message)s'
file_handler.setFormatter(logging.Formatter(file_handler_format))
logger.addHandler(file_handler)
