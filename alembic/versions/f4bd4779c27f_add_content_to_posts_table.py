"""add content to posts table

Revision ID: f4bd4779c27f
Revises: dd4c6b4a68a9
Create Date: 2022-12-02 06:15:58.455049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4bd4779c27f'
down_revision = 'dd4c6b4a68a9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
