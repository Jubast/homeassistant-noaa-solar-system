"""Platform for sensor integration."""
from __future__ import annotations
import logging

from . import (
    NOAASolarUpdateCoordinator,
    NOAASolarActivityUpdateCoordinator,
    NOAASolarMagFieldUpdateCoordinator,
    NOAASolarWindSpeedUpdateCoordinator,
    NOAASolarSuvi304UpdateCoordinator,
    NOAASolarLascoC3UpdateCoordinator,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.camera import Camera
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add entities."""
    _LOGGER.info("Setup NOAA Space Sensor Entities")

    coordinators: dict[str, NOAASolarUpdateCoordinator] = hass.data[DOMAIN][
        entry.entry_id
    ]

    for _, coordinator in coordinators.items():
        if isinstance(coordinator, NOAASolarMagFieldUpdateCoordinator):
            async_add_entities([NOAASolarMagFieldBtEntity(coordinator)], True)
            async_add_entities([NOAASolarMagFieldBzEntity(coordinator)], True)

        if isinstance(coordinator, NOAASolarWindSpeedUpdateCoordinator):
            async_add_entities([NOAASolarWindSpeedEntity(coordinator)], True)

        if isinstance(coordinator, NOAASolarActivityUpdateCoordinator):
            async_add_entities([NOAASolarActivityEntity(coordinator)], True)

        if isinstance(coordinator, NOAASolarSuvi304UpdateCoordinator):
            async_add_entities([NOAASolarSuvi304Entity(coordinator)], True)

        if isinstance(coordinator, NOAASolarLascoC3UpdateCoordinator):
            async_add_entities([NOAASolarLascoC3Entity(coordinator)], True)


class NOAASolarWindSpeedEntity(CoordinatorEntity):
    """Representation of solar data."""

    def __init__(self, coordinator: NOAASolarWindSpeedUpdateCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "NOAA Space Weather - Solar Wind Speed"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self.coordinator.data["WindSpeed"]

    @property
    def unit_of_measurement(self) -> str:
        """Return unit of measurement."""
        return "km/sec"


class NOAASolarMagFieldBtEntity(CoordinatorEntity):
    """Representation of solar data."""

    def __init__(self, coordinator: NOAASolarMagFieldUpdateCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "NOAA Space Weather - Solar Wind Magnetic Fields Bt"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self.coordinator.data["Bt"]

    @property
    def unit_of_measurement(self) -> str:
        """Return unit of measurement."""
        return "nT"


class NOAASolarMagFieldBzEntity(CoordinatorEntity):
    """Representation of solar data."""

    def __init__(self, coordinator: NOAASolarMagFieldUpdateCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "NOAA Space Weather - Solar Wind Magnetic Fields Bz"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self.coordinator.data["Bz"]

    @property
    def unit_of_measurement(self) -> str:
        """Return unit of measurement."""
        return "nT"


class NOAASolarActivityEntity(CoordinatorEntity):
    """Representation of solar data."""

    def __init__(self, coordinator: NOAASolarActivityUpdateCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "NOAA Space Weather - Solar Activity (10.7cm Flux)"

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self.coordinator.data["Flux"]

    @property
    def unit_of_measurement(self) -> str:
        """Return unit of measurement."""
        return "sfu"


class NOAASolarSuvi304Entity(CoordinatorEntity):
    """Representation of solar data."""

    def __init__(self, coordinator: NOAASolarSuvi304UpdateCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "NOAA Space Weather - Suvi 304 Image"

    @property
    def state(self) -> int | None:
        """Return the state of the sensor."""
        return None


class NOAASolarLascoC3Entity(CoordinatorEntity):
    """Representation of solar data."""

    def __init__(self, coordinator: NOAASolarLascoC3UpdateCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "NOAA Space Weather - Lasco C3 Image"

    @property
    def state(self) -> int | None:
        """Return the state of the sensor."""
        return None
