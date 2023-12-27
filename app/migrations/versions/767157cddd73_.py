"""empty message

Revision ID: 767157cddd73
Revises: 7288258e2971
Create Date: 2023-12-26 01:04:28.675173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '767157cddd73'
down_revision: Union[str, None] = '7288258e2971'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('error', sa.Column('sleep_time', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('error', 'sleep_time')
    # ### end Alembic commands ###
