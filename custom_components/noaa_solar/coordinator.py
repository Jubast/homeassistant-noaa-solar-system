"""The NOAA Solar integration."""
from __future__ import annotations
from abc import abstractmethod
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import NOAASpaceApi
from .utils.gif_utils import save_png_gif_frame, create_gif, Gif
from .common import SUVI_304_IMAGES_DIRECTORY, LASCO_C3_IMAGES_DIRECTORY

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class NOAASolarUpdateCoordinator(DataUpdateCoordinator):
    """Update handler."""

    def __init__(
        self, hass: HomeAssistant, update_interval: timedelta, api: NOAASpaceApi
    ) -> None:
        """Initialize global data updater."""
        self.api = api

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
        gif_frame = save_png_gif_frame(image, SUVI_304_IMAGES_DIRECTORY)

        if not gif_frame.saved:
            return self.data

        gif_data = create_gif(SUVI_304_IMAGES_DIRECTORY)
        gif = Gif(gif_data, gif_frame.file_datetime)

        return gif


class NOAASolarLascoC3UpdateCoordinator(NOAASolarUpdateCoordinator):
    """Update handler."""

    async def _fetch_data(self):
        """Fetch new data."""
        image = await self.api.fetch_lasco_c3_image()
        gif_frame = save_png_gif_frame(image, LASCO_C3_IMAGES_DIRECTORY)

        if not gif_frame.saved:
            return self.data

        gif_data = create_gif(LASCO_C3_IMAGES_DIRECTORY)
        gif = Gif(gif_data, gif_frame.file_datetime)

        return gif
