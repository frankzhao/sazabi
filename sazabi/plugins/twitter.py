from sazabi.types import SazabiBotPlugin
from twython.exceptions import TwythonError

class Twitter(SazabiBotPlugin):
  async def parse(self, client, message, *args, **kwargs):
    twitter_client = kwargs.get('twitter')
    if message.content.startswith('https://twitter.com/'):
      try:
        status = twitter_client.show_status(id=message.content.split('/')[-1])
      except TwythonError as e:
        self.logger.error("Ignoring tweet due to error: url={}, error={}"
                          .format(message.content, e.msg))
        return
      try:
        if len(status['extended_entities']['media']) > 1:
          extra_images = list(map(
              lambda media: media['media_url_https'],
              status['extended_entities']['media'][1:]
          ))
          self.logger.info("Loading {} extra twitter images.".format(len(extra_images)))
          if status is not None:
            await client.send_message(message.channel, '\n'.join(extra_images))
      except KeyError:
        pass
