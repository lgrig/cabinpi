"""empty message

Revision ID: 4911128bb4a1
Revises: 3e52c45745f9
Create Date: 2018-12-02 22:07:09.527142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4911128bb4a1'
down_revision = '3e52c45745f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gpio_task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('status_enum', sa.String(length=128), nullable=True),
    sa.Column('status_numeric', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gpio_task_name'), 'gpio_task', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_gpio_task_name'), table_name='gpio_task')
    op.drop_table('gpio_task')
    # ### end Alembic commands ###