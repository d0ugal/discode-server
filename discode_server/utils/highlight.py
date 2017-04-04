from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments import lexer
from pygments import lexers
from pygments import token

from discode_server import fragments


class CodeHtmlFormatter(HtmlFormatter):

    # Private they said? LOL
    def _wrap_tablelinenos(self, inner):
        yield 0, '<table class="codehilite">'
        lineno = 0
        for t, line in inner:
            if not t:
                continue
            lineno += 1
            yield t, f'<tr><td class="lineno" id="L{lineno}" data-line-number="{lineno}"></td>'
            yield t, '<td class="line"><pre>'
            yield t, line
            yield t, '</pre></td></tr>'

            comments = self.paste.comments
            if lineno in comments:
                yield 0, fragments.comment_row(lineno, comments[lineno])

        yield 0, '</table>'


class MistralLexer(lexer.RegexLexer):

    name = 'Mistral'
    aliases = ['mistral']

    tokens = {
        "root": [
            (r'^(\s)*(workflows|tasks|input)(\s)*:', token.Keyword),
            (r'^(\s)*(version|name|description)(\s)*:', token.Keyword),
            (r'^(\s)*(publish|timeout|retry|with\-items)(\s)*:', token.Keyword),
            (r'^(\s)*(on\-success|on\-error|on\-complete)(\s)*:', token.Keyword),
            (r'^(\s)*(action|workflow)(\s)*:', token.Keyword, 'call'),
            (r'(\-|\:)(\s)*(fail|succeed|pause)(\s)+', token.Operator.Word),
            (r'<%', token.Name.Entity, 'expression'),
            (r'\{\{', token.Name.Entity, 'expression'),
            (r'#.*$', token.Comment),
            (r'(^|\s|\-)+\d+', token.Number),
            lexer.include("generic"),
        ],
        "expression": [
            (r'\$', token.Operator),
            (r'\s(json_pp|task|tasks|execution|env|uuid)(?!\w)', token.Name.Builtin),
            lexer.include("generic"),
            (r'%>', token.Name.Entity, '#pop'),
            (r'}\\}', token.Name.Entity, '#pop'),
        ],
        "call": [
            (r'(\s)*[\w\.]+($|\s)', token.Name.Function),
            lexer.default('#pop'),
        ],
        "generic": [
            (r'(\-|:|=|!|\[|\])', token.Operator),
            (r'(null|None|True|False)', token.Name.Builtin),
            (r'"(\\\\|\\"|[^"])*"', token.String.Double),
            (r"'(\\\\|\\'|[^'])*'", token.String.Single),
            (r'\w|\s|\(|\)|,|\.', token.Text),
        ]
    }

    def analyse_text(text):
        score = 0
        if 'tasks:' in text:
            score += 0.2
        if 'action:' in text:
            score += 0.2
        if 'on-success:' in text:
            score += 0.2
        if 'on-error:' in text:
            score += 0.2
        if 'on-complete:' in text:
            score += 0.2
        return score


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
    names = [(l[1][0], l[0]) for l in sorted(lexer_specs, key=lambda s: s[0].lower())]
    return names
