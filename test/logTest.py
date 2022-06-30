import logging

from utility import log as log_util

logger = logging.getLogger()

if __name__ == '__main__':
    log_util.init_logger()
    logger.info("\n abcd")
