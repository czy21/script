#!/usr/bin/env python3
from time import sleep
from builtins import print as sys_print


def print(args):
    sleep(0.2)
    sys_print(args)
