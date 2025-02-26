"""initial migration

Revision ID: 0b4a87c33a7b
Revises: 
Create Date: 2024-11-26 20:44:33.596106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b4a87c33a7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('db_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('db_users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_db_users_username'), ['username'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('db_users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_db_users_username'))

    op.drop_table('db_users')
    # ### end Alembic commands ###
