"""first commit

Revision ID: 4682a5d4f74e
Revises: 
Create Date: 2022-04-16 13:51:35.845015

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4682a5d4f74e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(50), unique=True, index=True),
        sa.Column('description', sa.String(200)),
    )


def downgrade():
    op.drop_table('items')
