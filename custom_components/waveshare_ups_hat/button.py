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
        self._hass = hass
        self._name = "Shutdown"
        self._attr_device_class = ButtonDeviceClass.RESTART
        self._attr_entity_category = EntityCategory.CONFIG

        _LOGGER.debug("ShutdownButton initialized")

    async def async_added_to_hass(self) -> None:
        """Register the shutdown listener for this entity's lifetime."""
        await super().async_added_to_hass()
        remove_listener = self._hass.bus.async_listen(
            EVENT_HOMEASSISTANT_CLOSE, self._async_shutdown_event_handler
        )
        self.async_on_remove(remove_listener)

    async def _async_shutdown_event_handler(self, call) -> None:
        _LOGGER.debug("Shutdown event handled. Wait for shutdown: %d (seconds)", self.coordinator.shutdown_delay)
        await asyncio.sleep(self.coordinator.shutdown_delay)
        await self.async_press()

    async def async_press(self) -> None:
        """Handle button press to initiate UPS shutdown."""
        _LOGGER.debug("ShutdownButton pressed (async)")
        await self.coordinator.shutdown()
