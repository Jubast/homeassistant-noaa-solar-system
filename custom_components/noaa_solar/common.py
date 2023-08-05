"""Common data for the NOAA Solar integration."""

from os.path import join, dirname

INTEGRATION_DATA_DIRECTORY = join(dirname(__file__), "data")
IMAGES_DIRECTORY = join(INTEGRATION_DATA_DIRECTORY, "images")
SUVI_304_IMAGES_DIRECTORY = join(IMAGES_DIRECTORY, "suvi_304")
LASCO_C3_IMAGES_DIRECTORY = join(IMAGES_DIRECTORY, "lasco_c3")
