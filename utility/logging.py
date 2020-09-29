# coding:utf-8
import logging
from time import sleep

import colorlog

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}

log_sleep = 0.5


class Logger:
    def __init__(self, name=None):
        self.logger = logging.getLogger(name if name else __name__)
        self.logger.setLevel(logging.DEBUG)

        self.formatter = colorlog.ColoredFormatter(
            '%(white)s%(asctime)s  %(log_color)s%(levelname)s %(white)s--- %(cyan)s[%(name)s] %(white)s- %(message)s',
            log_colors=log_colors_config)
        ch = colorlog.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

    def debug(self, message):
        sleep(log_sleep)
        self.logger.debug(message)

    def info(self, message):
        sleep(log_sleep)
        self.logger.info(message)

    def warning(self, message):
        sleep(log_sleep)
        self.logger.warning(message)

    def error(self, message):
        sleep(log_sleep)
        self.logger.error(message)
