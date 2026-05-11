"""Shared entity definitions for NOAA Solar."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DEFAULT_NAME, DEVICE_MANUFACTURER, DEVICE_MODEL
from .coordinator import NOAASolarUpdateCoordinator


class NOAASolarEntity(CoordinatorEntity[NOAASolarUpdateCoordinator]):
    """Base NOAA Solar entity."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: NOAASolarUpdateCoordinator,
        *,
        unique_id_suffix: str | None = None,
    ) -> None:
        """Initialize the shared NOAA entity state."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
            name=coordinator.config_entry.title or DEFAULT_NAME,
            manufacturer=DEVICE_MANUFACTURER,
            model=DEVICE_MODEL,
        )
        if unique_id_suffix is not None:
            self._attr_unique_id = (
                f"{coordinator.config_entry.entry_id}_{unique_id_suffix}"
            )
