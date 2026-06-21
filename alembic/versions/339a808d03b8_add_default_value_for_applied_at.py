"""add default value for applied_at

Revision ID: 339a808d03b8
Revises: 2344e1b9f36b
Create Date: 2026-06-21 17:29:18.247832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '339a808d03b8'
down_revision: Union[str, Sequence[str], None] = '2344e1b9f36b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('applications', 'applied_at', server_default=sa.func.now())


def downgrade() -> None:
    op.alter_column('applications', 'applied_at', server_default=None)