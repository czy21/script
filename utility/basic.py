#!/usr/bin/env python3
import inspect
import logging
import os
import pathlib
import subprocess
import re

if os.name != "nt":
    import pwd

logger = logging.getLogger()


def getpwnam_uid(name, default=1000):
    try:
        return pwd.getpwnam(name).pw_uid
    except KeyError:
        return default


def getpwnam_gid(name, default=1000):
    try:
        return pwd.getpwnam(name).pw_gid
    except KeyError:
        return default


def action_formatter(action_name: str, message=None):
    return "{0} => {1}".format(action_name, message)


def print_default(msg_lines, proc: subprocess.Popen, func_param) -> None:
    for line in msg_lines:
        line = line.strip()
        if line:
            logger.info(line)


def execute(
        cmd,
        func=print_default,
        func_param=None,
        encoding="utf-8",
        is_input=True,
        is_return=True,
        shell=os.name == 'nt',
        dry_run=False
):
    if is_input:
        input_exec = str(input("Are you sure you want to execute (y/n)?").strip())
        if input_exec != "y":
            return
    if not dry_run:
        if is_return:
            with subprocess.Popen(["sh", "-c", "PATH=$PATH:/usr/local/bin;{0}".format(cmd)], stdout=subprocess.PIPE, encoding=encoding, shell=shell) as proc:
                func(iter(proc.stdout.readline, ''), proc, func_param)
                ret = proc.stdout.read()
                proc.stdout.close()
                proc.wait()
                return ret
        else:
            subprocess.Popen(["sh", "-c", "PATH=$PATH:/usr/local/bin;{0}".format(cmd)], shell=shell).wait()
