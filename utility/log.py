# coding:utf-8
import logging
import pathlib

import colorlog

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


def init_logger(name=None, file: pathlib.Path = None):
    logger = logging.getLogger(name)
    ch = colorlog.StreamHandler()
    color_format = '%(asctime)s %(log_color)s%(levelname)s %(reset)s[ %(threadName)s ] %(cyan)s%(name)s %(reset)s- %(message)s'
    ch.setFormatter(colorlog.ColoredFormatter(color_format, log_colors=log_colors_config))
    logger.addHandler(ch)
    if file:
        if not file.exists():
            file.parent.mkdir(exist_ok=True, parents=True)
            file.touch(exist_ok=True)
        fh = logging.FileHandler(filename=file.absolute().as_posix(), encoding='utf-8')
        fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(thread)d [ %(threadName)s ] %(name)s - %(message)s'))
        logger.addHandler(fh)