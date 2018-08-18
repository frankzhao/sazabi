import asyncio
import json
import time
from datetime import datetime

import requests

from sazabi.model import Channel
from sazabi.types import SazabiBotPlugin
from sazabi.util import create_session


class Twitch(SazabiBotPlugin):
  async def parse(self, client, message, *args, **kwargs):
    session = create_session()  # type: sqlalchemy.orm.session.Session
    client_id = kwargs.get('client_id')

    headers = {'Client-ID': client_id}

    for channel in session.query(Channel).all():
      user_login = channel.channel_name
      response = requests.get('https://api.twitch.tv/helix/streams?user_login='
                              + user_login, headers=headers)
      if response.status_code == 200:
        result = json.loads(response.text)
        streams = result.get('data')

        # update status
        channel = session.query(Channel).filter(
          Channel.channel_name == user_login).first()

        notify = False  # send a message update when going online
        if len(streams) > 0:
          if not channel.live:
            # became live
            notify = True
          self.logger.debug('Stream {} is live'.format(user_login))
          channel.live = True
        else:
          channel.live = False
          self.logger.debug('Stream {} is offline'.format(user_login))
        channel.last_updated = datetime.now()

        if notify:
          channel.last_change = datetime.now()
          self.logger.info('Send update, {} went live'.format(channel.channel_name))
          await self.send_update(client, channel.channel_name)
        else:
          self.logger.info('No stream changes')
        session.commit()

      else:
        self.logger.error(
          "Could not connect to twitch: {}, {}".format(response.status_code, response.text))

  async def send_update(self, client, stream_name):
    channels = [c for c in client.get_all_channels() if 'general' in c.name.lower()]
    for c in channels:
      message = 'Stream {} went online! https://twitch.tv/{}'.format(stream_name, stream_name)
      await self.send_message_wrapper(client, c, message)
      self.logger.info("Send update done")

  async def send_message_wrapper(self, client, channel, message):
    self.logger.info("Sending message: {}".format(message))
    await client.send_message(channel, message)
