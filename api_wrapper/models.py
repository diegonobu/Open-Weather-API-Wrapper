import icontract
from pydantic import BaseModel

from api_wrapper.dbcsupport import inv
from api_wrapper.support_api import get_iso3166_alpha3

WEATHER_BODY = {
    'main': {
        'temp_min': float,
        'temp_max': float,
        'temp': float,
        'feels_like': float,
    },
    'name': str,
    'sys': {
        'country': str
    }
}

WEATHER_FINAL = {
    'min': float,
    'max': float,
    'avg': float,
    'feels_like': float,
    'city': {
        'name': str,
        'country': str
    }
}


class City(BaseModel):
    name: str
    country: str

    @classmethod
    def convert(cls, data):
        return cls(name=data['name'],
                   country=get_iso3166_alpha3(data['sys']['country']))


@icontract.invariant(lambda self: inv(self, WEATHER_FINAL))
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
