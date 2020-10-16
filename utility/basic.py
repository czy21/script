#!/usr/bin/env python3
import subprocess
import sys

from colorama import Fore

from script.utility import log

logger = log.Logger(__name__)


def action_formatter(action_name, msg=None, action_color=Fore.YELLOW):
    action_name_msg = action_color + action_name
    if msg:
        action_name_msg += Fore.WHITE + " => " + msg
    return action_name_msg


def print_default(msg_lines, proc, func_param) -> None:
    for line in msg_lines:
        line = line.strip()
        if line:
            logger.info(line, is_sleep=False)


def execute(cmd, func=print_default, func_param=None):
    if func_param is None:
        func_param = {}
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, encoding="utf-8")
    func(iter(proc.stdout.readline, ''), proc, func_param)
    proc.stdout.close()
    proc.wait()
    if proc.returncode != 0:
        sys.exit(0)
    return proc





if __name__ == '__main__':
    cmd1 = "java --version"
    cmd2 = "mysql --version"
    execute(cmd1)
    execute(cmd2)
    print("sss")
