"""add foreign-key to posts table

Revision ID: 1df30cdc4ea5
Revises: 34c2fbaec92c
Create Date: 2022-12-02 06:52:12.090475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1df30cdc4ea5'
down_revision = '34c2fbaec92c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",
        local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('post', 'owner_id')
    pass
