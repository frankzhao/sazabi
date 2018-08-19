import logging
import os

from abc import abstractmethod


class LoggedObject(object):
  @property
  def logger(self):
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(os.getenv("SAZABI_LOG", "/var/log/sazabi.log"))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class SazabiBotPlugin(LoggedObject):
  @abstractmethod
  async def parse(self, client, message, *args, **kwargs):
    pass
