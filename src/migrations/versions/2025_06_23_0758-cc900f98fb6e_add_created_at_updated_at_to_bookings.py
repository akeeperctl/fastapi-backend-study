"""add created_at, updated_at to bookings

Revision ID: cc900f98fb6e
Revises: 4203e2fe4163
Create Date: 2025-06-23 07:58:16.531476

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cc900f98fb6e"
down_revision: Union[str, None] = "4203e2fe4163"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "bookings",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("bookings", "updated_at")
    op.drop_column("bookings", "created_at")
