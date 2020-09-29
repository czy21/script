#!/usr/bin/env python3
import logging

import colorlog
from colorama import Fore

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


class Logger:
    def __init__(self, name=None):
        self.logger = logging.getLogger(name if name else __name__)
        self.logger.setLevel(logging.DEBUG)

        self.formatter = colorlog.ColoredFormatter(
            '%(black)s%(asctime)s  %(log_color)s%(levelname)s %(black)s--- %(cyan)s[%(name)s] - %(message)s',
            log_colors=log_colors_config)
        ch = colorlog.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)


def message_formatter(action_name, msg=None, action_color=Fore.YELLOW):
    action_name_msg = action_color + action_name
    if msg:
        action_name_msg += Fore.BLACK + " => " + msg
    return action_name_msg
