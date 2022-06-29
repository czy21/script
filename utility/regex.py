#!/usr/bin/env python3
import json
import logging
import re

logger = logging.getLogger()


def is_match(pattern: str, name: str):
    return bool(re.search(pattern, name))


def not_match(pattern: str, text: str):
    return not is_match(pattern, text)


def match_rules(rules: list, text: str, name: str = ""):
    _rules = [{"rule": r, "isMatch": is_match(r, text)} for r in rules]
    logger.debug("{0} rules: {1} => {2}".format(name, text, json.dumps(_rules)))
    return _rules
