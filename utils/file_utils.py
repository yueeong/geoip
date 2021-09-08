import os
import logging

def load_input_data(filename):
    logger = logging.getLogger('console_log')
    if os.path.isfile(filename):
        try:
            input_file_handle = open(filename, mode='r')
            # with open(filename, mode='r') as input_file_handle:
            #     return input_file_handle
            return input_file_handle
        except Exception as e:
            logger.info("Something went wrong loading the apache log file : " + str(e))
    else:
        logger.info('File does not exist.')
