"""remove is_admin from users

Revision ID: 06240072f9ef
Revises: a857420051eb
Create Date: 2026-04-15 17:11:07.209022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06240072f9ef'
down_revision: Union[str, Sequence[str], None] = 'a857420051eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('users', 'is_admin')

def downgrade():
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
