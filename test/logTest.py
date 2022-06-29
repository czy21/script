import logging

from utility import log as log_util


if __name__ == '__main__':
    logger1=log_util.Logger("aaa")
    logger1.logger.setLevel(logging.WARNING)
    logger2=log_util.Logger("aaa")
    print("a")