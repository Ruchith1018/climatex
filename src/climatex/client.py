import httpx
import time
import asyncio
from typing import List, Optional, Dict, Any
from .models import WeatherResponse, CurrentWeather, GeocodingResponse, Location
from .utils import build_weather_params

class ClimateXClient:
    """
    ClimateXClient is a wrapper for the Open-Meteo API.
    Supports both synchronous and asynchronous operations.
    """
    WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

    def __init__(self, timeout: float = 20.0, retries: int = 3):
        self.timeout = timeout
        self.retries = retries
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
        params = build_weather_params(latitude, longitude, current=True, hourly=None, daily=None)
        
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
        params = build_weather_params(latitude, longitude, current=True, hourly=None, daily=None)
        
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
        params = build_weather_params(latitude, longitude, forecast_days=days)
        
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
        params = build_weather_params(latitude, longitude, forecast_days=days)
        
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
