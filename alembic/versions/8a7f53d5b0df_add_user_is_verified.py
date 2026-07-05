"""Add is_verified column to users table

Revision ID: 8a7f53d5b0df
Revises: 67fdec71859d
Create Date: 2026-07-03 15:35:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8a7f53d5b0df'
down_revision = '67fdec71859d'
branch_labels = None
depend_on = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column('users', 'is_verified')
