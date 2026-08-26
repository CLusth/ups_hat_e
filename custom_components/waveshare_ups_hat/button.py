"""UPS Hat E buttons."""

from __future__ import annotations

import asyncio
import logging

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, EVENT_HOMEASSISTANT_CLOSE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import UpsHatECoordinator
from .entity import UpsHatEEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the shutdown button."""
    coordinator = entry.runtime_data

    async_add_entities([ShutdownButton(hass, coordinator)])


class ShutdownButton(UpsHatEEntity, ButtonEntity):
    """Defines a reboot button."""

    def __init__(self, hass: HomeAssistant, coordinator: UpsHatECoordinator) -> None:
        """Initialize the ShutdownButton entity."""
        super().__init__(coordinator)
        self._name = "Shutdown"
        self._attr_device_class = ButtonDeviceClass.RESTART
        self._attr_entity_category = EntityCategory.CONFIG

        # Add a listener to detect when Home Assistant is shutting down
        hass.bus.async_listen(
            EVENT_HOMEASSISTANT_CLOSE, self._async_shutdown_event_handler
        )

        _LOGGER.debug("ShutdownButton initialized")

    async def _async_shutdown_event_handler(self, call) -> None:
        _LOGGER.debug("Shutdown event handled: %s (async)", call.data)
        _LOGGER.debug("Wait for shutdown: %d (seconds)", self._coordinator.shutdown_delay)
        await asyncio.sleep(self._coordinator.shutdown_delay)
        await self.async_press()

    async def async_press(self) -> None:
        """Handle button press to initiate UPS shutdown."""
        _LOGGER.debug("ShutdownButton pressed (async)")
        await self._coordinator.shutdown()
