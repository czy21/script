#!/usr/bin/env python3
import logging
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Logger:
    __logger = logging.getLogger()

    def __init__(self, name=None):
        self.__logger.name = name if name else __name__

    @classmethod
    def info(cls, message, *args, **kwargs):
        sleep(0.5)
        cls.__logger.info(message, *args, **kwargs)
