#!/usr/bin/env python3
import json
import logging
import re
from typing import Any

logger = logging.getLogger()


def is_match(pattern: str, name: str):
    return bool(re.compile(pattern).search(name))


def match_rules(rules: list[str] | Any, text: str, name: str = "") -> dict[str, bool]:
    _rules = {r: is_match(r.lower(), text.lower()) for r in rules}
    logger.debug("{0} {1}: {2}".format(name, text, json.dumps(_rules)))
    return _rules
