"""empty message

Revision ID: 1125c372122d
Revises: 94e4ab02bdaa
Create Date: 2022-05-12 17:13:25.277799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1125c372122d'
down_revision = '94e4ab02bdaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart_items', sa.Column('quantity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart_items', 'quantity')
    # ### end Alembic commands ###
