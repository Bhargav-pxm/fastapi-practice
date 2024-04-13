"""add content column to post table

Revision ID: 11efcd3721bb
Revises: 5a3d488ec7f7
Create Date: 2024-04-11 17:59:56.372505

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "11efcd3721bb"
down_revision: Union[str, None] = "5a3d488ec7f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
