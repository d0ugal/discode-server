import datetime

import pytest

from discode_server import db as dbapi


@pytest.mark.asyncio
async def test_get_paste(db):
    async with db.acquire() as conn:
        with pytest.raises(dbapi.PasteNotFound):
            await dbapi.get_paste(conn, 1)


@pytest.mark.asyncio
async def test_create_paste(db):
    async with db.acquire() as conn:
        await dbapi.create(conn, "PASTE CONTENTS", "python")
        paste = await dbapi.get_paste(conn, 1)
        assert paste.id == '1'
        assert paste.decimal_id == 1
        assert paste.contents == "PASTE CONTENTS"
        assert paste.lexer == "python"
        assert paste.created_on.date() == datetime.date.today()


@pytest.mark.asyncio
async def test_get_pastes(db):
    async with db.acquire() as conn:
        await dbapi.create(conn, "PASTE 1 CONTENTS", "python")
        await dbapi.create(conn, "PASTE 2 CONTENTS", "python")
        pastes = await dbapi.get_pastes(conn)
        assert ["1", "2"] == [p.id for p in pastes]


@pytest.mark.asyncio
async def test_delete_expired(db):
    async with db.acquire() as conn:
        old = datetime.datetime.now() - datetime.timedelta(days=60)
        await dbapi.create(conn, "PASTE 1 CONTENTS", "python", old)
        await dbapi.create(conn, "PASTE 2 CONTENTS", "python")
        pastes = await dbapi.get_pastes(conn)
        assert ["1", "2"] == [p.id for p in pastes]
        await dbapi.delete_expired(conn)
        pastes = await dbapi.get_pastes(conn)
        assert ["2"] == [p.id for p in pastes]
