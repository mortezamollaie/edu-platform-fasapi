"""role permission migration

Revision ID: e2d826a341cb
Revises: 71696931b9ad
Create Date: 2025-07-22 11:16:32.189538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2d826a341cb'
down_revision: Union[str, Sequence[str], None] = '71696931b9ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('user_role')
    op.drop_column('permission')
    op.drop_column('roles')
    op.drop_column('permissions')


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
