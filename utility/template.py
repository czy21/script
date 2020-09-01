#!/usr/bin/env python3

from string import Template


# example: m=StringTemplate("${{{var}}}")
# print(m.safe_substitute(var="hello"))
class StringTemplate(Template):
    delimiter = '$'
    pattern = r'''
        \$(?:
          (?P<escaped>\$) |   # Escape sequence of two delimiters
          (?P<named>[_a-z][_a-z0-9]*)      |   # delimiter and a Python identifier
          {{{(?P<braced>[_a-z][_a-z0-9]*)}}}   |   # delimiter and a braced identifier
          (?P<invalid>)              # Other ill-formed delimiter exprs
        )
        '''
