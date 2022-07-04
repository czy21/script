#!/usr/bin/env python3
import configparser
import io
import itertools
import pathlib

import share
import yaml

from utility import collection as collection_util

if __name__ == '__main__':
    root_path = pathlib.Path(__file__).parent
    installer = share.Installer(root_path, None)
    installer.run()
