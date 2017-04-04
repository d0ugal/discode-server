"""Create comment table

Revision ID: d3dad4db468d
Revises: 1bc2e4a12715
Create Date: 2017-03-22 11:17:45.042987

"""
import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3dad4db468d'
down_revision = '1bc2e4a12715'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('paste_id', sa.Integer, sa.ForeignKey("pastes.id"), nullable=False),
        sa.Column('line', sa.Integer, nullable=False),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('created_on', sa.DateTime, default=datetime.datetime.utcnow),
    )


def downgrade():
    op.drop_table('comments')
