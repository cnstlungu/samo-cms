"""empty message

Revision ID: 6133a3fcd307
Revises: aad10a4e0170
Create Date: 2018-10-14 18:23:03.161781

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6133a3fcd307'
down_revision = 'aad10a4e0170'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('email', mysql.VARCHAR(length=120), nullable=True))
    # ### end Alembic commands ###
