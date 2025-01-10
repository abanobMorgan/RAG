"""add assets name into assets class

Revision ID: f65d49d1dd49
Revises: 7ff83dfc05ee
Create Date: 2025-01-06 17:55:49.568715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f65d49d1dd49'
down_revision: Union[str, None] = '7ff83dfc05ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assets', sa.Column('asset_name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('assets', 'asset_name')
    # ### end Alembic commands ###
