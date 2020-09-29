#!/usr/bin/env python3
import subprocess

from colorama import Fore

from script.utility import logging

logger = logging.Logger(__name__)


def action_formatter(action_name, msg=None, action_color=Fore.YELLOW):
    action_name_msg = action_color + action_name
    if msg:
        action_name_msg += Fore.WHITE + " => " + msg
    return action_name_msg


def print_default(msg_lines) -> None:
    for line in msg_lines:
        logger.info(line.decode("UTF8").strip(), is_sleep=False)


def execute(cmd, func=print_default):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    func(iter(proc.stdout.readline, b''))
    proc.stdout.close()
    proc.wait()


def java_version():
    cmd = "jav --version"
    out = subprocess.getstatusoutput(cmd)
    print(out[1])


def mysql_version():
    cmd = "mysql --version"
    out = subprocess.getstatusoutput(cmd)
    print(out[1])


if __name__ == '__main__':
    java_version()
    mysql_version()
    print("sss")
