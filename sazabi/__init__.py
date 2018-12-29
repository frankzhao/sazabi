import asyncio
import logging
import threading

import discord
import imgurpython
import twython
import yaml

from sazabi.plugins.twitch import Twitch
from sazabi.types import SazabiBotPlugin, LoggedObject

client = discord.Client()


class Sazabi(LoggedObject):
  def __init__(self, session, config='config.yaml'):
    self.session = session  # type: sqlalchemy.orm.session.Session
    self.logger.setLevel(logging.INFO)
    self._config = self._read_config(config)
    self.imgur_client = self._imgur_client() if 'imgur' in self._enabled_plugins else None
    self.twitter_client = self._twitter_client() if 'twitter' in self._enabled_plugins else None
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

  @property
  def _twitch_config(self):
    return self._config.get('twitch')

  @property
  def _twitter_config(self):
    return self._config.get('twitter')

  @property
  def _enabled_plugins(self):
    return self._config.get('plugins')

  def _imgur_client(self):
    try:
      return imgurpython.ImgurClient(
          self._imgur_config.get('client_id'),
          self._imgur_config.get('client_token'),
      )
    except AttributeError:
      self.logger.error(
          "Client id and token for imgur plugin must be specified. Imgur plugin disabled!")

  def _twitter_client(self):
    try:
      twitter = twython.Twython(
          self._twitter_config.get('consumer_key'),
          self._twitter_config.get('consumer_secret'),
          oauth_version=2
      )
      ACCESS_TOKEN = twitter.obtain_access_token()
      return twython.Twython(
          self._twitter_config.get('consumer_key'),
          access_token=ACCESS_TOKEN
      )
    except AttributeError:
      self.logger.error(
          "Consumer key and secret for twitter plugin must be specified. Twitter plugin disabled!")

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
    self.logger.info("Launching...")
    f_stop = threading.Event()
    loop = asyncio.get_event_loop()

    try:
      tasks = [client.start(self._config.get('discord').get('token')),
               self.background_tasks(f_stop)]
      gathered = asyncio.gather(*tasks, loop=loop)
      loop.run_until_complete(gathered)
    except RuntimeError as e:
      self.logger.error("Received fatal error: {}".format(e))
      self._handle_exit()
    except KeyboardInterrupt:
      loop.run_until_complete(client.logout())
      pending = asyncio.Task.all_tasks(loop=loop)
      gathered = asyncio.gather(*pending, loop=loop)
      try:
        gathered.cancel()
        loop.run_until_complete(gathered)

        gathered.exception()
      except:
        pass
      finally:
        loop.close()

  def _handle_exit(self):
    self.logger.error("Handing fatal error, restarting...")
    client.loop.run_until_complete(client.logout())
    for t in asyncio.Task.all_tasks(loop=client.loop):
      if t.done():
        t.exception()
        continue
      t.cancel()
      try:
        client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
        t.exception()
      except asyncio.InvalidStateError:
        pass
      except asyncio.TimeoutError:
        pass
      except asyncio.CancelledError:
        pass
    self.launch()  # TODO may cause stack overflow

  async def background_tasks(self, f_stop):
    twitch = Twitch()
    while True:
      self.logger.info('Looking for stream updates...')
      await twitch.parse(client, None, None, **self._twitch_config)
      await asyncio.sleep(self._twitch_config.get('interval'))

  @asyncio.coroutine
  async def on_ready(self):
    self.logger.info(
        "Connected as: {} {}".format(client.user.name, client.user.id))

  @asyncio.coroutine
  async def on_message(self, message):
    self.logger.info("Got message: User: {}, Message: {}".format(message.author.name, message.content))
    for plugin in self._plugins:  # type SazabiBotPlugin
      kwargs = {
        'config': self._config,
        'imgur': self.imgur_client,
        'twitter': self.twitter_client
      }
      await plugin.parse(client, message, **kwargs)
