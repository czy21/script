#!/usr/bin/env python3
from mako import parsetree
from mako.lexer import Lexer
from mako.template import Template


class CustomLexerCls(Lexer):
    def match_expression(self):
        match = self.match(r"\${{{")
        if match:
            line, pos = self.matched_lineno, self.matched_charpos
            text, end = self.parse_until_text(True, r"\|", r"}}}")
            if end == "|":
                escapes, end = self.parse_until_text(True, r"}}}")
            else:
                escapes = ""
            text = text.replace("\r\n", "\n")
            self.append_node(
                parsetree.Expression,
                text,
                escapes.strip(),
                lineno=line,
                pos=pos,
            )
            return True
        else:
            return False


class CustomTemplate(Template):
    lexer_cls = CustomLexerCls

    def __init__(self, text=None, filename=None, strict_undefined=True):
        Template.__init__(self, text=text, filename=filename, strict_undefined=strict_undefined)
