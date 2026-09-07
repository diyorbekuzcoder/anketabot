"""Add profile fields to Admin

Revision ID: e53b47c941df
Revises: dd7febe1cec5
Create Date: 2026-09-07 22:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e53b47c941df'
down_revision: Union[str, None] = 'dd7febe1cec5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('admins', sa.Column('profile_picture', sa.String(), nullable=True))
    op.add_column('admins', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('admins', sa.Column('telegram_id', sa.String(), nullable=True))
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_admins_telegram_id', ['telegram_id'])


def downgrade() -> None:
    with op.batch_alter_table('admins', schema=None) as batch_op:
        batch_op.drop_constraint('uq_admins_telegram_id', type_='unique')
        batch_op.drop_column('telegram_id')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('profile_picture')
