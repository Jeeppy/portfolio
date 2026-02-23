"""add is_alternance and experience_id to education

Revision ID: aaa0815b4958
Revises: 8e7c653cc854
Create Date: 2026-02-22 16:30:42.108616

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aaa0815b4958"
down_revision: str | Sequence[str] | None = "8e7c653cc854"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("education", recreate="always") as batch_op:
        batch_op.add_column(
            sa.Column(
                "is_alternance", sa.Boolean(), nullable=False, server_default=sa.false()
            )
        )
        batch_op.add_column(sa.Column("experience_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_education_experience_id", "experience", ["experience_id"], ["id"]
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("education", recreate="always") as batch_op:
        batch_op.drop_constraint("fk_education_experience_id", type_="foreignkey")
        batch_op.drop_column("experience_id")
        batch_op.drop_column("is_alternance")
