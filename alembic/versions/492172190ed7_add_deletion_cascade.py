"""Add deletion cascade

Revision ID: 492172190ed7
Revises: d2b740cef7e0
Create Date: 2017-06-06 14:20:14.736911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '492172190ed7'
down_revision = 'd2b740cef7e0'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("comments") as batch_op:
        batch_op.drop_constraint(
            "comments_paste_id_fkey", type_="foreignkey")
    op.create_foreign_key(
        "comments_paste_id_fkey", "comments", "pastes",
        ["paste_id"], ["id"], ondelete="CASCADE")


def downgrade():
    with op.batch_alter_table("comments") as batch_op:
        batch_op.drop_constraint(
            "comments_paste_id_fkey", type_="foreignkey")
    op.create_foreign_key(
        "comments_paste_id_fkey", "comments", "pastes",
        ["paste_id"], ["id"])
