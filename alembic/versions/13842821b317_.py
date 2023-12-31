"""empty message

Revision ID: 13842821b317
Revises: 38689e06e88b
Create Date: 2023-12-21 16:33:58.842389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13842821b317'
down_revision: Union[str, None] = '38689e06e88b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
                    sa.Column('message_id', sa.Integer(), nullable=False),
                    sa.Column('from_id', sa.Integer(), nullable=False),
                    sa.Column('to_id', sa.Integer(), nullable=False),
                    sa.Column('message', sa.String(), nullable=True),
                    sa.Column('date', sa.TIMESTAMP(), nullable=True),
                    sa.PrimaryKeyConstraint('message_id'),
                    sa.UniqueConstraint('message_id')
    )
    op.create_unique_constraint(None, 'friend', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'friend', type_='unique')
    op.drop_table('message')
    # ### end Alembic commands ###
