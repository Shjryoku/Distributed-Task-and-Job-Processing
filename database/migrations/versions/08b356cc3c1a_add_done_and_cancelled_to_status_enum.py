"""add done and cancelled to status enum

Revision ID: 08b356cc3c1a
Revises: 6478ce04f27b
Create Date: 2026-05-07 21:19:40.419547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08b356cc3c1a'
down_revision: Union[str, Sequence[str], None] = '6478ce04f27b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
