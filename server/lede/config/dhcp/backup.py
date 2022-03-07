#!/usr/bin/env python3
import sys

sys.path.append('{{ param_project_path }}')
import share


def backup_domain():

    share.execute_cmd("echo a")


if __name__ == '__main__':
    backup_domain()
