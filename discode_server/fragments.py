from discode_server.utils import templates

import jinja2

_COMMENT_ROW = jinja2.Template("""
""")

env = templates.jinja_env()


def comment_row(lineno, comments):
    return templates.render_text("comments.html",
                                 lineno=lineno, comments=comments)
