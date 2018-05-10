import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sazabi.util import representable

Base = declarative_base()


@representable
class Channel(Base):
  __tablename__ = 'channel'

  id = Column(UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()'))
  channel_name = Column(String)
  channel_url = Column(String)
  live = Column(Boolean)
  last_updated = Column(DateTime)

  def __init__(self, id=None, channel_name=None, channel_url=None, live=False,
      last_updated=None):
    self.id = id
    self.channel_name = channel_name
    self.channel_url = channel_url
    self.live = live
    self.last_updated = last_updated

