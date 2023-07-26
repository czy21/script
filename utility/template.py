import jinja2

from utility.path import join_path
from utility.safe import decrypt, htpasswd


class Template:
    def __init__(self, text: str):
        env = jinja2.Environment()
        env.filters["join_path"] = lambda p: join_path(*p)
        env.filters["decrypt"] = decrypt
        env.filters["htpasswd"] = htpasswd
        env.filters["zip"] = zip
        env.filters["format_args"] = lambda value, pattern: pattern.format(value) if isinstance(value, str) else pattern.format(*value)
        self.text = text
        self._templator = env.from_string(text)

    def render(self, **kwargs):
        return self._templator.render(**kwargs)
