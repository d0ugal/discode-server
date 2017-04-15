import os

import raven
import sanic

from discode_server import db
from discode_server import notify
from discode_server import views
from discode_server.config import base_config
from discode_server import session


def create_app():
    app = sanic.Sanic(__name__)
    app.blueprint(views.bp)
    app.add_websocket_route(notify.feed, '/_notify/<paste_id:[A-Za-z0-9]+>')
    app.config.from_object(base_config)
    if 'DISCODE_CONFIG' in os.environ:
        app.config.from_envvar('DISCODE_CONFIG')
    app.static('/static', './static')

    app.middleware('request')(session.add_to_request)
    app.middleware('response')(session.save_session)

    sentry_dsn = app.config['SENTRY_DSN']
    sentry_client = raven.Client(sentry_dsn)

    @app.exception(Exception)
    def handle_exceptions(request, exception):
        sentry_client.captureException()

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

    print("-=- ENV -=-")
    for key, val in os.environ.items():
        print(f"{key}={val!r}")

    print("-=- CONFIG -=-")
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
