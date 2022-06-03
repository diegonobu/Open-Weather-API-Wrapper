from collections import namedtuple

import icontract
from pydantic import BaseModel

from api_wrapper.dbcsupport import inv
from api_wrapper.support_api import get_iso3166_alpha3

WeatherStructure = namedtuple('ReqStructure', 'type optional len')

WEATHER_REQ = {
    'main': {
        'temp_min': WeatherStructure(float, False, None),
        'temp_max': WeatherStructure(float, False, None),
        'temp': WeatherStructure(float, False, None),
        'feels_like': WeatherStructure(float, False, None),
    },
    'name': WeatherStructure(str, False, None),
    'sys': {
        'country': WeatherStructure(str, False, 2),
    }
}

WEATHER_ENS = {
    'min': WeatherStructure(float, False, None),
    'max': WeatherStructure(float, False, None),
    'avg': WeatherStructure(float, False, None),
    'feels_like': WeatherStructure(float, False, None),
    'city': {
        'name': WeatherStructure(str, False, None),
        'country': WeatherStructure(str, False, 3),
    }
}


class City(BaseModel):
    name: str
    country: str

    @classmethod
    def convert(cls, data):
        return cls(name=data['name'],
                   country=get_iso3166_alpha3(data['sys']['country']))


@icontract.invariant(lambda self: inv(self, WEATHER_ENS))
class Weather(BaseModel):
    """
    inv: 'min' in self;
    inv: 'max' in self;
    inv: 'avg' in self;
    inv: 'feels_like' in self;
    inv: 'city' in self;
    inv: 'name' in self['city'];
    inv: 'country' in self['city'];
    """
    min: float
    max: float
    avg: float
    feels_like: float
    city: City

    def __init__(self, **kwargs: any):
        super().__init__(**kwargs)

    @classmethod
    def convert(cls, data):
        return cls(min=data['main']['temp_min'],
                   max=data['main']['temp_max'],
                   avg=data['main']['temp'],
                   feels_like=data['main']['feels_like'],
                   city=City.convert(data))


@icontract.invariant(lambda self: isinstance(self.name, str))
@icontract.invariant(lambda self: isinstance(self.country, str))
@icontract.invariant(lambda self: len(self.country) == 3)
class CityV2:

    def __init__(self, data):
        self.name = data['name']
        self.country = get_iso3166_alpha3(data['sys']['country'])


@icontract.invariant(lambda self: isinstance(self.min, float))
@icontract.invariant(lambda self: isinstance(self.max, float))
@icontract.invariant(lambda self: isinstance(self.avg, float))
@icontract.invariant(lambda self: isinstance(self.feels_like, float))
class WeatherV2:
    """
    inv: 'min' in self;
    inv: 'max' in self;
    inv: 'avg' in self;
    inv: 'feels_like' in self;
    inv: 'city' in self;
    inv: 'name' in self['city'];
    inv: 'country' in self['city'];
    """

    def __init__(self, data):
        self.min = data['main']['temp_min']
        self.max = data['main']['temp_max']
        self.avg = data['main']['temp']
        self.feels_like = data['main']['feels_like']
        self.city = CityV2(data)
