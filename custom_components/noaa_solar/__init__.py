"""The NOAA Solar integration."""

from __future__ import annotations
import os
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_HOST, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import NOAASpaceApi
from .coordinator import (
    NOAASolarActivityUpdateCoordinator,
    NOAASolarMagFieldUpdateCoordinator,
    NOAASolarUpdateCoordinator,
    NOAASolarWindSpeedUpdateCoordinator,
    NOAASolarSuvi304UpdateCoordinator,
    NOAASolarLascoC3UpdateCoordinator,
)
from .data import NOAASolarConfigEntry, NOAASolarData

from .const import (
    CONF_DATA_SCAN_INTERVAL,
    CONF_IMAGE_SCAN_INTERVAL,
    CONF_VIDEO_FORMAT,
    DEFAULT_IMAGE_SCAN_INTERVAL,
    LOGGER,
)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.IMAGE]


async def async_setup_entry(hass: HomeAssistant, entry: NOAASolarConfigEntry) -> bool:
    """Set up NOAA Solar from a config entry."""
    LOGGER.info("Setup NOAA Space API Coordinators")

    api_host = entry.data[CONF_HOST]
    api_data_interval = timedelta(seconds=entry.data[CONF_DATA_SCAN_INTERVAL])
    api_image_interval = timedelta(seconds=entry.data[CONF_IMAGE_SCAN_INTERVAL])
    video_format = entry.data[CONF_VIDEO_FORMAT]

    api = NOAASpaceApi(api_host, async_get_clientsession(hass))

    local_media_dir = hass.config.media_dirs.get("local")
    if local_media_dir is None:
        raise ConfigEntryNotReady(
            "No 'local' media source configured. Add 'media_dirs: local: /path/to/media'"
            " to your Home Assistant configuration.yaml."
        )
    noaa_media_dir = os.path.join(local_media_dir, "noaa_solar")
    images_dir = os.path.join(noaa_media_dir, "images")
    videos_dir = os.path.join(noaa_media_dir, "videos")

    coordinators: dict[str, NOAASolarUpdateCoordinator] = {
        "mag_field": NOAASolarMagFieldUpdateCoordinator(hass, api_data_interval, api),
        "wind_speed": NOAASolarWindSpeedUpdateCoordinator(hass, api_data_interval, api),
        "activity": NOAASolarActivityUpdateCoordinator(hass, api_data_interval, api),
        "suvi_304": NOAASolarSuvi304UpdateCoordinator(
            hass,
            video_format,
            os.path.join(images_dir, "suvi_304"),
            videos_dir,
            api_image_interval,
            api,
        ),
        "lasco_c3": NOAASolarLascoC3UpdateCoordinator(
            hass,
            video_format,
            os.path.join(images_dir, "lasco_c3"),
            videos_dir,
            api_image_interval,
            api,
        ),
    }

    for coordinator in coordinators.values():
        await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = NOAASolarData(api=api, coordinators=coordinators)

    LOGGER.info(
        "NOAA Solar media available via HA media browser: local/noaa_solar/videos/",
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: NOAASolarConfigEntry) -> bool:
    """Unload a config entry."""
    LOGGER.info("Unload NOAA Space API Coordinators")

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: NOAASolarConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Migrations for config flow configuration."""

    if config_entry.version == 1:
        LOGGER.info("Migrating NOAA Solar integration from version 1 to 2")

        new_data = {**config_entry.data}
        new_data[CONF_DATA_SCAN_INTERVAL] = config_entry.data[CONF_SCAN_INTERVAL]
        new_data[CONF_IMAGE_SCAN_INTERVAL] = DEFAULT_IMAGE_SCAN_INTERVAL
        new_data.pop(CONF_SCAN_INTERVAL)
        config_entry.version = 2
        hass.config_entries.async_update_entry(config_entry, data=new_data)

    if config_entry.version == 2:
        LOGGER.info("Migrating NOAA Solar integration from version 2 to 3")

        new_data = {**config_entry.data}
        # Default to "GIF" to preserve previous behaviour for existing users.
        # New installations use DEFAULT_VIDEO_FORMAT ("MP4").
        new_data.setdefault(CONF_VIDEO_FORMAT, "GIF")
        config_entry.version = 3
        hass.config_entries.async_update_entry(config_entry, data=new_data)

    return True
