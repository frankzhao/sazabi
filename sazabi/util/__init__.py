import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
Use with @representable
"""


def representable(cls):
  def __str__(self):
    return '%s(%s)' % (
      type(self).__name__,
      ', '.join('%s=%s' % item for item in vars(self).items())
    )

  cls.__str__ = __str__
  return cls


def create_session():
  engine = create_engine(
      'postgresql+psycopg2://sazabi:sazabi@localhost:5432/sazabi', echo=False)
  Session = sessionmaker(bind=engine)
  return Session()  # type: sqlalchemy.orm.session.Session
