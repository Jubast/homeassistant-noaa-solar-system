"""Config flow for Solar System Scraper integration."""
from __future__ import annotations
from urllib.parse import ParseResult, urlparse

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_SCAN_INTERVAL
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_SCAN_INTERVAL, DEFAULT_NAME, DEFAULT_HOST, DOMAIN


class SolarSystemScraperHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Solar system scraper."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._errors: dict = {}

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Show config Form step."""
        if user_input is not None:
            # set some defaults in case we need to return to the form
            host = user_input.get(CONF_HOST, DEFAULT_HOST)
            scan_interval = user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

            host = host.strip("/")

            return self.async_create_entry(
                title=DEFAULT_NAME,
                data={CONF_HOST: host, CONF_SCAN_INTERVAL: scan_interval},
            )
        else:
            user_input = {}
            user_input[CONF_HOST] = DEFAULT_HOST
            user_input[CONF_SCAN_INTERVAL] = DEFAULT_SCAN_INTERVAL

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST, default=user_input.get(CONF_HOST, DEFAULT_HOST)
                    ): str,
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=user_input.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): int,
                }
            ),
            errors=self._errors,
        )
