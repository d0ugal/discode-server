import collections
import datetime
import hashlib
import logging

from sanic import exceptions
import aiopg.sa
import sqlalchemy as sa

from discode_server.utils import baseconv
from discode_server.utils import highlight

log = logging.getLogger(__file__)
meta = sa.MetaData()

paste = sa.Table(
    'pastes', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('contents', sa.Text(), nullable=False),
    sa.Column('created_on', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('sha', sa.String(64), nullable=False),
    sa.Column('lexer', sa.String(60), nullable=True),
    sa.Column('lexer_guessed', sa.Boolean, default=False),
)

comment = sa.Table(
    'comments', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('paste_id', sa.Integer, sa.ForeignKey("pastes.id"),
              nullable=False),
    sa.Column('line', sa.Integer, nullable=False),
    sa.Column('contents', sa.Text(), nullable=False),
    sa.Column('created_on', sa.DateTime, default=datetime.datetime.utcnow),
)


class Paste:
    def __init__(self, record, comments=None):
        self._record = record
        self.comments = collections.defaultdict(list)

        if not comments:
            return
        for comment in comments:
            self.comments[comment.line].append(comment.contents)

    @property
    def id(self):
        return baseconv.base36.from_decimal(self._record.id)

    @property
    def decimal_id(self):
        return self._record.id

    @property
    def contents(self):
        return self._record.contents

    @property
    def lexer(self):
        return self._record.lexer

    @property
    def created_on(self):
        return self._record.created_on


class Comment:
    def __init__(self, record):
        self._record = record

    @property
    def id(self):
        return self._record.id

    @property
    def contents(self):
        return self._record.contents

    @property
    def line(self):
        return self._record.line


class PasteNotFound(exceptions.NotFound):
    pass


async def create_engine(db_config, loop):
    return await aiopg.sa.create_engine(
        **db_config,
        loop=loop
    )


async def get_paste(conn, paste_id):
    query = sa.select([paste]).where(paste.c.id == paste_id)
    result = await conn.execute(query)
    p = await result.first()
    comments = await get_comments(conn, paste_id)
    if not p:
        raise PasteNotFound("Paste Not Found")
    return Paste(p, comments)


async def get_pastes(conn):
    query = sa.select([paste.c.id, paste.c.created_on])
    result = await conn.execute(query)
    pastes = await result.fetchall()
    if not pastes:
        raise PasteNotFound("Paste Not Found")
    return [Paste(r) for r in pastes]


async def delete_expired(conn):
    log.info("Deleteing expired pastes")
    days = 30
    delete_after = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    await conn.execute(paste.delete().where(paste.c.created_on < delete_after))


async def create_comment(conn, paste_id, line, contents):
    result = await conn.execute(comment.insert().values(
        paste_id=paste_id, line=line, contents=contents))
    record = await result.fetchone()
    await conn.execute(f"NOTIFY channel, %s", f"{paste_id},{line},{record.id}")

    return record


async def get_comments(conn, paste_id):
    query = sa.select([comment]).where(comment.c.paste_id == paste_id)
    result = await conn.execute(query)
    comments = await result.fetchall()
    return [Comment(c) for c in comments]


async def create(conn, contents, lexer, created_on=None):
    sha = hashlib.sha256(contents.encode('utf-8')).hexdigest()

    lexer, detected = highlight.guess(contents, lexer)

    values = {
        'contents': contents,
        'sha': sha,
        'lexer': lexer,
        'lexer_guessed': detected,
    }

    if created_on is not None:
        values['created_on'] = created_on

    result = await conn.execute(paste.insert().values(**values))
    record = await result.fetchone()

    if not record:
        raise Exception("whelp")

    return Paste(record)
