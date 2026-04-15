"""add role to users

Revision ID: a857420051eb
Revises: 4191a362d8ed
Create Date: 2026-04-15 16:29:30.490597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a857420051eb'
down_revision: Union[str, Sequence[str], None] = '4191a362d8ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('users', sa.Column('role', sa.String(), nullable=False, server_default='user'))

def downgrade():
    op.drop_column('users', 'role')