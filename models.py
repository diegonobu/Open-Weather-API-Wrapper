from pydantic import BaseModel


class City(BaseModel):
    name: str
    country: str


class Weather(BaseModel):
    min: float
    max: float
    avg: float
    feels_like: float
    city: City
