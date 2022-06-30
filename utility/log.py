# coding:utf-8
import logging
import pathlib

import colorlog


def init_logger(name=None, file: pathlib.Path = None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    ch = colorlog.StreamHandler()
    color_format = '%(asctime)s %(log_color)s%(levelname)s %(reset)s[ %(threadName)s ] %(cyan)s%(name)s %(reset)s- %(message)s'
    ch.setFormatter(colorlog.ColoredFormatter(color_format))
    logger.addHandler(ch)
    if file:
        file.parent.mkdir(exist_ok=True, parents=True)
        file.write_text("")
        fh = logging.FileHandler(filename=file.absolute().as_posix(), encoding='utf-8')
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [ %(threadName)s ] %(name)s - %(message)s'))
        logger.addHandler(fh)
