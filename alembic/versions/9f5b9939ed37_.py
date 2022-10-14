"""empty message

Revision ID: 9f5b9939ed37
Revises: 5d9eccb376e6
Create Date: 2022-05-05 18:39:29.092225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f5b9939ed37'
down_revision = '5d9eccb376e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('category',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('name', sa.String(length=50), nullable=True),
    # sa.PrimaryKeyConstraint('id')
    # )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.drop_table('category')
    # ### end Alembic commands ###