"""Config flow for the Waveshare Pi UPS Hat (E)."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID
from homeassistant.core import callback

from .const import (
    CONF_ADDR,
    CONF_SCAN_INTERVAL,
    CONF_SHUTDOWN_DELAY,
    DEFAULT_ADDR,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SHUTDOWN_DELAY,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

class WaveshareUpsHatConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Waveshare Pi UPS Hat (E)."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow for this integration."""
        return WaveshareUpsHatOptionsFlow()

    async def async_step_user(self, user_input=None):
        """Handle the user step."""
        if user_input is not None:
            unique_id = "UPS_HAT_E_" + str(user_input[CONF_ADDR]).strip().lower()
            _LOGGER.debug(f"Set unique_id: {unique_id}")
            await self.async_set_unique_id(unique_id)

            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_ADDR, default=DEFAULT_ADDR): str,
                vol.Required(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=3600)
                ),
                vol.Required(
                    CONF_SHUTDOWN_DELAY, default=DEFAULT_SHUTDOWN_DELAY
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=3600)),
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors={},
        )


class WaveshareUpsHatOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Waveshare Pi UPS Hat (E)."""

    async def async_step_init(self, user_input=None):
        """Manage the scan interval."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        scan_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        shutdown_delay = self.config_entry.options.get(
            CONF_SHUTDOWN_DELAY,
            self.config_entry.data.get(CONF_SHUTDOWN_DELAY, DEFAULT_SHUTDOWN_DELAY),
        )
        schema = vol.Schema(
            {
                vol.Required(CONF_SCAN_INTERVAL, default=scan_interval): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=3600)
                ),
                vol.Required(CONF_SHUTDOWN_DELAY, default=shutdown_delay): vol.All(
                    vol.Coerce(int), vol.Range(min=1, max=3600)
                ),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)