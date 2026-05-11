"""Config flow for NOAA Solar integration."""

from __future__ import annotations
from typing import Any, Self

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    DEFAULT_DATA_SCAN_INTERVAL,
    DEFAULT_IMAGE_SCAN_INTERVAL,
    DEFAULT_NAME,
    DEFAULT_HOST,
    DEFAULT_VIDEO_FORMAT,
    DOMAIN,
    CONF_DATA_SCAN_INTERVAL,
    CONF_IMAGE_SCAN_INTERVAL,
    CONF_VIDEO_FORMAT,
)

VIDEO_FORMAT_OPTIONS = ["GIF", "MP4"]


def data_schema(user_input: dict[str, Any]) -> vol.Schema:
    """Prepare data schema for NOAA Solar configuration."""
    return vol.Schema(
        {
            vol.Required(
                CONF_NAME,
                default=user_input.get(CONF_NAME, DEFAULT_NAME),
            ): str,
            vol.Required(
                CONF_HOST, default=user_input.get(CONF_HOST, DEFAULT_HOST)
            ): str,
            vol.Required(
                CONF_DATA_SCAN_INTERVAL,
                default=user_input.get(
                    CONF_DATA_SCAN_INTERVAL, DEFAULT_DATA_SCAN_INTERVAL
                ),
            ): int,
            vol.Required(
                CONF_IMAGE_SCAN_INTERVAL,
                default=user_input.get(
                    CONF_IMAGE_SCAN_INTERVAL, DEFAULT_IMAGE_SCAN_INTERVAL
                ),
            ): int,
            vol.Required(
                CONF_VIDEO_FORMAT,
                default=user_input.get(CONF_VIDEO_FORMAT, DEFAULT_VIDEO_FORMAT),
            ): SelectSelector(
                SelectSelectorConfig(
                    options=VIDEO_FORMAT_OPTIONS,
                    mode=SelectSelectorMode.LIST,
                )
            ),
        }
    )


def default_user_input() -> dict[str, Any]:
    """Prepare default user input."""
    user_input = {}
    user_input[CONF_NAME] = DEFAULT_NAME
    user_input[CONF_HOST] = DEFAULT_HOST
    user_input[CONF_DATA_SCAN_INTERVAL] = DEFAULT_DATA_SCAN_INTERVAL
    user_input[CONF_IMAGE_SCAN_INTERVAL] = DEFAULT_IMAGE_SCAN_INTERVAL
    user_input[CONF_VIDEO_FORMAT] = DEFAULT_VIDEO_FORMAT
    return user_input


def user_input_to_data(user_input: dict[str, Any]) -> Any:
    """Convert user input to config entity data."""
    # set some defaults in case we need to return to the form
    host = user_input.get(CONF_HOST, DEFAULT_HOST)
    data_scan_interval = user_input.get(
        CONF_DATA_SCAN_INTERVAL, DEFAULT_DATA_SCAN_INTERVAL
    )
    image_scan_interval = user_input.get(
        CONF_IMAGE_SCAN_INTERVAL, DEFAULT_IMAGE_SCAN_INTERVAL
    )
    video_format = user_input.get(CONF_VIDEO_FORMAT, DEFAULT_VIDEO_FORMAT)

    host = host.strip("/")

    return {
        CONF_HOST: host,
        CONF_DATA_SCAN_INTERVAL: data_scan_interval,
        CONF_IMAGE_SCAN_INTERVAL: image_scan_interval,
        CONF_VIDEO_FORMAT: video_format,
    }


class NOAASolarConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for NOAA Solar integration."""

    VERSION = 3

    def __init__(self) -> None:
        """Initialize a NOAA Solar config flow."""
        self.flow_host: str | None = None

    def is_matching(self, other_flow: Self) -> bool:
        """Return True if another in-progress flow targets the same host."""
        return self.flow_host is not None and self.flow_host == getattr(
            other_flow, "flow_host", None
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Show config Form step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            data = user_input_to_data(user_input)
            self.flow_host = data[CONF_HOST].casefold()
            await self.async_set_unique_id(self.flow_host)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                data=data,
            )

        user_input = default_user_input()
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema(user_input),
            errors=errors,
        )
