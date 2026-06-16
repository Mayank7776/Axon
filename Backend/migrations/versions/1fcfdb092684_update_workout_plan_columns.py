"""update_workout_plan_columns

Revision ID: 1fcfdb092684
Revises: 611684825312
Create Date: 2026-06-16 17:35:48.782479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fcfdb092684'
down_revision: Union[str, Sequence[str], None] = '611684825312'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('workout_plans', 'notes', new_column_name='description')
    op.add_column('workout_plans', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('workout_plans', 'is_active')
    op.alter_column('workout_plans', 'description', new_column_name='notes')
