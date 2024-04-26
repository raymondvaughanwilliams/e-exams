"""empty message

Revision ID: 0b4083b5d0d0
Revises: e2dce3207a76
Create Date: 2023-07-07 00:33:44.572478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b4083b5d0d0'
down_revision = 'e2dce3207a76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('index_number', sa.String(), nullable=True))
        batch_op.drop_column('parts')
        batch_op.drop_column('business_name')
        batch_op.drop_column('cars')
        batch_op.drop_column('return_period')
        batch_op.drop_column('returnable')
        batch_op.drop_column('certificate')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('certificate', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('returnable', sa.VARCHAR(length=250), nullable=True))
        batch_op.add_column(sa.Column('return_period', sa.VARCHAR(length=250), nullable=True))
        batch_op.add_column(sa.Column('cars', sa.VARCHAR(length=250), nullable=True))
        batch_op.add_column(sa.Column('business_name', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('parts', sa.VARCHAR(length=250), nullable=True))
        batch_op.drop_column('index_number')

    # ### end Alembic commands ###
