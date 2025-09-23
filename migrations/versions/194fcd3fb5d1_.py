"""empty message

Revision ID: 194fcd3fb5d1
Revises: 2a842741f55b
Create Date: 2025-09-22 18:06:59.509482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '194fcd3fb5d1'
down_revision: Union[str, Sequence[str], None] = '2a842741f55b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
