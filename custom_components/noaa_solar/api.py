"""API client implementations."""

from typing import Any
from cachetools import TTLCache
from aiohttp import ClientSession
from homeassistant.helpers.update_coordinator import UpdateFailed


class NOAASpaceApi:
    """NOAA API implementation."""

    def __init__(self, url: str) -> None:
        """Initialize NOAA space api."""
        # NOAA API always returns Cache-Control max-age:60, respect it and don't load their systems
        self.cache = TTLCache(maxsize=5, ttl=60)
        self.url = url

    async def fetch_solar_wind_mag_field(self) -> Any:
        """Fetch solar wind mag data."""
        json = await self.get_json(
            self.url + "/products/summary/solar-wind-mag-field.json"
        )
        return json

    async def fetch_solar_wind_speed(self) -> Any:
        """Fetch solar wind speed data."""
        json = await self.get_json(self.url + "/products/summary/solar-wind-speed.json")
        return json

    async def fetch_solar_activity_10_cm_flux(self) -> Any:
        """Fetch solar activity (10cm flux) data."""
        json = await self.get_json(self.url + "/products/summary/10cm-flux.json")
        return json

    async def fetch_suvi_primary_304_image(self) -> bytes:
        """Fetch suvi primary 304 image."""
        image = await self.get_image(
            self.url + "/images/animations/suvi/primary/304/latest.png"
        )
        return image

    async def fetch_lasco_c3_image(self) -> bytes:
        """Fetch lasco c3 image."""
        image = await self.get_image(
            self.url + "/images/animations/lasco-c3/latest.jpg"
        )
        return image

    def default_json_headers(self):
        """Prepare default request headers for fetching data from noaa api."""
        return {
            "Accept": "application/json",
            "User-Agent": "Home Assistant NOAA Solar Integration",
        }

    def default_image_headers(self):
        """Prepare default request headers for fetching data from noaa api."""
        return {
            "Accept": "image/png",
            "User-Agent": "Home Assistant NOAA Solar Integration",
        }

    async def get_json(self, url: str) -> Any:
        """HTTP request helper method."""
        cached = self.cache.get(url)
        if cached:
            return cached

        async with ClientSession() as session, session.get(
            url,
            headers=self.default_json_headers(),
        ) as resp:
            if resp.status == 200:
                json = await resp.json()
                self.cache[url] = json
                return json

            raise UpdateFailed(
                f"Error retrieving data from url '{url}'. Response status code is '{resp.status}'"
            )

    async def get_image(self, url: str) -> bytes:
        """HTTP request helper method."""
        cached = self.cache.get(url)
        if cached:
            return cached

        async with ClientSession() as session, session.get(
            url,
            headers=self.default_image_headers(),
        ) as resp:
            if resp.status == 200:
                data = await resp.read()
                self.cache[url] = data
                return data

            raise UpdateFailed(
                f"Error retrieving data from url '{url}'. Response status code is '{resp.status}'"
            )
