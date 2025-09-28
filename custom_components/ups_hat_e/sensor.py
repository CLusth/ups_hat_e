"""UPS Hat E sensors."""

import logging

from homeassistant import core
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .entity import UpsHatEEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: core.HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up UPS Hat E sensors via platform discovery."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return

    coordinator = discovery_info.get("coordinator")

    sensors = [
        ChargerVoltageSensor(coordinator),
        ChargerCurrentSensor(coordinator),
        ChargerPowerSensor(coordinator),
        BatteryVoltageSensor(coordinator),
        BatteryCurrentSensor(coordinator),
        SocSensor(coordinator),
        RemainingCapacitySensor(coordinator),
        RemainingTimeSensor(coordinator),
        Cell1VoltageSensor(coordinator),
        Cell2VoltageSensor(coordinator),
        Cell3VoltageSensor(coordinator),
        Cell4VoltageSensor(coordinator),
    ]
    async_add_entities(sensors)


class ChargerVoltageSensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the charger voltage of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the charger voltage sensor."""
        super().__init__(coordinator)
        self._name = "Charger Voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_device_class = SensorDeviceClass.VOLTAGE
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        """Return the voltage value reported by the UPS."""
        return self._coordinator.data["charger_voltage"]


class ChargerCurrentSensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the charger current of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the charger current sensor."""
        super().__init__(coordinator)
        self._name = "Charger Current"
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.MILLIAMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT
        self._attr_suggested_display_precision = 0

    @property
    def native_value(self):
        """Return the current value reported by the UPS."""
        return self._coordinator.data["charger_current"]


class ChargerPowerSensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the power of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the charger power sensor."""
        super().__init__(coordinator)
        self._name = "Charger Power"
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        """Return the power value reported by the UPS."""
        return self._coordinator.data["charger_power"]


class BatteryVoltageSensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the voltage of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the battery voltage sensor."""
        super().__init__(coordinator)
        self._name = "Battery Voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_device_class = SensorDeviceClass.VOLTAGE
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        """Return the voltage value reported by the UPS."""
        return self._coordinator.data["battery_voltage"]


class BatteryCurrentSensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the current of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the battery current sensor."""
        super().__init__(coordinator)
        self._name = "Battery Current"
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.MILLIAMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT
        self._attr_suggested_display_precision = 0

    @property
    def native_value(self):
        """Return the current value reported by the UPS."""
        return self._coordinator.data["battery_current"]


class SocSensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the SoC of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the SoC sensor."""
        super().__init__(coordinator)
        self._name = "SoC"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        """Return the SoC value reported by the UPS."""
        return self._coordinator.data["soc"]


class RemainingCapacitySensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the remaining capacity of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the capacity sensor."""
        super().__init__(coordinator)
        self._name = "Remaining Capacity"
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY_STORAGE
        self._attr_suggested_display_precision = 0

    @property
    def native_value(self):
        """Return the capacity value reported by the UPS."""
        return self._coordinator.data["remaining_battery_capacity"]


class RemainingTimeSensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the remianing time of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the remaining time sensor."""
        super().__init__(coordinator)
        self._name = "Remaining Time"
        self._attr_native_unit_of_measurement = UnitOfTime.MINUTES
        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_suggested_display_precision = 0

    @property
    def native_value(self):
        """Return the remaining reported by the UPS."""
        return self._coordinator.data["remaining_time"]


class Cell1VoltageSensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the charger voltage of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the cell 1 voltage sensor."""
        super().__init__(coordinator)
        self._name = "Cell1 Voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_device_class = SensorDeviceClass.VOLTAGE
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        """Return the voltage value reported by the UPS."""
        return self._coordinator.data["cell1_voltage"]


class Cell2VoltageSensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the charger voltage of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the cell 2 voltage sensor."""
        super().__init__(coordinator)
        self._name = "Cell2 Voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_device_class = SensorDeviceClass.VOLTAGE
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        """Return the voltage value reported by the UPS."""
        return self._coordinator.data["cell2_voltage"]


class Cell3VoltageSensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the charger voltage of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the cell 3 voltage sensor."""
        super().__init__(coordinator)
        self._name = "Cell3 Voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_device_class = SensorDeviceClass.VOLTAGE
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        """Return the voltage value reported by the UPS."""
        return self._coordinator.data["cell3_voltage"]


class Cell4VoltageSensor(UpsHatEEntity, SensorEntity):
    """Sensor for reporting the charger voltage of the UPS Hat E."""

    def __init__(self, coordinator) -> None:
        """Initialize the cell 4 voltage sensor."""
        super().__init__(coordinator)
        self._name = "Cell4 Voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_device_class = SensorDeviceClass.VOLTAGE
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        """Return the voltage value reported by the UPS."""
        return self._coordinator.data["cell4_voltage"]
