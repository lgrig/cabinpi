"""transactions table

Revision ID: d243f644b1cb
Revises: 3e52c45745f9
Create Date: 2018-11-28 04:09:39.378290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd243f644b1cb'
down_revision = '3e52c45745f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.Column('value_numeric', sa.Float(), nullable=True),
    sa.Column('value_enum', sa.String(length=128), nullable=True),
    sa.Column('ts', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    # ### end Alembic commands ###
