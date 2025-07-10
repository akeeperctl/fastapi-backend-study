"""make booking deletion cascade

Revision ID: 8cd453ec388c
Revises: 52aac8405a5e
Create Date: 2025-06-20 21:45:00.163420

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8cd453ec388c"
down_revision: Union[str, None] = "52aac8405a5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        op.f("fk_bookings_room_id_rooms"), "bookings", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_bookings_user_id_users"), "bookings", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_bookings_room_id_rooms"),
        "bookings",
        "rooms",
        ["room_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_bookings_user_id_users"),
        "bookings",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_bookings_user_id_users"), "bookings", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_bookings_room_id_rooms"), "bookings", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_bookings_user_id_users"), "bookings", "users", ["user_id"], ["id"]
    )
    op.create_foreign_key(
        op.f("fk_bookings_room_id_rooms"), "bookings", "rooms", ["room_id"], ["id"]
    )
