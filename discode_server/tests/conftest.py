import os

from alembic import config
from alembic import command
import pytest

from discode_server import app as app_
from discode_server import db as dbapi


@pytest.fixture(scope='function')
def app():
    os.environ['DISCODE_CONFIG'] = 'discode_server/config/test.py'
    command.upgrade(config.Config('alembic.ini'), 'head')
    app = app_.create_app()
    yield app
    command.downgrade(config.Config('alembic.ini'), 'base')


@pytest.fixture(scope='function')
def test_client(app):
    return app.test_client


@pytest.fixture(scope='function')
def db(app, event_loop):
    return event_loop.run_until_complete(
        dbapi.create_engine(app.config.DATABASE, loop=event_loop))
