import asyncio
import json

from discode_server import db
from discode_server import fragments

connected = set()
notified = set()


async def feed(request, ws):

    global connected
    connected.add(ws)
    print("Open WebSockets: ", len(connected))

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

                paste_id, lineno, comment_id = msg.payload.split(',')
                paste = await db.get_paste(conn, int(paste_id))
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
