import pytest

from discode_server import db as dbapi


@pytest.mark.asyncio
async def test_get_paste(db):
    async with db.acquire() as conn:
        with pytest.raises(dbapi.PasteNotFound):
            await dbapi.get_paste(conn, 1)
