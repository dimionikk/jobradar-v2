"""add is_active to vacancy

Revision ID: 6da0ae1217bb
Revises: 339a808d03b8
Create Date: 2026-06-22 11:25:17.134764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6da0ae1217bb'
down_revision: Union[str, Sequence[str], None] = '339a808d03b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('vacancies', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')))


def downgrade() -> None:
    op.drop_column('vacancies', 'is_active')
