"""rename col filetype as mimetype[D

Revision ID: f2c9b9b2f56d
Revises: eb06fc2a6a06
Create Date: 2026-06-15 14:23:34.066169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f2c9b9b2f56d'
down_revision: Union[str, Sequence[str], None] = 'eb06fc2a6a06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('files', sa.Column('mimetype', sa.String(length=255), nullable=True, comment='文件类型'))
    op.execute("UPDATE files SET mimetype = filetype")
    op.alter_column('files', 'mimetype', nullable=False)
    op.drop_column('files', 'filetype')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('files', sa.Column('filetype', sa.String(length=255), nullable=True, comment='文件类型'))
    op.execute("UPDATE files SET filetype = mimetype")
    op.alter_column('files', 'filetype', nullable=False)
    op.drop_column('files', 'mimetype')
