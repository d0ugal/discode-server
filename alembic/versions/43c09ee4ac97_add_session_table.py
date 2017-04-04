"""Add session table

Revision ID: 43c09ee4ac97
Revises: 90f49530d6c0
Create Date: 2017-03-28 08:37:59.490925

"""
from alembic import op
from sqlalchemy.dialects import postgresql as pg
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43c09ee4ac97'
down_revision = '90f49530d6c0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sessions',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('data', pg.JSON()),
        sa.Column('created_on', sa.DateTime),
    )


def downgrade():
    op.drop_table('sessions')
