# coding:utf-8
import logging
import os
import pathlib
from pathlib import Path
from time import sleep

import colorlog

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}

log_sleep = 0.1


class Logger:

    def __init__(self, name=None):
        self.logger = logging.getLogger(name if name else __name__)
        self.logger.setLevel(logging.INFO)
        ch = colorlog.StreamHandler()
        ch.setFormatter(colorlog.ColoredFormatter(
            '%(white)s%(asctime)s %(log_color)s%(levelname)s %(purple)s%(thread)d %(white)s[ %(threadName)s ] %(cyan)s%(name)s %(white)s- %(message)s',
            log_colors=log_colors_config))
        self.logger.addHandler(ch)

    def set_log_file(self, file: pathlib.Path):
        fh = logging.FileHandler(filename=file.absolute().as_posix(), encoding='utf-8')
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(thread)d [ %(threadName)s ] %(name)s - %(message)s'))
        self.logger.addHandler(fh)

    def debug(self, message, name=None):
        if self.logger.level == logging.DEBUG:
            if name:
                self.logger.name = name
            self.logger.debug(message)

    def info(self, message, name=None):
        if self.logger.level == logging.INFO:
            if name:
                self.logger.name = name
            self.logger.info(message)

    def warning(self, message, name=None):
        if self.logger.level == logging.WARNING:
            if name:
                self.logger.name = name
            self.logger.warning(message)

    def error(self, message, name=None):
        if self.logger.level == logging.ERROR:
            if name:
                self.logger.name = name
            self.logger.error(message)
