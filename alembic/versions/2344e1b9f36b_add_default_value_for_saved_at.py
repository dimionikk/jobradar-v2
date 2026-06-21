"""add default value for saved_at

Revision ID: 2344e1b9f36b
Revises: 25b5ad433aa3
Create Date: 2026-06-21 16:21:32.400618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2344e1b9f36b'
down_revision: Union[str, Sequence[str], None] = '25b5ad433aa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('saved_vacancies', 'saved_at', server_default=sa.func.now())


def downgrade() -> None:
    op.alter_column('saved_vacancies', 'saved_at', server_default=None)
