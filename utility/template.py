import typing

import jinja2

from utility.basic import getpwnam_uid, getpwnam_gid
from utility.path import join_path
from utility.safe import decrypt, htpasswd


class Undefined(jinja2.Undefined):
    def __str__(self) -> str:
        return "{{ " + self._undefined_name + " }}"


def get_uid(value):
    if isinstance(value, Undefined):
        return value
    return getpwnam_uid(value)


def get_gid(value):
    if isinstance(value, Undefined):
        return value
    return getpwnam_gid(value)


class Template:
    def __init__(self, text: str, undefined: typing.Type[jinja2.Undefined] = jinja2.Undefined):
        env = jinja2.Environment()
        env.undefined = undefined
        env.filters["join_path"] = lambda value: value if isinstance(value, Undefined) else join_path(*value)
        env.filters["decrypt"] = lambda value, mode: value if isinstance(value, Undefined) else decrypt(value, mode)
        env.filters["htpasswd"] = lambda value: value if isinstance(value, Undefined) else htpasswd(value)
        env.filters["format_args"] = lambda value, pattern: value if isinstance(value, Undefined) else pattern.format(value) if isinstance(value, str) else pattern.format(*value)
        env.filters["get_uid"] = lambda value: value if isinstance(value, Undefined) else get_uid(value)
        env.filters["get_gid"] = lambda value: value if isinstance(value, Undefined) else get_gid(value)
        self.text = text
        self._templator = env.from_string(text)

    def render(self, **kwargs):
        return self._templator.render(**kwargs)
