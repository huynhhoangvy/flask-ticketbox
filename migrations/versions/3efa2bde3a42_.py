"""empty message

Revision ID: 3efa2bde3a42
Revises: c583cca09508
Create Date: 2019-07-06 23:45:57.217956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3efa2bde3a42'
down_revision = 'c583cca09508'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('purchases', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('purchases', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###