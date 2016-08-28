import asyncio

import discord
import imgurpython
import yaml
import logging

from sazabi.types import SazabiBotPlugin, LoggedObject

client = discord.Client()


class Sazabi(LoggedObject):
    def __init__(self, config='config.yaml'):
        self.logger.setLevel(logging.INFO)
        self._config = self._read_config(config)
        self.imgur_client = self._imgur_client()
        self._plugins = None
        self._configure_plugins()

        # TODO move these into decorators
        setattr(client, self.on_message.__name__, self.on_message)
        setattr(client, self.on_ready.__name__, self.on_ready)

    @staticmethod
    def _read_config(config):
        with open(config) as fp:
            parsed = yaml.load(fp)
        return parsed

    @property
    def _discord_config(self):
        return self._config.get('discord')

    @property
    def _imgur_config(self):
        return self._config.get('imgur')

    def _imgur_client(self):
        return imgurpython.ImgurClient(
            self._imgur_config.get('client_id'),
            self._imgur_config.get('client_token'),
        )

    @property
    def _weather_config(self):
        return self._config.get('weather')

    def _configure_plugins(self):
        if self._plugins is None:
            plugin_config = [
                getattr(
                    __import__('sazabi.plugins.' + p, fromlist=[p.title()]), p.title()
                ) for p in self._config.get('plugins')]
            _ = map(__import__, plugin_config)
            self._plugins = [cls() for cls in SazabiBotPlugin.__subclasses__()]

    def launch(self):
        client.run(self._config.get('discord').get('token'))

    @asyncio.coroutine
    async def on_ready(self):
        self.logger.info("Connected as: {} {}".format(client.user.name, client.user.id))

    @asyncio.coroutine
    async def on_message(self, message):
        for plugin in self._plugins:  # type SazabiBotPlugin
            kwargs = {
                'config': self._config,
                'imgur': self.imgur_client,
            }
            await plugin.parse(client, message, **kwargs)
