"""edit bet model

Revision ID: 639995d94cdf
Revises: 1ab90e07d2e8
Create Date: 2025-02-22 12:39:03.791972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '639995d94cdf'
down_revision: Union[str, None] = '1ab90e07d2e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bet', 'expected_amount')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bet', sa.Column('expected_amount', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
