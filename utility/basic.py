#!/usr/bin/env python3
import subprocess

from colorama import Fore


def action_formatter(action_name, msg=None, action_color=Fore.YELLOW):
    action_name_msg = action_color + action_name
    if msg:
        action_name_msg += Fore.WHITE + " => " + msg
    return action_name_msg


if __name__ == '__main__':
    cmd = r"dir"

    out = subprocess.getstatusoutput(cmd)
    print(out)
