import requests

from sazabi.types import SazabiBotPlugin


class Weather(SazabiBotPlugin):
    def emoji_map(self, key=None):
        key = key.lower() if key else key
        emoji = {
            'few clouds': ':white_sun_small_cloud:',
            'scattered clouds': ':partly_sunny:',
            'broken clouds': ':white_sun_cloud:',
            'overcast clouds': ':cloud:',
            'clear sky': ':sunny:',
            'clear': ':sunny:',
            'light rain': ':cloud_rain:',
            'light': ':cloud_rain:',
            'moderate rain': ':cloud_rain:',
            'heavy intensity rain': ':cloud_rain:',
            'very heavy rain': ':cloud_rain:',
            'extreme rain': ':cloud_rain:',
            'freezing rain': ':cloud_snow:',
            'light intensity shower rain': ':white_sun_rain_cloud:',
            'shower rain': ':cloud_rain:',
            'heavy intensity shower rain': ':cloud_rain:',
            'ragged shower rain': ':cloud_rain:',
            'thunderstorm with light rain': ':thunder_cloud_rain:',
            'thunderstorm with rain': ':thunder_cloud_rain:',
            'thunderstorm with heavy rain': ':thunder_cloud_rain:',
            'light thunderstorm': ':cloud_lightning:',
            'thunderstorm': ':cloud_lightning:',
            'heavy thunderstorm': ':cloud_lightning:',
            'ragged thunderstorm': ':cloud_lightning:',
            'thunderstorm with light drizzle': ':thunder_cloud_rain:',
            'thunderstorm with drizzle': ':thunder_cloud_rain:',
            'thunderstorm with heavy drizzle': ':thunder_cloud_rain:',
            'light snow': ':cloud_snow:',
            'snow': ':cloud_snow:',
            'heavy snow': ':cloud_snow:',
            'sleet': ':cloud_snow:',
            'shower sleet': ':cloud_snow:',
            'light rain and snow': ':cloud_snow:',
            'rain and snow': ':cloud_snow:',
            'light shower snow': ':cloud_snow:',
            'shower snow': ':cloud_snow:',
            'heavy shower snow': ':cloud_snow:',
            'fog': ':foggy:',
            'tornado': ':cloud_tornado:',
            'tropical storm': ':thunder_cloud_rain:',
            'hurricane': ':cloud_tornado:',
            'severe thunderstorms': ':thunder_cloud_rain:',
            'thunderstorms': ':thunder_cloud_rain:',
            'mixed rain and snow': ':cloud_rain:',
            'mixed rain and sleet': ':cloud_rain:',
            'mixed snow and sleet': ':cloud_snow:',
            'freezing drizzle': ':cloud_rain:',
            'drizzle': ':cloud_rain:',
            'showers': ':cloud_rain:',
            'snow flurries': ':cloud_snow:',
            'light snow showers': ':cloud_snow:',
            'blowing snow': ':cloud_snow:',
            'hail': ':cloud_rain:',
            'dust': ':fog:',
            'foggy': ':foggy:',
            'haze': ':fog:',
            'smoky': ':fog:',
            'blustery': ':foggy:',
            'windy': ':wind_blowing_face:',
            'cold': ':snowflake:',
            'cloudy': ':cloud:',
            'mostly cloudy (night)': ':cloud:',
            'mostly cloudy (day)': ':cloud:',
            'mostly cloudy': ':cloud:',
            'partly cloudy (night)': ':cloud:',
            'partly cloudy (day)': ':cloud:',
            'clear (night)': ':full_moon:',
            'sunny': ':sunny:',
            'fair (night)': ':white_sun_small_cloud:',
            'fair (day)': ':white_sun_small_cloud:',
            'fair': ':white_sun_small_cloud:',
            'mixed rain and hail': ':cloud_rain:',
            'hot': ':sunny:',
            'isolated thunderstorms': ':thunder_cloud_rain:',
            'scattered thunderstorms': ':thunder_cloud_rain:',
            'scattered showers': ':cloud_rain:',
            'scattered snow showers': ':cloud_snow:',
            'partly cloudy': ':partly_sunny:',
            'thundershowers': ':thunder_cloud_rain:',
            'snow showers': ':cloud_snow:',
            'isolated thundershowers': ':thunder_cloud_rain:',
            'not available': ':grey_question:'
        }
        if key:
            return emoji.get(key)
        return emoji

    async def parse(self, client, message, *args, **kwargs):
        """
        :type client: discord.client.Client
        :type message: discord.message.Message
        :type args: list
        :type kwargs: dict
        :return:
        """
        msg = None
        if message.content.startswith("~weather"):
            city = message.content.split(' ')[1:]
            if not city:
                city = 'Brisbane'
            response = requests.get(
                'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20'
                'where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22{city_name}%22)'
                '&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
                .format(city_name=city))
            import logging
            logger = logging.getLogger('asyncio')
            logger.exception(response.json())
            if response:
                weather = response.json()['query']['results']['channel']
                emoji = self.emoji_map(key=weather.get('item').get('condition').get('text'))
                msg = '**{city}, {country}**\n' \
                      '{emoji} {temperature:.1f}°C {weather}\n' \
                      '*Humidity {humidity}%*\n' \
                      '*Wind: {wind_speed}m/s*'.format(
                    city=weather.get('location').get('city'),
                    country=weather.get('location').get('country'),
                    emoji=emoji,
                    temperature=(float(weather.get('item').get('condition').get('temp')) - 32) * (5 / 9),   # F to C
                    weather=weather.get('item').get('condition').get('text').title(),
                    humidity=weather.get('atmosphere').get('humidity'),
                    wind_speed=weather.get('wind').get('speed')
                )

        if msg is not None:
            await client.send_message(message.channel, msg)
