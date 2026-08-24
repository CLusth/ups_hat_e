"""Waveshare Pi UPS Hat (E)."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)
from .coordinator import UpsHatECoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.BUTTON]

async def _async_setup_coordinator(
    hass: HomeAssistant,
    config: ConfigType,
    *,
    config_entry: ConfigEntry,
) -> UpsHatECoordinator:
    """Set up and refresh the UPS Hat E coordinator."""
    config = dict(config)
    config[CONF_SCAN_INTERVAL] = timedelta(
        seconds=config.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    )

    coordinator = UpsHatECoordinator(hass, config, config_entry=config_entry)
    await coordinator.async_config_entry_first_refresh()
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
