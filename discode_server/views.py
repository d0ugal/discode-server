import asyncio
import pathlib

from sanic import exceptions
from sanic import response
import jinja2
import sanic

from discode_server.utils import baseconv
from discode_server.utils import highlight
from discode_server.utils import limiter
from discode_server import db
from discode_server import forms

bp = sanic.Blueprint('paste')

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(pathlib.Path('.') / "templates"))
)
env.filters['highlight'] = highlight.hl


def _render(template, **kwargs):
    return response.html(env.get_template(template).render(**kwargs))


@bp.listener('after_server_start')
async def delete_expired(app, loop):
    while True:
        async with app.config.DB.acquire() as conn:
            await db.delete_expired(conn)
        await asyncio.sleep(60 * 60)


@bp.get('/')
async def index(request):
    paste_form = forms.NewPasteForm()
    return _render('index.html', paste_form=paste_form)


@bp.post('/')
@limiter.limiter("12/minute")
async def create_paste(request):

    if request.form:
        paste_form = forms.NewPasteForm(request.form)
    else:
        if request.body:
            contents = request.body.decode("utf-8")
        else:
            contents = ''
        paste_form = forms.NewPasteForm(contents=contents)

    if not paste_form.validate():
        if request.form:
            return _render('index.html', paste_form=paste_form)
        else:
            return response.json(paste_form.errors)

    async with request.app.config.DB.acquire() as conn:
        contents = paste_form.contents.data
        lexer = paste_form.language.data
        paste = await db.create(conn, contents, lexer)

    request['session'].setdefault('pastes', [])
    request['session']['pastes'].append(paste.decimal_id)

    url = request.app.url_for('paste.show_paste', paste_id=paste.id)

    if not request.form:
        return response.json({"paste": url})
    return response.redirect(url)


@bp.get('/<paste_id:[A-Za-z0-9]+>')
async def show_paste(request, paste_id):
    comment_form = forms.CommentForm()
    paste_id = paste_id.upper()
    paste_id = baseconv.base62.to_decimal(paste_id)
    async with request.app.config.DB.acquire() as conn:
        paste = await db.get_paste(conn, paste_id)
    return _render('paste.html', paste=paste, comment_form=comment_form)


@bp.post('/<paste_id:[A-Za-z0-9]+>')
async def create_comment(request, paste_id):
    if not request.form:
        raise exceptions.InvalidUsage("Post a form yo")

    url_id = paste_id
    paste_id = paste_id.upper()
    paste_id = baseconv.base62.to_decimal(paste_id)
    comment_form = forms.CommentForm(request.form)

    if not comment_form.validate():
        raise exceptions.InvalidUsage("bad datas")

    lineno = comment_form.line.data

    async with request.app.config.DB.acquire() as conn:
        comment = await db.create_comment(
            conn, paste_id, comment_form.line.data,
            comment_form.contents.data)

    request['session'].setdefault('comments', [])
    request['session']['comments'].append(comment.id)

    url = request.app.url_for('paste.show_paste', paste_id=url_id)
    return response.redirect(f"{url}#L{lineno}")


@bp.get('/<paste_id:[A-Za-z0-9]+>/raw')
async def show_raw(request, paste_id):
    paste_id = paste_id.upper()
    paste_id = baseconv.base62.to_decimal(paste_id)
    async with request.app.config.DB.acquire() as conn:
        paste = await db.get_paste(conn, paste_id)
    return response.text(paste.contents)


@bp.get('/_list')
async def list_pastes(request):
    async with request.app.config.DB.acquire() as conn:
        pastes = await db.get_pastes(conn)
    return _render('list.html', pastes=pastes, url_for=request.app.url_for)
