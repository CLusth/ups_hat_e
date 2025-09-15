"""UPS Hat E button."""

from __future__ import annotations

from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .coordinator import UpsHatECoordinator
from .entity import UpsHatEEntity

from homeassistant.const import (
    EntityCategory,
    EVENT_HOMEASSISTANT_CLOSE,
)

import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up button platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return

    coordinator = discovery_info.get("coordinator")

    async_add_entities([ShutdownButton(hass, coordinator)])

class UpsHatEButton(UpsHatEEntity, ButtonEntity):
    """Base button."""

    def __init__(self, coordinator: UpsHatECoordinator) -> None:
        super().__init__(coordinator)

class ShutdownButton(UpsHatEButton):
    """Defines a reboot button."""

    def __init__(self, hass: HomeAssistant, coordinator: UpsHatECoordinator) -> None:
        super().__init__(coordinator)
        self._name = "Shutdown"
        self._attr_device_class = ButtonDeviceClass.RESTART
        self._attr_entity_category = EntityCategory.CONFIG

        # Add a listener to detect when Home Assisnt is shutting down
        hass.bus.async_listen(EVENT_HOMEASSISTANT_CLOSE, self._async_shutdown_event_handler)

        _LOGGER.debug("ShutdownButton initialized")

    async def _async_shutdown_event_handler(self, call) -> None:
        _LOGGER.debug("Shutdown event handled: %s (async)", call.data)
        await asyncio.sleep(15)
        await self.async_press()

    async def async_press(self) -> None:
        _LOGGER.debug("ShutdownButton pressed (async)")
        await self._coordinator.shutdown()
