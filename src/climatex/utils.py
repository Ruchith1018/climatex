from typing import Dict, Any, Optional, Union
from datetime import date, datetime

def clean_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values from a dictionary."""
    return {k: v for k, v in params.items() if v is not None}

def format_date(d: Union[str, date, datetime]) -> str:
    """Consistently format dates as YYYY-MM-DD."""
    if isinstance(d, (date, datetime)):
        return d.strftime("%Y-%m-%d")
    return d

def build_weather_params(
    latitude: float,
    longitude: float,
    current: bool = True,
    hourly: Optional[str] = "temperature_2m,relative_humidity_2m,wind_speed_10m",
    daily: Optional[str] = "temperature_2m_max,temperature_2m_min,sunrise,sunset",
    timezone: str = "auto",
    forecast_days: Optional[int] = 7,
    start_date: Optional[Union[str, date, datetime]] = None,
    end_date: Optional[Union[str, date, datetime]] = None,
    temperature_unit: str = "celsius",
    wind_speed_unit: str = "kmh",
    precipitation_unit: str = "mm",
) -> Dict[str, Any]:
    """Build URL parameters for the weather forecast and archive APIs."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,wind_direction_10m,is_day,weather_code" if current else None,
        "hourly": hourly,
        "daily": daily,
        "timezone": timezone,
        "forecast_days": forecast_days if not (start_date and end_date) else None,
        "start_date": format_date(start_date) if start_date else None,
        "end_date": format_date(end_date) if end_date else None,
        "temperature_unit": temperature_unit,
        "wind_speed_unit": wind_speed_unit,
        "precipitation_unit": precipitation_unit,
    }
    return clean_params(params)

def build_air_quality_params(
    latitude: float,
    longitude: float,
    hourly: str = "pm2_5,pm10,nitrogen_dioxide,ozone",
    timezone: str = "auto",
) -> Dict[str, Any]:
    """Build URL parameters for the Air Quality API."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly,
        "timezone": timezone,
    }
    return clean_params(params)
