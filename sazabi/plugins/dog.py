import requests
from random import choice

from sazabi.types import SazabiBotPlugin


class Dog(SazabiBotPlugin):
    async def parse(self, client, message, *args, **kwargs):
        if message.content == "~dog":
            self.logger.debug('Processing dog command')
            dog_urls = ['https://dog.ceo/api/breeds/image/random']
            dog_url = choice(dog_urls)
            dog = requests.get(dog_url).json().get('message')
            hold = await client.send_message(message.channel, dog)