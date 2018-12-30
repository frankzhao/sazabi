import requests
from random import choice
from urllib.parse import quote as urlquote

from sazabi.types import SazabiBotPlugin


class Cat(SazabiBotPlugin):
    async def parse(self, client, message, *args, **kwargs):
        if message.content == "~cat":
            self.logger.debug('Processing cat command')
            cat_urls = ['http://thecatapi.com/api/images/get', "http://aws.random.cat/meow"]
            cat_url = choice(cat_urls)
            if 'thecatapi' in cat_url:
                cat = requests.get(cat_url).url
            else:
                cat = requests.get(cat_url).json().get('file')

            if cat:
                # Encode URL
                cat = cat.replace('https://', '')
                cat = 'https://' + urlquote(cat)
                await client.send_message(message.channel, cat)
