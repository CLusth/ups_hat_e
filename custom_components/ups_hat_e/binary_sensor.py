"""UPS Hat E binary_sensors."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .entity import UpsHatEEntity


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up binary sensor platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return

    coordinator = discovery_info.get("coordinator")

    sensors = [
        OnlineBinarySensor(coordinator),
        ChargingBinarySensor(coordinator),
        FastChargingBinarySensor(coordinator),
    ]

    async_add_entities(sensors)


class OnlineBinarySensor(UpsHatEEntity, BinarySensorEntity):
    """Online binary sensor."""

    def __init__(self, coordinator) -> None:
        """Initialize the online binary sensor."""
        super().__init__(coordinator)
        self._name = "Online"
        self._attr_device_class = BinarySensorDeviceClass.PLUG

    @property
    def is_on(self):
        """Return True if the UPS Hat E is connected to power."""
        return self._coordinator.data["online"]


class ChargingBinarySensor(UpsHatEEntity, BinarySensorEntity):
    """Charging binary sensor."""

    def __init__(self, coordinator) -> None:
        """Initialize the charging binary sensor."""
        super().__init__(coordinator)
        self._name = "Charging"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        """Return True if the UPS Hat E is charging."""
        return self._coordinator.data["charging"]


class FastChargingBinarySensor(UpsHatEEntity, BinarySensorEntity):
    """Fast charging binary sensor."""

    def __init__(self, coordinator) -> None:
        """Initialize the fast charging binary sensor."""
        super().__init__(coordinator)
        self._name = "Fast Charging"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        """Return True if the UPS Hat E is fast charging."""
        return self._coordinator.data["fast_charging"]
