"""add shift_penalties table

Revision ID: a1b2c3d4e5f6
Revises: 003f10aa4b39
Create Date: 2026-01-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '003f10aa4b39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'shift_penalties',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('type', sa.String(length=16), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('penalty_minutes', sa.Integer(), nullable=True, comment='Количество минут опоздания/раннего ухода'),
        sa.Column('penalty_points', sa.Integer(), nullable=False, default=0, comment='Штрафные баллы'),
        sa.Column('detected_at', sa.DateTime(timezone=False), server_default=sa.func.now(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=False), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=False), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("type IN ('late_start', 'early_end', 'miss', 'other')", name='check_penalty_type'),
    )
    op.create_index(op.f('ix_shift_penalties_type'), 'shift_penalties', ['type'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_shift_penalties_type'), table_name='shift_penalties')
    op.drop_table('shift_penalties')

