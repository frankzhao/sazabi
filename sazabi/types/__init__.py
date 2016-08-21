import logging
from abc import abstractmethod


class LoggedObject(object):
    @property
    def logger(self):
        return logging.getLogger(__name__)


class SazabiBotPlugin(LoggedObject):
    @abstractmethod
    async def parse(self, client, message, *args, **kwargs):
        pass
