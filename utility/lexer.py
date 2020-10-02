from mako import parsetree
from mako.lexer import Lexer


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
