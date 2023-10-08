"""Constants for the NOAA Solar integration."""

from typing import Final


DOMAIN = "noaa_solar"

# Default config for solar system scraper.
DEFAULT_HOST = "https://services.swpc.noaa.gov/"
DEFAULT_NAME = "NOAA Solar"
DEFAULT_DATA_SCAN_INTERVAL = 60  # seconds
DEFAULT_IMAGE_SCAN_INTERVAL = 3600  # seconds

# Configuration defaults
CONF_DATA_SCAN_INTERVAL: Final = "data_scan_interval"
CONF_IMAGE_SCAN_INTERVAL: Final = "image_scan_interval"
