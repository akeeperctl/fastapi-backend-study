"""make email unique

Revision ID: 70152c374304
Revises: 877da523de51
Create Date: 2025-06-18 09:46:36.744118

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "70152c374304"
down_revision: Union[str, None] = "877da523de51"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(op.f("uq_users_email"), "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_users_email"), "users", type_="unique")
