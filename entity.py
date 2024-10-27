"""UPS Hat E entity."""

from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN
from .coordinator import UpsHatECoordinator


class UpsHatEEntity:
    """UPS Hat E entity."""

    def __init__(self, coordinator: UpsHatECoordinator) -> None:
        self._coordinator = coordinator
        self._device_id = self._coordinator.id_prefix
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.id_prefix)},
            name=coordinator.name_prefix,
            manufacturer="Waveshare Pi UPS Hat E",
        )

    @property
    def name(self):
        return self._coordinator.name_prefix + " " + self._name

    @property
    def unique_id(self):
        return self._coordinator.id_prefix + "_" + self._name

    async def async_update(self):
        await self._coordinator.async_request_refresh()
