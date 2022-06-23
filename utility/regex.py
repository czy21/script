#!/usr/bin/env python3
import re


def exclude_match(pattern, name):
    return pattern is None or not bool(re.search(pattern, name))
