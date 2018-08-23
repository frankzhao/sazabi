from discord.user import User

from sazabi.types import SazabiBotPlugin


class Twitter(SazabiBotPlugin):
    async def parse(self, client, message, *args, **kwargs):
        twitter_client = kwargs.get('twitter')
        if message.content.startswith('https://twitter.com/'):
            status = twitter_client.show_status(id='1032512403890614273')
            if len(status['extended_entities']['media']) > 1:
                extra_images = list(map(
                    lambda media: media['media_url_https'], 
                    status['extended_entities']['media'][1:]
                ))
            if status is not None:
                await client.send_message(message.channel, {files: extra_images})
