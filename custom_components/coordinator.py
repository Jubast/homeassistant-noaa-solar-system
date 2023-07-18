"""The Solar System Scraper integration."""
from __future__ import annotations
from abc import abstractmethod
from datetime import timedelta
import logging
from typing import Any

import aiohttp
from asyncio import create_task

from cachetools import TTLCache
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_SCAN_INTERVAL

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .utils.gif_utils import save_png_gif_frame, create_gif, save_gif
from .common import (
    SUVI_304_IMAGES_DIRECTORY,
    LASCO_C3_IMAGES_DIRECTORY,
    SUVI_304_GIF_NAME,
    LASCO_C3_GIF_NAME,
    WWW_SOLARSYSTEM_GIFS_DIRECTORY,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class NOAASolarUpdateCoordinator(DataUpdateCoordinator):
    """Update handler."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, api: NOAASpaceApi
    ) -> None:
        """Initialize global data updater."""
        self.api = api

        update_interval = timedelta(seconds=entry.data[CONF_SCAN_INTERVAL])

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def _async_update_data(self):
        """Get the latest data from NOAA."""
        return await self._fetch_data()

    @abstractmethod
    async def _fetch_data(self):
        """Fetch the actual data."""
        raise NotImplementedError


class NOAASolarMagFieldUpdateCoordinator(NOAASolarUpdateCoordinator):
    """Update handler."""

    async def _fetch_data(self):
        """Fetch new data."""
        return await self.api.fetch_solar_wind_mag_field()


class NOAASolarWindSpeedUpdateCoordinator(NOAASolarUpdateCoordinator):
    """Update handler."""

    async def _fetch_data(self):
        """Fetch new data."""
        return await self.api.fetch_solar_wind_speed()


class NOAASolarActivityUpdateCoordinator(NOAASolarUpdateCoordinator):
    """Update handler."""

    async def _fetch_data(self):
        """Fetch new data."""
        return await self.api.fetch_solar_activity_10_cm_flux()


class NOAASolarSuvi304UpdateCoordinator(NOAASolarUpdateCoordinator):
    """Update handler."""

    async def _fetch_data(self):
        """Fetch new data."""
        image = await self.api.fetch_suvi_primary_304_image()
        saved = save_png_gif_frame(image, SUVI_304_IMAGES_DIRECTORY)

        if not saved:
            return None

        gif = create_gif(SUVI_304_IMAGES_DIRECTORY)
        gif_directory = self.hass.config.path(WWW_SOLARSYSTEM_GIFS_DIRECTORY)
        save_gif(gif_directory, SUVI_304_GIF_NAME, gif)

        return None


class NOAASolarLascoC3UpdateCoordinator(NOAASolarUpdateCoordinator):
    """Update handler."""

    async def _fetch_data(self):
        """Fetch new data."""
        image = await self.api.fetch_lasco_c3_image()
        saved = save_png_gif_frame(image, LASCO_C3_IMAGES_DIRECTORY)

        if not saved:
            return None

        gif = create_gif(LASCO_C3_IMAGES_DIRECTORY)
        gif_directory = self.hass.config.path(WWW_SOLARSYSTEM_GIFS_DIRECTORY)
        save_gif(gif_directory, LASCO_C3_GIF_NAME, gif)

        return None


class NOAASpaceApi:
    """NOAA API implementation"""

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize NOAA space api."""
        # NOAA API always returns Cache-Control max-age:60, respect it and don't load their systems
        self.cache = TTLCache(maxsize=5, ttl=60)
        self.url = entry.data[CONF_HOST]

    async def fetch_solar_wind_mag_field(self) -> Any:
        """Fetches solar wind mag"""
        json = await self.get_json(
            self.url + "/products/summary/solar-wind-mag-field.json"
        )
        return json

    async def fetch_solar_wind_speed(self) -> Any:
        """Fetches solar wind speed"""
        json = await self.get_json(self.url + "/products/summary/solar-wind-speed.json")
        return json

    async def fetch_solar_activity_10_cm_flux(self) -> Any:
        """Fetches solar activity (10cm flux)"""
        json = await self.get_json(self.url + "/products/summary/10cm-flux.json")
        return json

    async def fetch_suvi_primary_304_image(self) -> bytes:
        """Fetches suvi primary 304 image"""
        image = await self.get_image(
            self.url + "/images/animations/suvi/primary/304/latest.png"
        )
        return image

    async def fetch_lasco_c3_image(self) -> bytes:
        """Fetches lasco c3 image"""
        image = await self.get_image(
            self.url + "/images/animations/lasco-c3/latest.jpg"
        )
        return image

    def default_json_headers(self):
        """Provides default request headers for fetching data from noaa api"""
        return {
            "Accept": "application/json",
            "User-Agent": "Home Assistant Integration",
        }

    def default_image_headers(self):
        """Provides default request headers for fetching data from noaa api"""
        return {"Accept": "image/png", "User-Agent": "Home Assistant Integration"}

    async def get_json(self, url: str) -> Any:
        """HTTP request helper method"""
        cached = self.cache.get(url)
        if cached:
            return cached

        async with aiohttp.ClientSession() as session:
            async with session.get(
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
        """HTTP request helper method"""
        cached = self.cache.get(url)
        if cached:
            return cached

        async with aiohttp.ClientSession() as session:
            async with session.get(
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
