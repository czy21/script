#!/usr/bin/env python3

from mako.template import Template

from script.utility.lexer import CustomLexerCls


class CustomTemplate(Template):
    lexer_cls = CustomLexerCls
