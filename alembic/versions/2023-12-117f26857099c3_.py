"""empty message

Revision ID: 7f26857099c3
Revises: 6e09a6b22ab7
Create Date: 2023-12-11 17:56:05.657395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f26857099c3'
down_revision: Union[str, None] = '6e09a6b22ab7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profile_image', sa.LargeBinary(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'profile_image')
    # ### end Alembic commands ###