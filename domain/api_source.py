# !/usr/bin/env python
import io
import math
import os
import re
import sys

sys.path.append("../../")
from script.utility import path, template
from colorama import init, Fore

param_code_api_path = ""


def package():
    mvn_package_command = "mvn clean install"
