from typing import Dict, Any, Optional

def clean_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values from a dictionary."""
    return {k: v for k, v in params.items() if v is not None}

def build_weather_params(
    latitude: float,
    longitude: float,
    current: bool = True,
    hourly: Optional[str] = "temperature_2m,relative_humidity_2m,wind_speed_10m",
    daily: Optional[str] = "temperature_2m_max,temperature_2m_min,sunrise,sunset",
    timezone: str = "auto",
    forecast_days: int = 7,
) -> Dict[str, Any]:
    """Build URL parameters for the weather forecast API."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,wind_direction_10m,is_day,weather_code" if current else None,
        "hourly": hourly,
        "daily": daily,
        "timezone": timezone,
        "forecast_days": forecast_days,
    }
    return clean_params(params)
