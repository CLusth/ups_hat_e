"""UPS Hat E binary_sensors."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .coordinator import UpsHatECoordinator
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


class UpsHatEBinarySensor(UpsHatEEntity, BinarySensorEntity):
    """Base binary sensor."""

    def __init__(self, coordinator: UpsHatECoordinator) -> None:
        super().__init__(coordinator)


class OnlineBinarySensor(UpsHatEBinarySensor):
    """Online binary sensor."""

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Online"
        self._attr_device_class = BinarySensorDeviceClass.PLUG

    @property
    def is_on(self):
        return self._coordinator.data["online"]


class ChargingBinarySensor(UpsHatEBinarySensor):
    """Charging binary sensor."""

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Charging"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        return self._coordinator.data["charging"]


class FastChargingBinarySensor(UpsHatEBinarySensor):
    """Fast charging binary sensor."""

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Fast Charging"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        return self._coordinator.data["fast_charging"]
