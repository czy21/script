#!/usr/bin/env python3
import inspect
import logging
import os
import pathlib
import subprocess

logger = logging.getLogger()


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
    stack_last = inspect.stack()[1]
    stack_file = stack_last.filename
    stack_line = stack_last.lineno
    stack_func = stack_last.function
    logger.info("{0}\n{1}".format("{0} line: {1} func: {2}".format(pathlib.Path(stack_file).as_posix(), str(stack_line), stack_func), cmd))
    if is_input:
        input_exec = str(input("Are you sure you want to execute (y/n)?").strip())
        if input_exec != "y":
            return
    if not dry_run:
        if is_return:
            with subprocess.Popen(["sh", "-c", cmd], stdout=subprocess.PIPE, encoding=encoding, shell=shell) as proc:
                func(iter(proc.stdout.readline, ''), proc, func_param)
                ret = proc.stdout.read()
                proc.stdout.close()
                proc.wait()
                return ret
        else:
            subprocess.Popen(["sh", "-c", cmd], shell=shell).wait()
