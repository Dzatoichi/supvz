"""add scheduled_shift_id to shift_penalties table

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2026-01-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6g7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'shift_penalties',
        sa.Column('scheduled_shift_id', sa.Integer(), nullable=False)
    )
    op.create_index(
        op.f('ix_shift_penalties_scheduled_shift_id'),
        'shift_penalties',
        ['scheduled_shift_id'],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_shift_penalties_scheduled_shift_id'), table_name='shift_penalties')
    op.drop_column('shift_penalties', 'scheduled_shift_id')

