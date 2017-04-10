import os
from urllib import parse

DEBUG = False


DATABASE_SA = os.environ.get('HEROKU_POSTGRESQL_CHARCOAL_URL')

PG_BOUNCER = os.environ.get('HEROKU_POSTGRESQL_CHARCOAL_URL_PGBOUNCER')
bits = parse.urlparse(PG_BOUNCER)

DATABASE = {
    'user': bits.username,
    'database': bits.path[1:],
    'password': bits.password,
    'host': bits.hostname,
    'port': bits.port,
    'maxsize': 4,
}

# 4 worker * 5 connections = 16 connectionso
# 20 is the limit on Heroku, this leaves room for error and/or other processes
# (like migrations which use 1)
WORKER_COUNT = 4
