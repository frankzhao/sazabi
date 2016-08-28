import requests

from sazabi.types import SazabiBotPlugin


class Weather(SazabiBotPlugin):
    def emoji_map(self, key=None):
        emoji = {
            'few clouds': ':white_sun_small_cloud:',
            'scattered clouds': ':partly_sunny:',
            'broken clouds': ':white_sun_cloud:',
            'overcast clouds': ':cloud:',
            'clear sky': ':sunny:',
            'light rain': ':cloud_rain:',
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
            'light snow': 'cloud_snow:',
            'snow': 'cloud_snow:',
            'heavy snow': 'cloud_snow:',
            'sleet': 'cloud_snow:',
            'shower sleet': 'cloud_snow:',
            'light rain and snow': 'cloud_snow:',
            'rain and snow': 'cloud_snow:',
            'light shower snow': 'cloud_snow:',
            'shower snow': 'cloud_snow:',
            'heavy shower snow': 'cloud_snow:',
            'fog': ':foggy:'
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
        api_key = kwargs.get('config').get('weather').get('api_key')
        msg = None
        if message.content.startswith("~weather"):
            city = message.content.split(' ')[1:]
            if not city:
                city = 'Brisbane'
            response = requests.get('http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={api_key}'
                                    .format(city_name=city, api_key=api_key))
            if response:
                try:
                    weather = response.json()
                    emoji = self.emoji_map(weather.get('weather')[0].get('description'))
                    msg = '**{city}, {country}**\n' \
                          '{emoji} {temperature:.1f}° {weather}\n' \
                          '*Humidity {humidity}%*\n' \
                          '*Wind: {wind_speed}m/s*'.format(
                        city=weather.get('name'),
                        country=weather.get('sys').get('country'),
                        emoji=emoji if emoji else '',
                        temperature=float(weather.get('main').get('temp')) - 273.16,
                        weather=weather.get('weather')[0].get('description').title(),
                        humidity=weather.get('main').get('humidity'),
                        wind_speed=weather.get('wind').get('speed')
                    )
                except TypeError:
                    pass

        if msg is not None:
            await client.send_message(message.channel, msg)
