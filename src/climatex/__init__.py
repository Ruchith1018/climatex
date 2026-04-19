from .client import ClimateXClient
from .models import (
    WeatherResponse,
    AirQualityResponse,
    CurrentWeather,
    HourlyData,
    DailyData,
    Location,
)

__version__ = "0.2.0"
__all__ = [
    "ClimateXClient",
    "WeatherResponse",
    "AirQualityResponse",
    "CurrentWeather",
    "HourlyData",
    "DailyData",
    "Location",
]
