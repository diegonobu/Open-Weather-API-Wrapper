import os

import requests
from flask import Flask, request, jsonify
from flask_caching import Cache

from api_wrapper.models import Weather

app = Flask(__name__)
cache = Cache(config={
    'CACHE_TYPE': os.environ.get('CACHE_TYPE', default='SimpleCache'),
    'CACHE_DEFAULT_TIMEOUT': int(os.environ.get('CACHE_DEFAULT_TIMEOUT', default=300)),
    'CACHE_THRESHOLD': int(os.environ.get('CACHE_THRESHOLD', default=5))
})

API_URL = 'https://api.openweathermap.org/data/2.5/weather'
API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')
default_max_number = int(os.environ.get('DEFAULT_MAX_NUMBER', default=290))


def get_iso3166_alpha3(iso2code):
    """
    Gets country code in the ISO 3166-1 alpha 3 format.

    :param (str) iso2code: Country ISO 3166-1 alpha-2 code.
    :return: Country ISO 3166-1 alpha-3 code.
    """
    r = requests.get(f'https://api.worldbank.org/v2/country/{iso2code}', params={'format': 'json'})
    _, item = r.json()
    return item[0]['id']


@app.route('/temperature/<string:city_name>')
def get_temperature_by_city_name(city_name):
    """
    Gets description of weather of queried city.

    :param (str) city_name: Name of the city you want to query.
    :return: Weather data in JSON format.
    """
    city_weather = cache.get(city_name)
    if city_weather:
        return jsonify(city_weather)

    params = {'q': city_name, 'appid': API_KEY}
    r = requests.get(API_URL, params=params)
    weather = Weather.convert(r.json())
    weather.city.country = get_iso3166_alpha3(weather.city.country)
    cache.set(city_name, weather.dict())
    return jsonify(weather.dict())


@app.route('/temperature')
def get_temperature():
    """
    Gets list of cached cities with max temperature.

    :return: List of cached cities with max temperature.
    """
    max = request.args.get('max', float(default_max_number), float)
    max_of_cities = {city_name: cache.get(city_name)['max']
                     for city_name in cache.cache._cache
                     if cache.get(city_name)['max'] <= max}

    return jsonify(max_of_cities)
