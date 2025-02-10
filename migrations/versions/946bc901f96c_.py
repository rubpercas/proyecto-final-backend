"""empty message

Revision ID: 946bc901f96c
Revises: 4aeafa4b0c86
Create Date: 2025-02-10 11:59:49.767067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '946bc901f96c'
down_revision = '4aeafa4b0c86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('nombre',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('nombre_usuario',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('nombre_usuario',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('nombre',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###
