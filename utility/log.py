# coding:utf-8
import logging
import sys
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


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def parse_argv(argv: list, key):
    for a in argv:
        if a == key:
            return sys.argv[sys.argv.index(key) + 1]
    return ""


class Logger(metaclass=Singleton):

    def __init__(self, name=None):
        self.logger = logging.getLogger(name if name else __name__)
        self.logger.setLevel(logging.DEBUG)
        ch = colorlog.StreamHandler()
        ch.setFormatter(colorlog.ColoredFormatter(
            '%(white)s%(asctime)s %(log_color)s%(levelname)s %(purple)s%(thread)d %(white)s[ %(threadName)s ] %(cyan)s%(name)s %(white)s- %(message)s',
            log_colors=log_colors_config))

        env_path = parse_argv(sys.argv, "--env")
        log_file = parse_argv(sys.argv, "--log-file")
        if log_file != "":
            fh = logging.FileHandler(filename=Path(env_path).joinpath("../", log_file).absolute().resolve().as_posix(), encoding='utf-8')
            fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(thread)d [ %(threadName)s ] %(name)s - %(message)s'))
            self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def debug(self, message):
        sleep(log_sleep)
        self.logger.debug(message)

    def info(self, message, is_sleep=True):
        if is_sleep:
            sleep(log_sleep)
        self.logger.info(message)

    def warning(self, message):
        sleep(log_sleep)
        self.logger.warning(message)

    def error(self, message, is_sleep=True):
        if is_sleep:
            sleep(log_sleep)
        self.logger.error(message)
