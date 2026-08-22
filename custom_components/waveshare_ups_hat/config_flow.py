"""Config flow for the Waveshare Pi UPS Hat (E)."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID

from .const import (
    CONF_ADDR,
    CONF_SCAN_INTERVAL,
    DEFAULT_ADDR,
    DEFAULT_NAME,
    DEFAULT_UNIQUE_ID,
    DOMAIN,
)


class WaveshareUpsHatConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Waveshare Pi UPS Hat (E)."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the user step."""
        if user_input is not None:
            address = str(user_input[CONF_ADDR]).strip().lower()
            await self.async_set_unique_id(address)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input[CONF_NAME], data=user_input
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_UNIQUE_ID, default=DEFAULT_UNIQUE_ID): str,
                vol.Required(CONF_ADDR, default=DEFAULT_ADDR): str,
                vol.Required(CONF_SCAN_INTERVAL, default=30): vol.All(
                    vol.Coerce(int), vol.Range(min=1)
                ),
            }
        )
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors={},
        )