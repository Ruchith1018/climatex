from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class CurrentWeather(BaseModel):
    time: str
    interval: int
    temperature_2m: float = Field(..., description="Air temperature at 2 meters above ground")
    wind_speed_10m: float = Field(..., description="Wind speed at 10 meters above ground")
    wind_direction_10m: int
    is_day: int
    weather_code: int

class HourlyData(BaseModel):
    time: List[str]
    temperature_2m: Optional[List[float]] = None
    relative_humidity_2m: Optional[List[float]] = None
    wind_speed_10m: Optional[List[float]] = None
    # Support for Air Quality variables
    pm2_5: Optional[List[float]] = None
    pm10: Optional[List[float]] = None
    nitrogen_dioxide: Optional[List[float]] = None
    ozone: Optional[List[float]] = None

class DailyData(BaseModel):
    time: List[str]
    temperature_2m_max: List[float]
    temperature_2m_min: List[float]
    sunrise: Optional[List[str]] = None
    sunset: Optional[List[str]] = None

class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: Optional[str] = None
    elevation: float
    current: Optional[CurrentWeather] = None
    hourly: Optional[HourlyData] = None
    daily: Optional[DailyData] = None

class AirQualityResponse(BaseModel):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: Optional[str] = None
    elevation: Optional[float] = None
    hourly: HourlyData

class Location(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    elevation: Optional[float] = None
    feature_code: Optional[str] = None
    country_code: Optional[str] = None
    admin1: Optional[str] = None
    timezone: str

class GeocodingResponse(BaseModel):
    results: List[Location] = []
    generationtime_ms: float
