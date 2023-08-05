"""The NOAA Solar integration."""
from __future__ import annotations
import logging
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_HOST, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant

from .api import NOAASpaceApi
from .coordinator import (
    NOAASolarActivityUpdateCoordinator,
    NOAASolarMagFieldUpdateCoordinator,
    NOAASolarUpdateCoordinator,
    NOAASolarWindSpeedUpdateCoordinator,
    NOAASolarSuvi304UpdateCoordinator,
    NOAASolarLascoC3UpdateCoordinator,
)

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.IMAGE]
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Solar System Scraper from a config entry."""
    _LOGGER.info("Setup NOAA Space API Coordinators")

    api_host = entry.data[CONF_HOST]
    api_interval = timedelta(seconds=entry.data[CONF_SCAN_INTERVAL])

    api = NOAASpaceApi(api_host)

    coordinators: dict[str, NOAASolarUpdateCoordinator] = {
        "mag_field": NOAASolarMagFieldUpdateCoordinator(hass, api_interval, api),
        "wind_speed": NOAASolarWindSpeedUpdateCoordinator(hass, api_interval, api),
        "activity": NOAASolarActivityUpdateCoordinator(hass, api_interval, api),
        "suvi_304": NOAASolarSuvi304UpdateCoordinator(hass, api_interval, api),
        "lasco_c3": NOAASolarLascoC3UpdateCoordinator(hass, api_interval, api),
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
