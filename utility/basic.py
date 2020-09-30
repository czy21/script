#!/usr/bin/env python3
import subprocess

from colorama import Fore

from script.utility import log

logger = log.Logger(__name__)


def action_formatter(action_name, msg=None, action_color=Fore.YELLOW):
    action_name_msg = action_color + action_name
    if msg:
        action_name_msg += Fore.WHITE + " => " + msg
    return action_name_msg


def print_default(msg_lines) -> None:
    for line in msg_lines:
        if line:
            logger.info(line, is_sleep=False)


def execute(cmd, func=print_default):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, encoding="utf-8")
    func(iter(proc.stdout.readline, ''))
    proc.stdout.close()
    proc.wait()


if __name__ == '__main__':
    cmd1 = "jav --version"
    cmd2 = "mysql --version"
    execute(cmd1)
    execute(cmd2)
    print("sss")
