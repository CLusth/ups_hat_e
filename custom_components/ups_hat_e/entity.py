"""UPS Hat E entity."""

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import UpsHatECoordinator


class UpsHatEEntity(CoordinatorEntity):
    """UPS Hat E entity."""

    def __init__(self, coordinator: UpsHatECoordinator) -> None:
        """Initialize a UPS Hat E entity."""
        self._coordinator = coordinator
        self._device_id = self._coordinator.id_prefix
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.id_prefix)},
            name=coordinator.name_prefix,
            manufacturer="Waveshare Pi UPS Hat E",
        )

        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)

    @property
    def name(self):
        """Return the name of the UPS Hat E entity."""
        return self._coordinator.name_prefix + " " + self._name

    @property
    def unique_id(self):
        """Return the unique ID for the UPS Hat E entity."""
        return self._coordinator.id_prefix + "_" + self._name

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
