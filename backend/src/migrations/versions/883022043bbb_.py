"""empty message

Revision ID: 883022043bbb
Revises: 8f99427989dc
Create Date: 2025-09-22 23:46:02.953827

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "883022043bbb"
down_revision: Union[str, Sequence[str], None] = "8f99427989dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
