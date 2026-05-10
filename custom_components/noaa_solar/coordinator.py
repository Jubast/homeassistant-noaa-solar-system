"""The NOAA Solar integration."""

from __future__ import annotations
import os
from abc import abstractmethod
from datetime import timedelta, datetime
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import NOAASpaceApi
from .utils.image_utils import save_frame_to_disk
from .utils.video_utils import create_video

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
        data = await self.api.fetch_solar_wind_mag_field()
        entry = data[0]
        return {"Bt": entry["bt"], "Bz": entry["bz_gsm"]}


class NOAASolarWindSpeedUpdateCoordinator(NOAASolarUpdateCoordinator):
    """Update handler."""

    async def _fetch_data(self):
        """Fetch new data."""
        data = await self.api.fetch_solar_wind_speed()
        return {"WindSpeed": data[0]["proton_speed"]}


class NOAASolarActivityUpdateCoordinator(NOAASolarUpdateCoordinator):
    """Update handler."""

    async def _fetch_data(self):
        """Fetch new data."""
        data = await self.api.fetch_solar_activity_10_cm_flux()
        return {"Flux": data[0]["flux"]}


class NOAASolarVideoUpdateCoordinator(NOAASolarUpdateCoordinator):
    """Update handler for videos."""

    stream_name: str  # defined by each subclass

    def __init__(
        self,
        hass: HomeAssistant,
        video_format: str,
        image_directory: str,
        video_directory: str,
        update_interval: timedelta,
        api: NOAASpaceApi,
    ) -> None:
        """Initialize global data updater."""
        self.video_format = video_format
        self.image_directory = image_directory
        self.video_directory = video_directory
        self._video_created: datetime | None = None

        super().__init__(hass, update_interval, api)

    def _video_path(self) -> str:
        ext = "mp4" if self.video_format == "MP4" else "gif"
        return os.path.join(self.video_directory, f"{self.stream_name}.{ext}")

    @abstractmethod
    async def _fetch_data(self):
        """Fetch the actual data."""
        raise NotImplementedError


class NOAASolarSuvi304UpdateCoordinator(NOAASolarVideoUpdateCoordinator):
    """Update handler."""

    stream_name = "suvi_304"

    async def _fetch_data(self):
        """Fetch new data."""
        image = await self.api.fetch_suvi_primary_304_image()

        video_frame = save_frame_to_disk(image, self.image_directory)

        needs_video = self._video_created is None or (
            video_frame.saved
            and datetime.now() > self._video_created + timedelta(hours=12)
        )
        video_path = self._video_path()
        if needs_video:
            create_video(self.video_format, self.image_directory, video_path)
            self._video_created = datetime.now()

        return {
            "latest_image": os.path.join(self.image_directory, "latest.png"),
            "latest_image_updated": (
                video_frame.file_datetime
                if video_frame.saved
                else (self.data or {}).get("latest_image_updated")
            ),
            "latest_video": video_path,
        }


class NOAASolarLascoC3UpdateCoordinator(NOAASolarVideoUpdateCoordinator):
    """Update handler."""

    stream_name = "lasco_c3"

    async def _fetch_data(self):
        """Fetch new data."""
        image = await self.api.fetch_lasco_c3_image()

        video_frame = save_frame_to_disk(image, self.image_directory)

        needs_video = self._video_created is None or (
            video_frame.saved
            and datetime.now() > self._video_created + timedelta(hours=12)
        )
        video_path = self._video_path()
        if needs_video:
            create_video(self.video_format, self.image_directory, video_path)
            self._video_created = datetime.now()

        return {
            "latest_image": os.path.join(self.image_directory, "latest.png"),
            "latest_image_updated": (
                video_frame.file_datetime
                if video_frame.saved
                else (self.data or {}).get("latest_image_updated")
            ),
            "latest_video": video_path,
        }
