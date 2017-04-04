"""Create paste table

Revision ID: 1bc2e4a12715
Revises:
Create Date: 2017-03-21 19:48:58.424921

"""
import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bc2e4a12715'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pastes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('contents', sa.Text(), nullable=False, unique=True),
        sa.Column('created_on', sa.DateTime, default=datetime.datetime.utcnow)
    )


def downgrade():
    op.drop_table('pastes')
