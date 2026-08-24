#!/usr/bin/env python3

import argparse
import itertools
import json
import pathlib
import subprocess
from itertools import chain
from typing import TypeVar, Generic, Callable, List, Optional
from urllib.parse import urlparse

import requests

parser = argparse.ArgumentParser()
parser.add_argument('--updates-dir', required=True)
args: argparse.Namespace = parser.parse_args()

for t in pathlib.Path(args.updates_dir).rglob('*.json'):
    file_text = t.read_text(encoding="utf-8")
    file_text = file_text.replace(f"downloadService.post('{t.stem}',",'').replace('})','}')
    html_text = f'''<!DOCTYPE html><html><head><meta http-equiv='Content-Type' content='text/html;charset=UTF-8' /></head><body><script>window.onload = function () {{ window.parent.postMessage(JSON.stringify({file_text}),'*'); }};</script></body></html>'''
    pathlib.Path(t.as_posix() + ".html").write_text(html_text, encoding="utf-8")