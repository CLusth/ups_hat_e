"""Waveshare Pi UPS Hat (E)"""

from __future__ import annotations

from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID, Platform
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_ADDR,
    CONF_BATTERY_CAPACITY,
    CONF_SCAN_INTERVAL,
    DEFAULT_ADDR,
    DEFAULT_NAME,
    DEFAULT_UNIQUE_ID,
    DOMAIN,
)
from .coordinator import UpsHatECoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_ADDR, default=DEFAULT_ADDR): cv.string,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Optional(CONF_UNIQUE_ID, default=DEFAULT_UNIQUE_ID): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=20): int,
                vol.Optional(CONF_BATTERY_CAPACITY, default=4800): cv.positive_int,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, global_config: ConfigType) -> bool:
    """Your controller/hub specific code."""

    if DOMAIN not in global_config:
        return False

    config: ConfigType = global_config[DOMAIN]

    if CONF_SCAN_INTERVAL not in config:
        return False
    config[CONF_SCAN_INTERVAL] = timedelta(seconds=config[CONF_SCAN_INTERVAL])

    coordinator = UpsHatECoordinator(hass, config)
    await coordinator.async_refresh()

    await async_load_platform(
        hass, "sensor", DOMAIN, {"coordinator": coordinator}, config
    )

    await async_load_platform(
        hass, "binary_sensor", DOMAIN, {"coordinator": coordinator}, config
    )

    await async_load_platform(
        hass, "button", DOMAIN, {"coordinator": coordinator}, config
    )

    async def async_update_data(now):
        await coordinator.async_request_refresh()

    async_track_time_interval(hass, async_update_data, config.get(CONF_SCAN_INTERVAL))

    return True
