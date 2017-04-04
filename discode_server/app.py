import os
import sys
import traceback

import sanic
from sanic import response

from discode_server import db
from discode_server import notify
from discode_server import views
from discode_server.config import base_config
from discode_server import session


def create_app():
    app = sanic.Sanic(__name__)
    app.blueprint(views.bp)
    app.add_websocket_route(notify.feed, '/_notify')
    app.config.from_object(base_config)
    if 'DISCODE_CONFIG' in os.environ:
        app.config.from_envvar('DISCODE_CONFIG')
    app.static('/static', './static')

    app.middleware('request')(session.add_to_request)
    app.middleware('response')(session.save_session)

    @app.exception(Exception)
    def errors(request, exception):
        traceback.print_exc(file=sys.stdout)
        return response.text(":-(", status=500)

    @app.listener('before_server_start')
    async def setup_connection(app, loop):

        app.config.DB = await db.create_engine(
            app.config.DATABASE,
            loop=loop
        )

    @app.listener('after_server_stop')
    async def close_connection(app, loop):
        app.config.DB.close()
        await app.config.DB.wait_closed()

    return app


def run():
    port = int(os.environ.get('PORT', 8000))
    app = create_app()

    for key, val in app.config.items():
        if key == 'LOGO':
            continue
        print(f"{key}={val!r}")

    app.run(
        host="0.0.0.0",
        port=port,
        workers=app.config.WORKER_COUNT,
        debug=app.config.DEBUG
    )
