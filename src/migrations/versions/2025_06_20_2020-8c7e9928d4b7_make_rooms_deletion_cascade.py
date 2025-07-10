"""make rooms deletion cascade

Revision ID: 8c7e9928d4b7
Revises: 70152c374304
Create Date: 2025-06-20 20:20:27.386723

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8c7e9928d4b7"
down_revision: Union[str, None] = "70152c374304"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f("rooms_hotel_id_fkey"), "rooms", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_rooms_hotel_id_hotels"),
        "rooms",
        "hotels",
        ["hotel_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_rooms_hotel_id_hotels"), "rooms", type_="foreignkey")
    op.create_foreign_key(op.f("rooms_hotel_id_fkey"), "rooms", "hotels", ["hotel_id"], ["id"])
