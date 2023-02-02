#!/usr/bin/env python3
import json
import logging
import re

logger = logging.getLogger()


def is_match(pattern: str, name: str):
    return bool(re.compile(pattern).search(name))


def match_rules(rules: list[str], text: str, name: str = "") -> dict[str, bool]:
    _rules = {r: is_match(r.lower(), text.lower()) for r in rules}
    logger.debug("{0} match {1} => {2}".format(name, text, json.dumps(_rules)))
    return _rules
