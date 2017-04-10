import os
from urllib import parse

DEBUG = False


DATABASE_SA = os.environ.get('HEROKU_POSTGRESQL_CHARCOAL_URL')
bits = parse.urlparse(DATABASE_SA)

DATABASE = {
    'user': bits.username,
    'database': bits.path[1:],
    'password': bits.password,
    'host': bits.hostname,
    'port': bits.port,
}

# 8 worker * 10 connections = 80 connectionso
# pgbouncer is setup for 100, so we have a few extra to play with
WORKER_COUNT = 8
