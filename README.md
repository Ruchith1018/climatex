# ClimateX 🌦️

ClimateX is a simple, high-performance Python wrapper for the [Open-Meteo API](https://open-meteo.com/). It supports both synchronous and asynchronous requests, making it ideal for everything from data science scripts to real-time bots and web applications.

## Features

- ⚡ **Sync & Async Support**: Built on top of `httpx`.
- 🔍 **Geocoding API**: Search for coordinates by city name.
- 🌡️ **Current Weather**: Get real-time weather details.
- 📅 **7-Day Forecast**: Hourly and daily weather variables.
- 🛡️ **Type Safety**: Fully typed with Pydantic models.

## Local Development Setup

To set up **ClimateX** for local development, follow these steps:

1. **Create a Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

2. **Activate the Environment**:
   - **Windows**: `.venv\Scripts\activate`
   - **Mac/Linux**: `source .venv/bin/activate`

3. **Install in Editable Mode (with dev dependencies)**:
   ```bash
   pip install -e ".[test, dev]"
   ```

## Installation

```bash
pip install climatex
```

## Quick Start

### Synchronous Usage

```python
from climatex import ClimateXClient

client = ClimateXClient()

# Search for a location
locations = client.search_location("London")
london = locations[0]

# Get current weather
weather = client.get_current_weather(london.latitude, london.longitude)
print(f"Current Temperature: {weather.temperature_2m}°C")
```

### Asynchronous Usage

```python
import asyncio
from climatex import ClimateXClient

async def main():
    async with ClimateXClient() as client:
        weather = await client.get_current_weather(51.5, -0.12)
        print(f"Temperature: {weather.temperature_2m}°C")

asyncio.run(main())
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
