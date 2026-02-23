"""make appointment subject and message nullable

Revision ID: 363f4e5a1161
Revises: 141827b29fdc
Create Date: 2026-02-23 09:26:07.085932

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "363f4e5a1161"
down_revision: str | Sequence[str] | None = "141827b29fdc"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("appointment", recreate="always") as batch_op:
        batch_op.alter_column(
            "subject", existing_type=sa.String(length=200), nullable=True
        )
        batch_op.alter_column(
            "message", existing_type=sa.String(length=2000), nullable=True
        )


def downgrade() -> None:
    with op.batch_alter_table("appointment", recreate="always") as batch_op:
        batch_op.alter_column(
            "subject", existing_type=sa.String(length=200), nullable=False
        )
        batch_op.alter_column(
            "message", existing_type=sa.String(length=2000), nullable=False
        )
