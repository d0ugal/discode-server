"""Add lexer_guessed col

Revision ID: d2b740cef7e0
Revises: 43c09ee4ac97
Create Date: 2017-03-28 09:26:58.740440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2b740cef7e0'
down_revision = '43c09ee4ac97'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pastes',
        sa.Column('lexer_guessed', sa.Boolean, default=False),
    )


def downgrade():
    op.drop_column('pastes', 'lexer_guessed')
