"""API client implementations."""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp
from cachetools import TTLCache


class NOAASolarApiClientError(Exception):
    """Base exception for NOAA Solar API client errors."""


class NOAASolarApiClientCommunicationError(NOAASolarApiClientError):
    """Raised when API communication fails."""


class NOAASolarApiClientAuthenticationError(NOAASolarApiClientError):
    """Raised when API authentication fails."""


class NOAASolarApiClientRateLimitError(NOAASolarApiClientError):
    """Raised when API rate limiting is encountered."""

    def __init__(self, message: str, retry_after: int | None = None) -> None:
        """Initialize rate-limit error details."""
        super().__init__(message)
        self.retry_after = retry_after


class NOAASpaceApi:
    """NOAA API implementation."""

    def __init__(self, url: str, session: aiohttp.ClientSession) -> None:
        """Initialize NOAA space api."""
        # NOAA API always returns Cache-Control max-age:60, respect it and don't load their systems
        self._cache: TTLCache[str, Any] = TTLCache(maxsize=5, ttl=60)
        self._url = url.rstrip("/")
        self._session = session
        self._request_timeout_seconds = 20

    async def fetch_solar_wind_mag_field(self) -> Any:
        """Fetch solar wind mag data."""
        json = await self.get_json(
            self._url + "/products/summary/solar-wind-mag-field.json"
        )
        return json

    async def fetch_solar_wind_speed(self) -> Any:
        """Fetch solar wind speed data."""
        json = await self.get_json(
            self._url + "/products/summary/solar-wind-speed.json"
        )
        return json

    async def fetch_solar_activity_10_cm_flux(self) -> Any:
        """Fetch solar activity (10cm flux) data."""
        json = await self.get_json(self._url + "/products/summary/10cm-flux.json")
        return json

    async def fetch_suvi_primary_304_image(self) -> bytes:
        """Fetch suvi primary 304 image."""
        image = await self.get_image(
            self._url + "/images/animations/suvi/primary/304/latest.png"
        )
        return image

    async def fetch_lasco_c3_image(self) -> bytes:
        """Fetch lasco c3 image."""
        image = await self.get_image(
            self._url + "/images/animations/lasco-c3/latest.jpg"
        )
        return image

    def default_json_headers(self) -> dict[str, str]:
        """Prepare default request headers for fetching data from noaa api."""
        return {
            "Accept": "application/json",
            "User-Agent": "Home Assistant NOAA Solar Integration",
        }

    def default_image_headers(self) -> dict[str, str]:
        """Prepare default request headers for fetching data from noaa api."""
        return {
            "Accept": "image/png",
            "User-Agent": "Home Assistant NOAA Solar Integration",
        }

    async def get_json(self, url: str) -> Any:
        """HTTP request helper method."""
        cached = self._cache.get(url)
        if cached is not None:
            return cached

        try:
            async with asyncio.timeout(self._request_timeout_seconds):
                async with self._session.get(
                    url,
                    headers=self.default_json_headers(),
                ) as resp:
                    self._raise_for_status(url, resp)
                    json = await resp.json()
                    self._cache[url] = json
                    return json
        except TimeoutError as err:
            raise NOAASolarApiClientCommunicationError(
                f"Timeout while requesting {url}"
            ) from err
        except aiohttp.ClientError as err:
            raise NOAASolarApiClientCommunicationError(
                f"Error while requesting {url}: {err}"
            ) from err

    async def get_image(self, url: str) -> bytes:
        """HTTP request helper method."""
        cached = self._cache.get(url)
        if cached is not None:
            return cached

        try:
            async with asyncio.timeout(self._request_timeout_seconds):
                async with self._session.get(
                    url,
                    headers=self.default_image_headers(),
                ) as resp:
                    self._raise_for_status(url, resp)
                    data = await resp.read()
                    self._cache[url] = data
                    return data
        except TimeoutError as err:
            raise NOAASolarApiClientCommunicationError(
                f"Timeout while requesting {url}"
            ) from err
        except aiohttp.ClientError as err:
            raise NOAASolarApiClientCommunicationError(
                f"Error while requesting {url}: {err}"
            ) from err

    def _raise_for_status(self, url: str, response: aiohttp.ClientResponse) -> None:
        """Map HTTP statuses to integration-specific exceptions."""
        if response.status in (401, 403):
            raise NOAASolarApiClientAuthenticationError(
                f"Authentication failed for {url} with status {response.status}"
            )

        if response.status == 429:
            retry_after_header = response.headers.get("Retry-After")
            retry_after = (
                int(retry_after_header)
                if retry_after_header is not None and retry_after_header.isdigit()
                else None
            )
            raise NOAASolarApiClientRateLimitError(
                f"Rate limited by {url}",
                retry_after=retry_after,
            )

        if response.status >= 400:
            raise NOAASolarApiClientCommunicationError(
                f"Error retrieving data from {url}. Status code {response.status}"
            )
