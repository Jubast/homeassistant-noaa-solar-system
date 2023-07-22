"""Common data for the NOAA Solar integration."""

from os.path import join, dirname

INTEGRATION_DATA_DIRECTORY = join(dirname(__file__), "data")
IMAGES_DIRECTORY = join(INTEGRATION_DATA_DIRECTORY, "images")
SUVI_304_IMAGES_DIRECTORY = join(IMAGES_DIRECTORY, "suvi_304")
LASCO_C3_IMAGES_DIRECTORY = join(IMAGES_DIRECTORY, "lasco_c3")

SUVI_304_GIF_NAME = "suvi_304.gif"
LASCO_C3_GIF_NAME = "lasco_c3.gif"

WWW_SOLARSYSTEM_DIRECTORY = join("www", "community", "solarsystem")
WWW_SOLARSYSTEM_GIFS_DIRECTORY = join(WWW_SOLARSYSTEM_DIRECTORY, "gifs")
