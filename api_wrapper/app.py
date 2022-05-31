import os

import icontract
from flask import request, jsonify, Blueprint, Response
from flask_caching import Cache

from api_wrapper import support_api
from api_wrapper.dbcsupport import pre, post
from api_wrapper.models import Weather, WEATHER_BODY, WEATHER_FINAL

cache = Cache(config={
    'CACHE_TYPE': os.environ.get('CACHE_TYPE', default='SimpleCache'),
    'CACHE_DEFAULT_TIMEOUT': int(os.environ.get('CACHE_DEFAULT_TIMEOUT', default=300)),
    'CACHE_THRESHOLD': int(os.environ.get('CACHE_THRESHOLD', default=5))
})

default_max_number = int(os.environ.get('DEFAULT_MAX_NUMBER', default=290))

temperature = Blueprint('temperature', __name__, url_prefix='/temperature')


@icontract.ensure(lambda result, data: post(result, WEATHER_FINAL))
@icontract.require(lambda data: pre(data, WEATHER_BODY))
@temperature.route('/<string:city_name>')
def get_temperature_by_city_name(city_name) -> Response:
    """
    Gets description of weather of queried city.

    req: 'main' in self;
    req: 'temp_min' in self['main'];
    req: 'temp_max' in self['main'];
    req: 'temp' in self['main'];
    req: 'feels_like' in self['main'];
    req: 'name' in self;
    req: 'sys' in self;
    req: 'country' in self['sys'];

    ensure: 'min' in self;
    ensure: 'max' in self;
    ensure: 'avg' in self;
    ensure: 'feels_like' in self;
    ensure: 'city' in self;
    ensure: 'name' in self['city'];
    ensure: 'country' in self['city'];

    :param (str) city_name: Name of the city.
    :return: Weather data in JSON format.
    """
    city_weather = cache.get(city_name)
    if city_weather:
        return jsonify(city_weather)

    city_data = support_api.get_data_by_city_name(city_name)
    if city_data['cod'] == '404':
        return {'message': city_data['message']}, 404

    weather = Weather.convert(city_data)
    weather.city.country = support_api.get_iso3166_alpha3(weather.city.country)
    cache.set(city_name, weather.dict())
    return jsonify(weather.dict())


@temperature.route('/')
def get_temperature() -> Response:
    """
    Gets list of cached cities with max temperature.

    :return: List of cached cities with max temperature.
    """
    max_ = request.args.get('max', float(default_max_number), float)
    max_of_cities = {city_name: cache.get(city_name)['max']
                     for city_name in cache.cache._cache
                     if cache.get(city_name)['max'] <= max_}

    return jsonify(max_of_cities)
