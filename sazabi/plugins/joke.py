import requests
from random import choice

from sazabi.types import SazabiBotPlugin


class Joke(SazabiBotPlugin):
    async def parse(self, client, message, *args, **kwargs):
        if message.content == "~joke":
            response = requests.get(
                'https://www.reddit.com/r/oneliners/new.json',
                headers={'User-agent': 'sazabi-bot'}).json()
            if response is not None:
                try:
                    response = choice(response.get('data').get('children'))
                    joke_url = response.get('data').get('title')
                    hold = await client.send_message(message.channel, joke_url)
                except Exception as e:
                    self.logger.exception('Joke command failed!')
                    raise e