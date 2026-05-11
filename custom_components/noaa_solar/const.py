"""Constants for the NOAA Solar integration."""

from logging import Logger, getLogger
from typing import Final

LOGGER: Logger = getLogger(__package__)

DOMAIN = "noaa_solar"
ATTRIBUTION = "Data provided by NOAA Space Weather Prediction Center"
DEVICE_MANUFACTURER = "NOAA"
DEVICE_MODEL = "Solar System"

# Default config for solar system scraper.
DEFAULT_HOST = "https://services.swpc.noaa.gov/"
DEFAULT_NAME = "NOAA Solar"
DEFAULT_DATA_SCAN_INTERVAL = 60  # seconds
DEFAULT_IMAGE_SCAN_INTERVAL = 3600  # seconds
DEFAULT_VIDEO_FORMAT = "MP4"

# Configuration defaults
CONF_DATA_SCAN_INTERVAL: Final = "data_scan_interval"
CONF_IMAGE_SCAN_INTERVAL: Final = "image_scan_interval"
CONF_VIDEO_FORMAT: Final = "video_format"
