"""Add paste sha col

Revision ID: e78f9d818988
Revises: d3dad4db468d
Create Date: 2017-03-22 19:20:28.949724

"""
import hashlib

from alembic import op
import sqlalchemy as sa
from sqlalchemy import sql


# revision identifiers, used by Alembic.
revision = 'e78f9d818988'
down_revision = 'd3dad4db468d'
branch_labels = None
depends_on = None

meta = sa.MetaData()

def upgrade():

    conn = op.get_bind()

    op.add_column('pastes',
        sa.Column('sha', sa.String(64), nullable=True, unique=True),
    )
    op.drop_constraint("pastes_contents_key", "pastes")

    pastes = sa.Table(
        'pastes', meta,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('created_on', sa.DateTime),
        sa.Column('sha', sa.String(32), nullable=False, unique=True)
    )

    for paste in conn.execute(pastes.select()):
        sha = hashlib.sha256(paste.contents.encode('utf-8')).hexdigest()
        conn.execute(pastes.update().where(pastes.c.id == paste.id).values(sha=sha))

    op.alter_column('pastes', 'sha', nullable=False)


def downgrade():
    op.drop_column('pastes', 'sha')
    op.create_unique_constraint("pastes_contents_key", "pastes", ["contents"])
