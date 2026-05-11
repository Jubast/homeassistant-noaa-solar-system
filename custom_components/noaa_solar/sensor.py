"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import (
    NOAASolarActivityUpdateCoordinator,
    NOAASolarMagFieldUpdateCoordinator,
    NOAASolarWindSpeedUpdateCoordinator,
)
from .data import NOAASolarConfigEntry
from .entity import NOAASolarEntity
from .const import LOGGER


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: NOAASolarConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add NOAA Solar Sensor entities."""
    LOGGER.info("Setup NOAA Space Sensor Entities")

    coordinators = entry.runtime_data.coordinators

    for _, coordinator in coordinators.items():
        if isinstance(coordinator, NOAASolarMagFieldUpdateCoordinator):
            async_add_entities([NOAASolarMagFieldBtEntity(coordinator)], True)
            async_add_entities([NOAASolarMagFieldBzEntity(coordinator)], True)

        if isinstance(coordinator, NOAASolarWindSpeedUpdateCoordinator):
            async_add_entities([NOAASolarWindSpeedEntity(coordinator)], True)

        if isinstance(coordinator, NOAASolarActivityUpdateCoordinator):
            async_add_entities([NOAASolarActivityEntity(coordinator)], True)


class NOAASolarWindSpeedEntity(NOAASolarEntity, SensorEntity):
    """Representation of NOAA Solar wind speed data."""

    _attr_name = "NOAA Space Weather - Solar Wind Speed"
    _attr_native_unit_of_measurement = "km/s"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: NOAASolarWindSpeedUpdateCoordinator) -> None:
        """Initialize the NOAA Solar wind speed entity."""
        super().__init__(coordinator, unique_id_suffix="wind_speed")

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data["WindSpeed"]


class NOAASolarMagFieldBtEntity(NOAASolarEntity, SensorEntity):
    """Representation NOAA Solar Magnetic Fields Bt data."""

    _attr_name = "NOAA Space Weather - Solar Wind Magnetic Fields Bt"
    _attr_native_unit_of_measurement = "nT"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: NOAASolarMagFieldUpdateCoordinator) -> None:
        """Initialize the NOAA Solar Magnetic Fields Bt entity."""
        super().__init__(coordinator, unique_id_suffix="mag_field_bt")

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data["Bt"]


class NOAASolarMagFieldBzEntity(NOAASolarEntity, SensorEntity):
    """Representation NOAA Solar Magnetic Fields Bz data."""

    _attr_name = "NOAA Space Weather - Solar Wind Magnetic Fields Bz"
    _attr_native_unit_of_measurement = "nT"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: NOAASolarMagFieldUpdateCoordinator) -> None:
        """Initialize the NOAA Solar Magnetic fields Bz entity."""
        super().__init__(coordinator, unique_id_suffix="mag_field_bz")

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data["Bz"]


class NOAASolarActivityEntity(NOAASolarEntity, SensorEntity):
    """Representation NOAA Solar activity data."""

    _attr_name = "NOAA Space Weather - Solar Activity (10.7cm Flux)"
    _attr_native_unit_of_measurement = "sfu"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: NOAASolarActivityUpdateCoordinator) -> None:
        """Initialize the NOAA Solar activity entity."""
        super().__init__(coordinator, unique_id_suffix="activity_flux")

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        return self.coordinator.data["Flux"]
