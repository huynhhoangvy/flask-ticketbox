"""empty message

Revision ID: 0b92dc98065a
Revises: f7b6a82f8830
Create Date: 2019-07-07 00:06:46.888654

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0b92dc98065a'
down_revision = 'f7b6a82f8830'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=999), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('birthdate', sa.DateTime(), nullable=True),
    sa.Column('gender', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('profile')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=999), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('birthdate', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('gender', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='profile_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='profile_pkey')
    )
    op.drop_table('profiles')
    # ### end Alembic commands ###
