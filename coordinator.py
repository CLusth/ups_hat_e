"""UPS Hat E coordinator."""

import logging

import smbus2 as smbus
from collections import deque
from statistics import median

from homeassistant import core
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_ADDR,
    CONF_SCAN_INTERVAL,
    DOMAIN,
    REG_BATVOLTAGE,
    REG_BUSVOLTAGE,
    REG_CELL_1_VOLTAGE,
    REG_CHARGING,
    REG_REBOOT,
    CONST_SHUTDOWN_CMD,
    SAMPLES,
)

_LOGGER = logging.getLogger(__name__)


class UpsHatECoordinator(DataUpdateCoordinator):
    def __init__(self, hass: core.HomeAssistant, config: ConfigType) -> None:
        """Initialize coordinator."""
        _LOGGER.debug("Initialize coordinator.")
        self.name_prefix = config.get(CONF_NAME)
        self.id_prefix = config.get(CONF_UNIQUE_ID)
        try:
            self._addr = int(config.get(CONF_ADDR))
        except:
            _LOGGER.error(f"ADDR {config.get(CONF_ADDR)} for UPS Hat E is invalid.")
            raise

        self.data = {
            "charger_voltage": 0,
            "charger_current": 0,
            "charger_power": 0,
            "battery_voltage": 0,
            "battery_current": 0,
            "soc": 0,
            "remaining_battery_capacity": 0,  # in Wh
            "remaining_time": 0,
            "cell1_voltage": 0,
            "cell2_voltage": 0,
            "cell3_voltage": 0,
            "cell4_voltage": 0,
            "online": False,
            "charging": False,
            "fast_charging": False,
        }

        self._is_online = False
        self._is_charging = False
        self._is_fast_charging = False
        self._charger_current_buf = deque(maxlen=SAMPLES)
        self._charger_voltage_buf = deque(maxlen=SAMPLES)
        self._charger_power_buf = deque(maxlen=SAMPLES)
        self._battery_current_buf = deque(maxlen=SAMPLES)
        self._battery_voltage_buf = deque(maxlen=SAMPLES)
        self._remaining_time_buf = deque(maxlen=SAMPLES)

        _LOGGER.debug("Call super")
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=config.get(CONF_SCAN_INTERVAL),
            always_update=True
        )

    async def _async_setup(self):
        """Set up the coordinator
        
        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        _LOGGER.debug("Assign SMBUS")
        self._bus = smbus.SMBus(1)

    async def _async_update_data(self):
        try:
            try:
                data = self._bus.read_i2c_block_data(self._addr, REG_CHARGING, 0x01)
            except Exception as e:
                _LOGGER.warning(f"PIHAT Exception: {str(e)}")

            self._is_online = bool(data[0] & 0x20)
            self._is_fast_charging = bool(data[0] & 0x40)
            self._is_charging = bool(data[0] & 0x80)

            data = self._bus.read_i2c_block_data(self._addr, REG_BUSVOLTAGE, 0x06)
            charger_voltage = int.from_bytes(data[0:2], "little", signed=True)

            self._charger_voltage_buf.append(charger_voltage)

            charger_current = int.from_bytes(data[2:4], "little", signed=True)
            self._charger_current_buf.append(charger_current)

            charger_power = int.from_bytes(data[4:6], "little", signed=True)
            self._charger_power_buf.append(charger_power)

            _LOGGER.debug("VBUS Voltage %5dmV"%charger_voltage)
            _LOGGER.debug("VBUS Current %5dmA"%charger_current)
            _LOGGER.debug("VBUS Power   %5dmW"%charger_power)

            data = self._bus.read_i2c_block_data(self._addr, REG_BATVOLTAGE, 0x0C)
            battery_voltage = int.from_bytes(data[0:2], "little", signed=True)
            self._battery_voltage_buf.append(int(battery_voltage))
            _LOGGER.debug("Battery Voltage %d mV"%battery_voltage)

            battery_current = int.from_bytes(data[2:4], "little", signed=True)
            self._battery_current_buf.append(int(battery_current))
            _LOGGER.debug("Battery Current1 %d mA"%battery_current)

            soc = int.from_bytes(data[4:6], "little", signed=True)
            _LOGGER.debug("Battery Percent %d%%"%soc)

            remaining_battery_capacity = int.from_bytes(data[6:8], "little", signed=True)
            _LOGGER.debug("Remaining Capacity %d mAh"%remaining_battery_capacity)

            if not self._is_online:
                # If there is no power read these registers
                remaining_time = int.from_bytes(data[8:10], "little", signed=True)
                _LOGGER.debug("Time To Empty %d min"%remaining_time)
            else:
                # ... when charging read other registers
                if (battery_current > 0):
                    remaining_time = int.from_bytes(data[10:12], "little", signed=True)
                else:
                    # Avoid intrepeting 0xFFFF as a number
                    remaining_time = 0
                _LOGGER.debug("Time To Full %d min"%remaining_time)
            
            # Simplistic solution where both types of values go to the same buffer
            self._remaining_time_buf.append(remaining_time)

            data = self._bus.read_i2c_block_data(self._addr, REG_CELL_1_VOLTAGE, 0x08)
            cell1_voltage = int.from_bytes(data[0:2], "little", signed=True)
            cell2_voltage = int.from_bytes(data[2:4], "little", signed=True)
            cell3_voltage = int.from_bytes(data[4:6], "little", signed=True)
            cell4_voltage = int.from_bytes(data[6:8], "little", signed=True)
            _LOGGER.debug("Cell Voltage1 %d mV"%cell1_voltage)
            _LOGGER.debug("Cell Voltage2 %d mV"%cell2_voltage)
            _LOGGER.debug("Cell Voltage3 %d mV"%cell3_voltage)
            _LOGGER.debug("Cell Voltage4 %d mV"%cell4_voltage)

            self.data = {
                "charger_voltage": round(median(self._charger_voltage_buf) / 1000, 2),
                "charger_current": round(median(self._charger_current_buf), 2),
                "charger_power": round(median(self._charger_power_buf) / 1000, 2),
                "battery_voltage": round(median(self._battery_voltage_buf) / 1000, 2),
                "battery_current": round(median(self._battery_current_buf), 2),
                "soc": round(soc, 1),
                "remaining_battery_capacity": round(
                    (remaining_battery_capacity * battery_voltage / 1000) / 1000, 2
                ),  # in Wh
                "remaining_time": round(median(self._remaining_time_buf)),
                "cell1_voltage": cell1_voltage / 1000,
                "cell2_voltage": cell2_voltage / 1000,
                "cell3_voltage": cell3_voltage / 1000,
                "cell4_voltage": cell4_voltage / 1000,
                "online": self._is_online,
                "charging": self._is_charging,
                "fast_charging": self._is_fast_charging,
            }

            _LOGGER.debug(f"UPS_HAT_E DATA 2: {self.data}")
            return self.data
        except Exception as e:
            raise UpdateFailed(f"Error updating data: {e}")

    def _writeByte(self, register, data):
        temp = [0]
        temp[0] = data & 0xFF
        self._bus.write_i2c_block_data(self._addr, register, temp)

    async def shutdown(self):
        # Only allow shutdown if not plugged id
        if not self._is_online:
            self._writeByte(REG_REBOOT, CONST_SHUTDOWN_CMD)
