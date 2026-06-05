"""Platform for image integration."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.image import ImageEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import (
    NOAASolarLascoC3UpdateCoordinator,
    NOAASolarSuvi304UpdateCoordinator,
)
from .const import LOGGER
from .data import NOAASolarConfigEntry
from .entity import NOAASolarEntity
from .utils.image_utils import read_image_bytes_from_disk


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: NOAASolarConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add NOAA Solar Image entities."""
    LOGGER.info("Setup NOAA Space Image Entities")

    coordinators = entry.runtime_data.coordinators

    for _, coordinator in coordinators.items():
        if isinstance(coordinator, NOAASolarSuvi304UpdateCoordinator):
            async_add_entities([NOAASolarSuvi304Entity(hass, coordinator)], True)

        if isinstance(coordinator, NOAASolarLascoC3UpdateCoordinator):
            async_add_entities([NOAASolarLascoC3Entity(hass, coordinator)], True)


class NOAASolarSuvi304Entity(ImageEntity, NOAASolarEntity):
    """Representation of NOAA Suvi304 Primary images."""

    def __init__(
        self, hass: HomeAssistant, coordinator: NOAASolarSuvi304UpdateCoordinator
    ) -> None:
        """Initialize the NOAA Solar Suvi304 Image entity."""
        ImageEntity.__init__(self, hass)
        NOAASolarEntity.__init__(self, coordinator, unique_id_suffix="suvi_304_image")
        self._attr_name = "NOAA Space Weather - Suvi 304 Image"

    @property
    def content_type(self) -> str:
        """Return the content type."""
        return "image/png"

    @property
    def image_last_updated(self) -> datetime | None:
        """The time when the latest frame was downloaded."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("latest_image_updated")

    async def async_image(self) -> bytes | None:
        """Return bytes of the latest downloaded frame."""
        if not self.coordinator.data:
            return None
        latest = self.coordinator.data.get("latest_image")
        if latest is None:
            return None
        try:
            return await self.hass.async_add_executor_job(
                read_image_bytes_from_disk, latest
            )
        except FileNotFoundError:
            return None


class NOAASolarLascoC3Entity(ImageEntity, NOAASolarEntity):
    """Representation of NOAA LascoC3 Primary images."""

    def __init__(
        self, hass: HomeAssistant, coordinator: NOAASolarLascoC3UpdateCoordinator
    ) -> None:
        """Initialize the NOAA Solar LascoC3 entity."""
        ImageEntity.__init__(self, hass)
        NOAASolarEntity.__init__(self, coordinator, unique_id_suffix="lasco_c3_image")
        self._attr_name = "NOAA Space Weather - Lasco C3 Image"

    @property
    def content_type(self) -> str:
        """Return the content type."""
        return "image/png"

    @property
    def image_last_updated(self) -> datetime | None:
        """The time when the latest frame was downloaded."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("latest_image_updated")

    async def async_image(self) -> bytes | None:
        """Return bytes of the latest downloaded frame."""
        if not self.coordinator.data:
            return None
        latest = self.coordinator.data.get("latest_image")
        if latest is None:
            return None
        try:
            return await self.hass.async_add_executor_job(
                read_image_bytes_from_disk, latest
            )
        except FileNotFoundError:
            return None
