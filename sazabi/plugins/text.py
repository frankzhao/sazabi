from discord.user import User

from sazabi.types import SazabiBotPlugin


class Text(SazabiBotPlugin):
    async def parse(self, client, message, *args, **kwargs):
        """
        :type client: discord.client.Client
        :type message: discord.message.Message
        :type args: list
        :type kwargs: dict
        :return:
        """
        # TODO read these custom texts from file
        msg = None
        if message.content == "~commands":
            msg = '\n'.join(list(map(lambda x: '~'+x, kwargs.get('config').get('plugins'))))
        elif message.content == "~vaporwave":
            msg = ":sparkles: A E S T H E T I C :sparkles:"
        elif message.content == "~sparkling":
            msg = """
･ﾟ✧:･ﾟ+..｡✧･ﾟ:・..｡ ✧･ﾟ :･ﾟ ゜・:･ ✧･ﾟ:･ﾟ:.｡ ✧･ﾟ*・✧･':
｡ﾟ+..｡ ✧･ﾟ: ✧･ﾟ:・゜・SPARKULING・✧･ﾟ :･ﾟ ゜・:･ ✧･ﾟ
*・゜・:･ﾟ✧:･ﾟ✧｡ﾟ+..｡ ✧･ﾟ: ✧･ﾟ:・゜・:･ﾟ✧::・・:･ﾟ･ﾟ'
"""

        if msg is not None:
            await client.send_message(message.channel, msg)
