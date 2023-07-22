"""The NOAA Solar integration."""
from __future__ import annotations
from datetime import timedelta
import logging

from .coordinator import (
    NOAASolarActivityUpdateCoordinator,
    NOAASolarMagFieldUpdateCoordinator,
    NOAASolarUpdateCoordinator,
    NOAASolarWindSpeedUpdateCoordinator,
    NOAASolarLascoC3UpdateCoordinator,
    NOAASolarSuvi304UpdateCoordinator,
    NOAASpaceApi,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Solar System Scraper from a config entry."""
    _LOGGER.info("Setup NOAA Space API Coordinators")

    api = NOAASpaceApi(entry)

    coordinators: dict[str, NOAASolarUpdateCoordinator] = {
        "mag_field": NOAASolarMagFieldUpdateCoordinator(hass, entry, api),
        "wind_speed": NOAASolarWindSpeedUpdateCoordinator(hass, entry, api),
        "activity": NOAASolarActivityUpdateCoordinator(hass, entry, api),
        "suvi_304": NOAASolarSuvi304UpdateCoordinator(hass, entry, api),
        "lasco_c3": NOAASolarLascoC3UpdateCoordinator(hass, entry, api),
    }

    for coordinator in coordinators.values():
        await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinators
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unload NOAA Space API Coordinators")

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
