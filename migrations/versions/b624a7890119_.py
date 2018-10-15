"""empty message

Revision ID: b624a7890119
Revises: 6133a3fcd307
Create Date: 2018-10-15 00:01:01.303890

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b624a7890119'
down_revision = '6133a3fcd307'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('deleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'deleted')
    # ### end Alembic commands ###
