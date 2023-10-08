"""Platform for sensor integration."""
from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .coordinator import (
    NOAASolarUpdateCoordinator,
    NOAASolarActivityUpdateCoordinator,
    NOAASolarMagFieldUpdateCoordinator,
    NOAASolarWindSpeedUpdateCoordinator,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add NOAA Solar Sensor entities."""
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


class NOAASolarWindSpeedEntity(CoordinatorEntity):
    """Representation of NOAA Solar wind speed data."""

    def __init__(self, coordinator: NOAASolarWindSpeedUpdateCoordinator) -> None:
        """Initialize the NOAA Solar wind speed entity."""
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
    """Representation NOAA Solar Magnetic Fields Bt data."""

    def __init__(self, coordinator: NOAASolarMagFieldUpdateCoordinator) -> None:
        """Initialize the NOAA Solar Magnetic Fields Bt entity."""
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
    """Representation NOAA Solar Magnetic Fields Bz data."""

    def __init__(self, coordinator: NOAASolarMagFieldUpdateCoordinator) -> None:
        """Initialize the NOAA Solar Magnetic fields Bz entity."""
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
    """Representation NOAA Solar activity data."""

    def __init__(self, coordinator: NOAASolarActivityUpdateCoordinator) -> None:
        """Initialize the NOAA Solar activity entity."""
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
