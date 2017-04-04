"""Add lexer col, allow dupes

Revision ID: 90f49530d6c0
Revises: e78f9d818988
Create Date: 2017-03-23 07:53:16.831215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90f49530d6c0'
down_revision = 'e78f9d818988'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pastes',
        sa.Column('lexer', sa.String(60), nullable=True)
    )
    op.drop_constraint("pastes_sha_key", "pastes")


def downgrade():
    op.create_unique_constraint("pastes_sha_key", "pastes", ["sha"])
    op.drop_column('pastes', 'lexer')
