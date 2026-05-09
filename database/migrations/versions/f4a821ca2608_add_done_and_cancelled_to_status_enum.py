"""add done and cancelled to status enum

Revision ID: f4a821ca2608
Revises: 08b356cc3c1a
Create Date: 2026-05-07 21:19:54.661182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4a821ca2608'
down_revision: Union[str, Sequence[str], None] = '08b356cc3c1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE status ADD VALUE IF NOT EXISTS 'DONE'")
    op.execute("ALTER TYPE status ADD VALUE IF NOT EXISTS 'CANCELLED'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
