"""add avg_rating

Revision ID: 4f51ec1f90e6
Revises: dcc251fbb9c8
Create Date: 2022-03-20 14:56:17.016938

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '4f51ec1f90e6'
down_revision = 'dcc251fbb9c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('avg_rating', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'avg_rating')
    # ### end Alembic commands ###