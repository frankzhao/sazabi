from datetime import datetime
import json
import requests
from sazabi.util import create_session
from sazabi.model import Channel
from sazabi.types import SazabiBotPlugin


class Twitch(SazabiBotPlugin):

  def parse(self, client, message, *args, **kwargs):
    session = create_session()   # type: sqlalchemy.orm.session.Session
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
        channel = session.query(Channel).filter(Channel.channel_name == user_login).first()

        if len(streams) > 0:
          self.logger.info('Stream {} is live'.format(user_login))
          channel.live = True
        else:
          channel.live = False
          self.logger.info('Stream {} is offline'.format(user_login))
        channel.last_updated = datetime.now()
        session.commit()
      else:
        self.logger.error("Could not connect to twtch: {}".format(response.status_code))
