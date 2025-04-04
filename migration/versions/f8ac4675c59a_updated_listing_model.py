"""Updated listing model

Revision ID: f8ac4675c59a
Revises: 9ae4ae35da73
Create Date: 2025-03-25 17:50:12.266994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8ac4675c59a'
down_revision: Union[str, None] = '9ae4ae35da73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('listings', sa.Column('listing_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('listings', 'listing_url')
    # ### end Alembic commands ###
