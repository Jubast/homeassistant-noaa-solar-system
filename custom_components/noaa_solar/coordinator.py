"""The NOAA Solar integration."""

from __future__ import annotations
from abc import abstractmethod
from datetime import timedelta, datetime
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import NOAASpaceApi
from .utils.image_utils import save_frame_to_disk
from .utils.video_utils import Video, create_video
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


class NOAASolarVideoUpdateCoordinator(NOAASolarUpdateCoordinator):
    """Update handler for videos."""

    def __init__(
        self,
        hass: HomeAssistant,
        video_format: str,
        update_interval: timedelta,
        api: NOAASpaceApi,
    ) -> None:
        """Initialize global data updater."""
        self.video_format = video_format

        super().__init__(hass, update_interval, api)

    @abstractmethod
    async def _fetch_data(self):
        """Fetch the actual data."""
        raise NotImplementedError


class NOAASolarSuvi304UpdateCoordinator(NOAASolarVideoUpdateCoordinator):
    """Update handler."""

    async def _fetch_data(self):
        """Fetch new data."""
        current_video: Video = self.data
        image = await self.api.fetch_suvi_primary_304_image()

        video_frame = save_frame_to_disk(image, SUVI_304_IMAGES_DIRECTORY)

        # nothing new, return created state
        if current_video and not video_frame.saved:
            return current_video

        # handle case where gif was not yet created
        if not current_video:
            video = create_video(
                self.video_format, SUVI_304_IMAGES_DIRECTORY, video_frame.file_datetime
            )
            return video

        # check if a gif update is due
        # (this is for perf reasons, no need to create a >10MB gif every 2 minutes..)
        next_update_datetime = current_video.created + timedelta(hours=12)
        if datetime.now() > next_update_datetime:
            video = create_video(
                self.video_format, SUVI_304_IMAGES_DIRECTORY, video_frame.file_datetime
            )
            return video

        return current_video


class NOAASolarLascoC3UpdateCoordinator(NOAASolarVideoUpdateCoordinator):
    """Update handler."""

    async def _fetch_data(self):
        """Fetch new data."""
        current_video: Video = self.data
        image = await self.api.fetch_lasco_c3_image()

        video_frame = save_frame_to_disk(image, LASCO_C3_IMAGES_DIRECTORY)

        # nothing new, return created state
        if current_video and not video_frame.saved:
            return current_video

        # handle case where gif was not yet created
        if not current_video:
            video = create_video(
                self.video_format, LASCO_C3_IMAGES_DIRECTORY, video_frame.file_datetime
            )
            return video

        # check if a gif update is due
        # (this is for perf reasons, no need to create a >10MB gif every 2 minutes..)
        next_update_datetime = current_video.created + timedelta(hours=12)
        if datetime.now() > next_update_datetime:
            video = create_video(
                self.video_format, LASCO_C3_IMAGES_DIRECTORY, video_frame.file_datetime
            )
            return video

        return current_video
