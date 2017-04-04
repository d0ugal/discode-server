import os

from alembic import config
from alembic import command
import pytest

from discode_server import app as app_


@pytest.fixture()
def app():
    os.environ['DISCODE_CONFIG'] = 'discode_server/config/test.py'
    command.upgrade(config.Config('alembic.ini'), 'head')
    yield app_.create_app()
    command.downgrade(config.Config('alembic.ini'), 'base')


@pytest.fixture()
def test_client(app):
    return app.test_client
