"""remove unqiue identifiers from drivers

Revision ID: 966a62029755
Revises: e5104f4a8e98
Create Date: 2025-08-03 18:49:17.671783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '966a62029755'
down_revision = 'e5104f4a8e98'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('drivers') as batch_op:
        batch_op.drop_index('code')
        batch_op.drop_index('permanent_number')

def downgrade():
    with op.batch_alter_table('drivers') as batch_op:
        batch_op.create_index('code', ['code'], unique=True)
        batch_op.create_index('permanent_number', ['permanent_number'], unique=True)

