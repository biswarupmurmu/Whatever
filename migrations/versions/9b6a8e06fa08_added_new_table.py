"""Added new table

Revision ID: 9b6a8e06fa08
Revises: 496971813ea7
Create Date: 2024-04-29 23:44:51.427325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b6a8e06fa08'
down_revision = '496971813ea7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('fname', sa.VARCHAR(length=100), nullable=False),
    sa.Column('lname', sa.VARCHAR(length=100), nullable=False),
    sa.Column('email', sa.VARCHAR(length=80), nullable=False),
    sa.Column('password', sa.VARCHAR(length=80), nullable=False),
    sa.Column('verified_email', sa.BOOLEAN(), nullable=False),
    sa.Column('address', sa.VARCHAR(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###