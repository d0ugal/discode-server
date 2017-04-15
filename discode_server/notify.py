import asyncio
import json

from discode_server import db
from discode_server import fragments
from discode_server.utils import baseconv

connected = set()
notified = set()


async def feed(request, ws, paste_id):

    global connected, notified

    connected.add(ws)
    print("Open WebSockets: ", len(connected))
    paste_id = baseconv.base36.to_decimal(paste_id)

    try:
        while True:
            if not ws.open:
                return

            async with request.app.config.DB.acquire() as conn:
                await conn.execute(f"LISTEN channel")
                try:
                    msg = await asyncio.wait_for(
                            conn.connection.notifies.get(), 1)
                except asyncio.TimeoutError:
                    continue

                if not ws.open:
                    return

                fingerprint = ws.remote_address, msg.payload
                if fingerprint in notified:
                    continue
                notified.add(fingerprint)

                p_id, lineno, comment_id = msg.payload.split(',')
                p_id = int(p_id)

                if paste_id != p_id:
                    continue

                paste = await db.get_paste(conn, int(p_id))
                html = fragments.comment_row(lineno,
                                             paste.comments[int(lineno)])
                data = json.dumps({
                    "html": html,
                    "lineno": lineno,
                    "paste_id": paste.id,
                    "comment_id": comment_id,
                })
                await ws.send(data)
    finally:
        connected.remove(ws)
        print("Open WebSockets: ", len(connected))
