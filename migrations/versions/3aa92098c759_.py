"""empty message

Revision ID: 3aa92098c759
Revises: f8e46ecd13c8
Create Date: 2019-07-04 23:23:08.879046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aa92098c759'
down_revision = 'f8e46ecd13c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=999), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=True),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('event_url', sa.String(), nullable=True),
    sa.Column('is_private', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rating_users',
    sa.Column('rater_id', sa.Integer(), nullable=False),
    sa.Column('target_user_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['rater_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['target_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('rater_id', 'target_user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rating_users')
    op.drop_table('events')
    op.drop_table('users')
    # ### end Alembic commands ###