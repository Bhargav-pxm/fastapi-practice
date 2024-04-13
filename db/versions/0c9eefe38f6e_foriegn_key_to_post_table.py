"""foriegn-key to post table

Revision ID: 0c9eefe38f6e
Revises: 70bb91870103
Create Date: 2024-04-12 11:04:50.235225

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0c9eefe38f6e"
down_revision: Union[str, None] = "70bb91870103"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
    )
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    ),


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
