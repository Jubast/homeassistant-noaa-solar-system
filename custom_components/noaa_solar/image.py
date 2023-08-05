"""Platform for image integration."""
from __future__ import annotations
from datetime import datetime
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.components.image import ImageEntity

from .coordinator import (
    NOAASolarUpdateCoordinator,
    NOAASolarSuvi304UpdateCoordinator,
    NOAASolarLascoC3UpdateCoordinator,
)

from .utils.gif_utils import Gif

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add NOAA Solar Image entities."""
    _LOGGER.info("Setup NOAA Space Image Entities")

    coordinators: dict[str, NOAASolarUpdateCoordinator] = hass.data[DOMAIN][
        entry.entry_id
    ]

    for _, coordinator in coordinators.items():
        if isinstance(coordinator, NOAASolarSuvi304UpdateCoordinator):
            async_add_entities([NOAASolarSuvi304Entity(hass, coordinator)], True)

        if isinstance(coordinator, NOAASolarLascoC3UpdateCoordinator):
            async_add_entities([NOAASolarLascoC3Entity(hass, coordinator)], True)


class NOAASolarSuvi304Entity(ImageEntity, CoordinatorEntity):
    """Representation of NOAA Suvi304 Primary images."""

    def __init__(
        self, hass: HomeAssistant, coordinator: NOAASolarSuvi304UpdateCoordinator
    ) -> None:
        """Initialize the NOAA Solar Suvi304 Image entity."""
        ImageEntity.__init__(self, hass)
        CoordinatorEntity.__init__(self, coordinator)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "NOAA Space Weather - Suvi 304 Image"

    @property
    def content_type(self) -> str:
        """Image content type."""
        return "image/gif"

    @property
    def image_last_updated(self) -> datetime | None:
        """The time when the image was last updated."""
        gif: Gif = self.coordinator.data
        if not gif:
            return None

        return gif.created

    def image(self) -> bytes | None:
        """Return bytes of image."""
        gif: Gif = self.coordinator.data
        if not gif:
            return None

        return gif.data


class NOAASolarLascoC3Entity(ImageEntity, CoordinatorEntity):
    """Representation of NOAA LascoC3 Primary images."""

    def __init__(
        self, hass: HomeAssistant, coordinator: NOAASolarLascoC3UpdateCoordinator
    ) -> None:
        """Initialize the NOAA Solar LascoC3 entity."""
        ImageEntity.__init__(self, hass)
        CoordinatorEntity.__init__(self, coordinator)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "NOAA Space Weather - Lasco C3 Image"

    @property
    def content_type(self) -> str:
        """Image content type."""
        return "image/gif"

    @property
    def image_last_updated(self) -> datetime | None:
        """The time when the image was last updated."""
        gif: Gif = self.coordinator.data
        if not gif:
            return None

        return gif.created

    def image(self) -> bytes | None:
        """Return bytes of image."""
        gif: Gif = self.coordinator.data
        if not gif:
            return None

        return gif.data
