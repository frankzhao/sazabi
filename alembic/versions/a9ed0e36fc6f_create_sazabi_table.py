"""create sazabi table

Revision ID: a9ed0e36fc6f
Revises: 
Create Date: 2018-05-04 18:59:19.019475

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = 'a9ed0e36fc6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
      'channel',
      sa.Column('id', UUID, primary_key=True,
                server_default=sa.text("uuid_generate_v4()")),
      sa.Column('channel_name', sa.String, nullable=False),
      sa.Column('channel_url', sa.String, nullable=False),
      sa.Column('live', sa.Boolean, nullable=False, default=False),
      sa.Column('last_updated', sa.DateTime, nullable=True),
      sa.Column('last_change', sa.DateTime, nullable=True)
  )


def downgrade():
  op.drop_table('channel')
