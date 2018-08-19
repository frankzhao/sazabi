import logging
import os

from abc import abstractmethod


class LoggedObject(object):
  @property
  def logger(self):
    logger = logging.getLogger(__name__)
    return logger


class SazabiBotPlugin(LoggedObject):
  @abstractmethod
  async def parse(self, client, message, *args, **kwargs):
    pass
