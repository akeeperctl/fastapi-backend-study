"""add bookings

Revision ID: 38f5c44b08e6
Revises: 8c7e9928d4b7
Create Date: 2025-06-20 20:34:21.174442

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "38f5c44b08e6"
down_revision: Union[str, None] = "8c7e9928d4b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.DateTime(), nullable=False),
        sa.Column("date_to", sa.DateTime(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], name=op.f("fk_bookings_room_id_rooms")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_bookings_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_bookings")),
    )


def downgrade() -> None:
    op.drop_table("bookings")
