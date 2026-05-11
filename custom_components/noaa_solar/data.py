"""Typed data stored for NOAA Solar config entries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from .api import NOAASpaceApi
    from .coordinator import NOAASolarUpdateCoordinator


type NOAASolarConfigEntry = ConfigEntry[NOAASolarData]


@dataclass
class NOAASolarData:
    """Runtime data for the NOAA Solar integration."""

    api: NOAASpaceApi
    coordinators: dict[str, NOAASolarUpdateCoordinator]
