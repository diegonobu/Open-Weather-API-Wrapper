import os
from functools import partial

import icontract
import requests

API_URL = 'https://api.openweathermap.org/data/2.5/weather'
API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')


@icontract.ensure(lambda result, iso2code: len(result) == 3, 'country code of result must have 3 letters')
@icontract.require(lambda iso2code: len(iso2code) == 2, 'country code must have 2 letters')
def get_iso3166_alpha3(iso2code):
    """
    Gets country code in the ISO 3166-1 alpha 3 format.

    :param (str) iso2code: Country ISO 3166-1 alpha-2 code.
    :return: Country ISO 3166-1 alpha-3 code.
    """
    r = requests.get(f'https://api.worldbank.org/v2/country/{iso2code}', params={'format': 'json'})
    _, item = r.json()
    return item[0]['id']


get_weather = partial(requests.get, API_URL)


def get_data_by_city_name(city_name):
    """
    Gets data of queried city.

    :param (str) city_name: Name of the city you want to query.
    :return: Data in JSON format.
    """
    params = {'q': city_name, 'appid': API_KEY}
    response = get_weather(params=params)
    return response.json()
