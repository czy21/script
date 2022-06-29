#!/usr/bin/env python3
import re


def is_match(pattern: str, name: str):
    return bool(re.search(pattern, name))


def not_match(pattern: str, text: str):
    return not is_match(pattern, text)
