import pathlib

import jinja2

from utility.path import join_path
from utility.safe import decrypt, htpasswd


class Template:
    def __init__(self, text: str):
        self.text = text
        self._templator = jinja2.Template(text)
        self._templator.globals["join_path"] = join_path
        self._templator.globals["decrypt"] = decrypt
        self._templator.globals["htpasswd"] = htpasswd

    def render(self, **kwargs):
        return self._templator.render(**kwargs)
