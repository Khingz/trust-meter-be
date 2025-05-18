"""recreate missing revision a1c07d5b0d47

Revision ID: a1c07d5b0d47
Revises: 
Create Date: 2025-05-14 20:08:57.983760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1c07d5b0d47'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
