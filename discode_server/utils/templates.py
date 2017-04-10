import re
import pathlib

from sanic import response
import CommonMark
import bleach
import jinja2

from discode_server.utils import highlight

_env = None
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@jinja2.evalcontextfilter
def nl2br(eval_ctx, value):
    br = jinja2.Markup('<br>\n')
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', br)
                          for p in _paragraph_re.split(jinja2.escape(value)))
    if eval_ctx.autoescape:
        result = jinja2.Markup(result)
    return result


def _bleach(contents):
    markdown_tags = [
        "h1", "h2", "h3", "h4", "h5", "h6",
        "b", "i", "strong", "em", "tt",
        "p", "br",
        "span", "div", "blockquote", "code", "hr", "pre",
        "ul", "ol", "li", "dd", "dt",
        "img",
        "a",
    ]
    return bleach.clean(contents, tags=markdown_tags)


def jinja_env():
    global _env

    if _env is not None:
        return _env

    path = str(pathlib.Path('.') / "templates")
    _env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)
    )
    _env.filters['highlight'] = highlight.hl
    _env.filters['nl2br'] = nl2br
    _env.filters['commonmark'] = CommonMark.commonmark
    _env.filters['bleach'] = _bleach
    return _env


def render_text(template, **kwargs):
    return jinja_env().get_template(template).render(**kwargs)


def render(template, **kwargs):
    return response.html(render_text(template, **kwargs))
