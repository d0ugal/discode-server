import datetime
import time
import uuid

from sqlalchemy.dialects import postgresql as pg
import sqlalchemy as sa
import psycopg2

meta = sa.MetaData()

session = sa.Table(
    'sessions', meta,
    sa.Column('id', sa.String(64), primary_key=True),
    sa.Column('data', pg.JSON()),
    sa.Column('created_on', sa.DateTime, default=datetime.datetime.utcnow),
)

COOKIE_NAME = "SESSION"
EXPIRY = 2592000


def _calculate_expires(expiry):
    expires = time.time() + expiry
    return time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expires))


def _delete_cookie(request, response):
    response.cookies[COOKIE_NAME] = request['session']['id']
    response.cookies[COOKIE_NAME]['expires'] = 0
    response.cookies[COOKIE_NAME]['max-age'] = 0


def _set_cookie_expiration(request, response):
    response.cookies[COOKIE_NAME] = request['session']['id']
    response.cookies[COOKIE_NAME]['expires'] = _calculate_expires(EXPIRY)
    response.cookies[COOKIE_NAME]['max-age'] = EXPIRY
    response.cookies[COOKIE_NAME]['httponly'] = True


async def add_to_request(request):

    sesh_id = request.cookies.get(COOKIE_NAME)
    sesh = {'id': sesh_id or uuid.uuid4().hex}

    request['session'] = sesh

    if sesh_id:
        query = sa.select([session]).where(session.c.id == sesh_id)
        async with request.app.config.DB.acquire() as conn:
            result = await conn.execute(query)
            s = await result.first()
            if s:
                sesh = s.data

    request['session'] = sesh


async def save_session(request, response):

    if 'session' not in request:
        return

    if response is None:
        return

    sesh = request['session']
    sesh_id = sesh['id']

    if set(sesh.keys()) == set(("id", )):
        return
        async with request.app.config.DB.acquire() as conn:
            await conn.execute(session.delete().where(session.c.id == sesh_id))
        # delete cookie
        return

    async with request.app.config.DB.acquire() as conn:
        insert = session.insert().values(id=sesh_id, data=sesh)
        update = session.update().where(session.c.id == sesh_id
                                        ).values(data=sesh)
        try:
            await conn.execute(insert)
        except psycopg2.IntegrityError:
            await conn.execute(update)

    _set_cookie_expiration(request, response)
