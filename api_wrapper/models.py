from pydantic import BaseModel


class City(BaseModel):
    name: str
    country: str

    @classmethod
    def convert(cls, data):
        return cls(name=data['name'], country=data['sys']['country'])


class Weather(BaseModel):
    min: float
    max: float
    avg: float
    feels_like: float
    city: City

    @classmethod
    def convert(cls, data):
        return cls(min=data['main']['temp_min'],
                   max=data['main']['temp_max'],
                   avg=data['main']['temp'],
                   feels_like=data['main']['feels_like'],
                   city=City.convert(data))
