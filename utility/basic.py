#!/usr/bin/env python3
import logging
import subprocess
import sys

from colorama import Fore

logger = logging.getLogger()


def action_formatter(action_name: str, message=None):
    return "{0} => {1}".format(action_name, message)


def print_default(msg_lines, proc: subprocess.Popen, func_param) -> None:
    for line in msg_lines:
        line = line.strip()
        if line:
            logger.info(line)


def execute(cmd, func=print_default, func_param=None, encoding="utf-8"):
    input_exec = str(input("Are you sure you want to execute (y/n)?").strip())
    if input_exec != "y":
        return
    with subprocess.Popen(["sh", "-c", cmd], stdout=subprocess.PIPE, encoding=encoding, shell=True) as proc:
        func(iter(proc.stdout.readline, ''), proc, func_param)
        proc.stdout.close()
        proc.wait()
        if proc.returncode != 0:
            sys.exit(0)


if __name__ == '__main__':
    cmd1 = "java --version"
    cmd2 = "mysql --version"
    execute(cmd1)
    execute(cmd2)
    print("sss")
