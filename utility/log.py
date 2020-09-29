# coding:utf-8
import logging
from logging.handlers import RotatingFileHandler # 按文件大小滚动备份
import colorlog  # 控制台日志输入颜色
import time
import datetime
import os

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


class Log:
    def __init__(self, name=None):
        self.logger = logging.getLogger(name if name else __name__)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
            log_colors=log_colors_config)  # 日志输出格式
        ch = colorlog.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info( message)

    def warning(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.info(message)


if __name__ == "__main__":
    log = Log()
    log.debug("---测试开始----")
    log.info("操作步骤")
    log.warning("----测试结束----")
    log.error("----测试错误----")