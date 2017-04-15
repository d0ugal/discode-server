from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments import lexers


class CodeHtmlFormatter(HtmlFormatter):

    # Private they said? LOL
    def _wrap_tablelinenos(self, inner):
        from discode_server import fragments
        yield 0, '<table class="codehilite">'
        lineno = 0
        for t, line in inner:
            if not t:
                continue
            lineno += 1
            yield t, (f'<tr><td class="lineno" id="L{lineno}" '
                      f'data-line-number="{lineno}"></td>')
            yield t, '<td class="line"><pre>'
            yield t, line
            yield t, '</pre></td></tr>'

            comments = self.paste.comments
            if lineno in comments:
                yield 0, fragments.comment_row(lineno, comments[lineno])

        yield 0, '</table>'


def hl(paste):
    formatter = CodeHtmlFormatter(linenos='table')
    formatter.paste = paste
    contents = paste.contents

    if not paste.lexer or paste.lexer == "DETECT_LANGUAGE":
        lexer = lexers.guess_lexer(contents)
    elif paste.lexer == "PLAIN_TEXT":
        lexer = None
    else:
        lexer = lexers.get_lexer_by_name(paste.lexer)

    return highlight(contents, lexer, formatter)


def guess(code, lexer):

    if lexer != 'DETECT_LANGUAGE':
        return lexer, False

    lexer = lexers.guess_lexer(code)
    return lexer.aliases[0], True


def get_lexer_names():
    lexer_specs = lexers.get_all_lexers()
    names = [(l[1][0], l[0]) for l in
             sorted(lexer_specs, key=lambda s: s[0].lower())]
    return names
