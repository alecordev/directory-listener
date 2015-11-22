"""
alecor
"""

import os
import sys
import time
import shutil
import logging
from logging import handlers
import datetime

SLEEP_TIME = 3
PATH = '.'
# in, processing and processed are folders under the specified PATH
INPUT_PATH = os.path.join(PATH, 'in')
PROCESSING_PATH = os.path.join(PATH, 'processing')
PROCESSED_PATH = os.path.join(PATH, 'processed')

def create_logger(filename=None, max_size=0, max_quantity=0):
    
    LOG_FILENAME = filename or datetime.datetime.now().strftime('listener_%Y%m%d.log')
    LOG_MAX_SIZE = max_size
    LOGS_MAX_QUANTITY = max_quantity
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    fh = handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=LOG_MAX_SIZE, backupCount=LOGS_MAX_QUANTITY)
    fh.setLevel(logging.INFO)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)
    
    return logger

logger = create_logger()

def main(file_to_process):
    """
    Do stuff with the file_to_process.

    file_to_process -> str
    Here, the file can be found in: os.path.join(PROCESSING_PATH, file_to_process)

    raise Exception if processing failed for whatever reason.
    """
    logger.info('Processing {}'.format(file_to_process))
    # with open(os.path.join(PROCESSING_PATH, file_to_process), 'r') as f:
    #     logger.info(f.readline())

def process(file_to_process):
    try:
        f_name, f_ext = os.path.splitext(file_to_process)
        shutil.copy(os.path.join(INPUT_PATH, file_to_process), os.path.join(PROCESSING_PATH, file_to_process))
        os.remove(os.path.join(INPUT_PATH, file_to_process))
        try:
            main(file_to_process)
        except Exception as e:
            logger.error(e)
        else:
            logger.info('Cleaning up {}'.format(file_to_process))
            shutil.copy(os.path.join(PROCESSING_PATH, file_to_process), os.path.join(PROCESSED_PATH, file_to_process))
            os.remove(os.path.join(PROCESSING_PATH, file_to_process))
    except Exception as e:
        logger.error('Error: {}'.format(e))

if __name__ == '__main__':
    
    if len(sys.argv) >= 2:
        INPUT_PATH = sys.argv[1]
        logger.info('Input path set as {}'.format(INPUT_PATH))

    while 1:
        try:
            for file_to_process in os.listdir(PROCESSING_PATH):
                process(file_to_process)
            for file_to_process in os.listdir(INPUT_PATH):
                process(file_to_process)
            time.sleep(SLEEP_TIME)
        except Exception as e:
            logger.error('Error: {}'.format(e))
