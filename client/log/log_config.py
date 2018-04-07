import logging
import logging.handlers

from client.utils.common import CODING
from client.log.log_common import *

FILENAME_PATH = 'client/log'

# logger_name = sys.argv[0].split('/')[-1]
logger_name = LOGGER_NAME
logger = logging.getLogger(logger_name)

handler_level = logging.INFO

file_name = FILE_NAME
file_path = FILE_PATH

handler = logging.FileHandler(file_path, 'a', encoding=CODING)

handler.setLevel(handler_level)

formatter = logging.Formatter('%(asctime)s   %(levelname)-8s    %(message)s')

handler.setFormatter(formatter)

logger.addHandler(handler)

if __name__ == '__main__':
    logger.info('info message')
    logger.error('error message')
    logger.critical('critical message')
