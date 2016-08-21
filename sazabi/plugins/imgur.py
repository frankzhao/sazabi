import logging

from random import choice

from sazabi.types import SazabiBotPlugin


class Imgur(SazabiBotPlugin):
    async def parse(self, client, message, *args, **kwargs):
        imgur_client = kwargs.get('imgur')
        pic = None
        if message.content == "~imgur":
            self.logger.debug('Processing imgur command')

            pics = imgur_client.gallery_random(page=0)
            pic = choice(pics).link
        elif message.content == "~meme":
            self.logger.debug('Processing meme command')

            memes = imgur_client.memes_subgallery(sort='viral', page=0, window='week')
            pic = choice(memes).link
        elif message.content == "~robot":
            keyword = choice(['gundam', 'robot', 'mecha'])

            self.logger.debug('Processing robot command')

            robots = imgur_client.gallery_search(keyword)
            pic = choice(robots).link

        if pic is not None:
            await client.send_message(message.channel, pic)
