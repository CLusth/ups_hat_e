"""Waveshare Pi UPS Hat (E)."""

from __future__ import annotations

from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID, Platform
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_ADDR,
    CONF_SCAN_INTERVAL,
    CONF_USE_MOCK,
    DEFAULT_ADDR,
    DEFAULT_NAME,
    DEFAULT_UNIQUE_ID,
    DOMAIN,
)
from .coordinator import UpsHatECoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.BUTTON]

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_ADDR, default=DEFAULT_ADDR): cv.string,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Optional(CONF_UNIQUE_ID, default=DEFAULT_UNIQUE_ID): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=30): int,
                vol.Optional(CONF_USE_MOCK, default=False): bool,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def _async_setup_coordinator(
    hass: HomeAssistant,
    config: ConfigType,
    *,
    config_entry: ConfigEntry | None = None,
) -> UpsHatECoordinator:
    """Set up and refresh the UPS Hat E coordinator."""
    config = dict(config)
    config[CONF_SCAN_INTERVAL] = timedelta(
        seconds=config.get(CONF_SCAN_INTERVAL, 30)
    )
    config[CONF_USE_MOCK] = bool(config.get(CONF_USE_MOCK, False))

    coordinator = UpsHatECoordinator(hass, config, config_entry=config_entry)
    if config_entry is not None:
        await coordinator.async_config_entry_first_refresh()
    else:
        await coordinator.async_request_refresh()
    return coordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Waveshare UPS Hat E from a config entry."""
    coordinator = await _async_setup_coordinator(
        hass, entry.data, config_entry=entry
    )
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Waveshare UPS Hat E config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_setup(hass: HomeAssistant, global_config: ConfigType) -> bool:
    """Set up Waveshare UPS Hat E from YAML."""

    if DOMAIN not in global_config:
        return False

    config: ConfigType = global_config[DOMAIN]

    if CONF_SCAN_INTERVAL not in config:
        return False
    coordinator = await _async_setup_coordinator(
        hass, config
    )

    await async_load_platform(
        hass, "sensor", DOMAIN, {"coordinator": coordinator}, config
    )

    await async_load_platform(
        hass, "binary_sensor", DOMAIN, {"coordinator": coordinator}, config
    )

    await async_load_platform(
        hass, "button", DOMAIN, {"coordinator": coordinator}, config
    )

    return True
