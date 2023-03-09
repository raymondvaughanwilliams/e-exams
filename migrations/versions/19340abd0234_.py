"""empty message

Revision ID: 19340abd0234
Revises: 1e3fce724d6d
Create Date: 2023-03-08 00:29:48.116605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19340abd0234'
down_revision = '1e3fce724d6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('farmers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('premium_amount', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('cashcode', sa.String(length=255), nullable=True),
    sa.Column('date_added', sa.Date(), nullable=True),
    sa.Column('last_modified', sa.Date(), nullable=True),
    sa.Column('language', sa.String(length=255), nullable=True),
    sa.Column('society', sa.String(length=255), nullable=True),
    sa.Column('farmercode', sa.String(length=255), nullable=True),
    sa.Column('cooperative', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_farmers'))
    )
    op.create_table('request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('cashcode', sa.String(), nullable=True),
    sa.Column('farmer_id', sa.Integer(), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['farmer_id'], ['farmers.id'], name=op.f('fk_request_farmer_id_farmers')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_request'))
    )
    op.drop_table('farmer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('farmer',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('number', sa.INTEGER(), nullable=True),
    sa.Column('premium_amount', sa.INTEGER(), nullable=True),
    sa.Column('location', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_farmer')
    )
    op.drop_table('request')
    op.drop_table('farmers')
    # ### end Alembic commands ###
