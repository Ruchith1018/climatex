import httpx
import time
import asyncio
from typing import List, Optional, Dict, Any, Union
from datetime import date, datetime
from .models import WeatherResponse, CurrentWeather, AirQualityResponse, GeocodingResponse, Location
from .utils import build_weather_params, build_air_quality_params

class ClimateXClient:
    """
    ClimateXClient is a wrapper for the Open-Meteo API.
    Supports both synchronous and asynchronous operations.
    """
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
    AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

    def __init__(
        self, 
        timeout: float = 20.0, 
        retries: int = 3,
        temperature_unit: str = "celsius",
        wind_speed_unit: str = "kmh",
        precipitation_unit: str = "mm"
    ):
        self.timeout = timeout
        self.retries = retries
        self.temperature_unit = temperature_unit
        self.wind_speed_unit = wind_speed_unit
        self.precipitation_unit = precipitation_unit
        self._sync_client: Optional[httpx.Client] = None
        self._async_client: Optional[httpx.AsyncClient] = None

    @property
    def sync_client(self) -> httpx.Client:
        if self._sync_client is None:
            self._sync_client = httpx.Client(timeout=self.timeout)
        return self._sync_client

    @property
    def async_client(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(timeout=self.timeout)
        return self._async_client

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._sync_client:
            self._sync_client.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._async_client:
            await self._async_client.aclose()

    def _get_common_params(self) -> Dict[str, str]:
        return {
            "temperature_unit": self.temperature_unit,
            "wind_speed_unit": self.wind_speed_unit,
            "precipitation_unit": self.precipitation_unit,
        }

    def search_location(self, name: str, count: int = 10) -> List[Location]:
        """Search for a location by name (Synchronous)."""
        params: Dict[str, Any] = {"name": name, "count": count, "language": "en", "format": "json"}
        
        for attempt in range(self.retries + 1):
            try:
                response = self.sync_client.get(self.GEOCODING_URL, params=params)
                response.raise_for_status()
                data = GeocodingResponse(**response.json())
                return data.results
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt == self.retries:
                    raise
                time.sleep(1 * (attempt + 1))
        return []

    async def search_location_async(self, name: str, count: int = 10) -> List[Location]:
        """Search for a location by name (Asynchronous)."""
        params: Dict[str, Any] = {"name": name, "count": count, "language": "en", "format": "json"}
        
        for attempt in range(self.retries + 1):
            try:
                response = await self.async_client.get(self.GEOCODING_URL, params=params)
                response.raise_for_status()
                data = GeocodingResponse(**response.json())
                return data.results
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt == self.retries:
                    raise
                await asyncio.sleep(1 * (attempt + 1))
        return []

    def get_current_weather(self, latitude: float, longitude: float) -> CurrentWeather:
        """Get current weather details (Synchronous)."""
        params = build_weather_params(latitude, longitude, current=True, hourly=None, daily=None, **self._get_common_params())
        
        for attempt in range(self.retries + 1):
            try:
                response = self.sync_client.get(self.WEATHER_URL, params=params)
                response.raise_for_status()
                data = WeatherResponse(**response.json())
                if not data.current:
                    raise ValueError("No current weather data returned")
                return data.current
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt == self.retries:
                    raise
                time.sleep(1 * (attempt + 1))
        raise ValueError("Failed to fetch weather data after retries")

    async def get_current_weather_async(self, latitude: float, longitude: float) -> CurrentWeather:
        """Get current weather details (Asynchronous)."""
        params = build_weather_params(latitude, longitude, current=True, hourly=None, daily=None, **self._get_common_params())
        
        for attempt in range(self.retries + 1):
            try:
                response = await self.async_client.get(self.WEATHER_URL, params=params)
                response.raise_for_status()
                data = WeatherResponse(**response.json())
                if not data.current:
                    raise ValueError("No current weather data returned")
                return data.current
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt == self.retries:
                    raise
                await asyncio.sleep(1 * (attempt + 1))
        raise ValueError("Failed to fetch weather data after retries")

    def get_forecast(self, latitude: float, longitude: float, days: int = 7) -> WeatherResponse:
        """Get full weather forecast (Synchronous)."""
        params = build_weather_params(latitude, longitude, forecast_days=days, **self._get_common_params())
        
        for attempt in range(self.retries + 1):
            try:
                response = self.sync_client.get(self.WEATHER_URL, params=params)
                response.raise_for_status()
                return WeatherResponse(**response.json())
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt == self.retries:
                    raise
                time.sleep(1 * (attempt + 1))
        raise ValueError("Failed to fetch forecast data after retries")

    async def get_forecast_async(self, latitude: float, longitude: float, days: int = 7) -> WeatherResponse:
        """Get full weather forecast (Asynchronous)."""
        params = build_weather_params(latitude, longitude, forecast_days=days, **self._get_common_params())
        
        for attempt in range(self.retries + 1):
            try:
                response = await self.async_client.get(self.WEATHER_URL, params=params)
                response.raise_for_status()
                return WeatherResponse(**response.json())
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt == self.retries:
                    raise
                await asyncio.sleep(1 * (attempt + 1))
        raise ValueError("Failed to fetch forecast data after retries")

    def get_historical_weather(
        self, 
        latitude: float, 
        longitude: float, 
        start_date: Union[str, date, datetime],
        end_date: Union[str, date, datetime]
    ) -> WeatherResponse:
        """Get historical weather data (Synchronous)."""
        params = build_weather_params(
            latitude, longitude, current=False, 
            start_date=start_date, end_date=end_date, 
            **self._get_common_params()
        )
        
        for attempt in range(self.retries + 1):
            try:
                response = self.sync_client.get(self.ARCHIVE_URL, params=params)
                response.raise_for_status()
                return WeatherResponse(**response.json())
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt == self.retries:
                    raise
                time.sleep(1 * (attempt + 1))
        raise ValueError("Failed to fetch historical data after retries")

    async def get_historical_weather_async(
        self, 
        latitude: float, 
        longitude: float, 
        start_date: Union[str, date, datetime],
        end_date: Union[str, date, datetime]
    ) -> WeatherResponse:
        """Get historical weather data (Asynchronous)."""
        params = build_weather_params(
            latitude, longitude, current=False, 
            start_date=start_date, end_date=end_date, 
            **self._get_common_params()
        )
        
        for attempt in range(self.retries + 1):
            try:
                response = await self.async_client.get(self.ARCHIVE_URL, params=params)
                response.raise_for_status()
                return WeatherResponse(**response.json())
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt == self.retries:
                    raise
                await asyncio.sleep(1 * (attempt + 1))
        raise ValueError("Failed to fetch historical data after retries")

    def get_air_quality(self, latitude: float, longitude: float) -> AirQualityResponse:
        """Get air quality monitoring data (Synchronous)."""
        params = build_air_quality_params(latitude, longitude)
        
        for attempt in range(self.retries + 1):
            try:
                response = self.sync_client.get(self.AIR_QUALITY_URL, params=params)
                response.raise_for_status()
                return AirQualityResponse(**response.json())
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt == self.retries:
                    raise
                time.sleep(1 * (attempt + 1))
        raise ValueError("Failed to fetch air quality data after retries")

    async def get_air_quality_async(self, latitude: float, longitude: float) -> AirQualityResponse:
        """Get air quality monitoring data (Asynchronous)."""
        params = build_air_quality_params(latitude, longitude)
        
        for attempt in range(self.retries + 1):
            try:
                response = await self.async_client.get(self.AIR_QUALITY_URL, params=params)
                response.raise_for_status()
                return AirQualityResponse(**response.json())
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt == self.retries:
                    raise
                await asyncio.sleep(1 * (attempt + 1))
        raise ValueError("Failed to fetch air quality data after retries")
