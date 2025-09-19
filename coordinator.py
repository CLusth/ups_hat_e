"""UPS Hat E coordinator."""

import logging

import smbus2 as smbus
from collections import deque
from statistics import mean

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
            "state": "Unknown",
            "online": False,
            "charging": False,
        }
        _LOGGER.debug("Assign SMBUS")
        self._bus = smbus.SMBus(1)

        self._is_online = False
        self._charger_current_buf = deque(maxlen=SAMPLES)
        self._charger_voltage_buf = deque(maxlen=SAMPLES)
        self._charger_power_buf = deque(maxlen=SAMPLES)
        self._battery_current_buf = deque(maxlen=SAMPLES)
        self._battery_voltage_buf = deque(maxlen=SAMPLES)

        _LOGGER.debug("Call super")
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=config.get(CONF_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        try:
            try:
                data = self._bus.read_i2c_block_data(self._addr, REG_CHARGING, 0x01)
            except Exception as e:
                _LOGGER.warning(f"PIHAT Exception: {str(e)}")

            if(data[0] & 0x40):
                state = "Fast Charging"
                _LOGGER.debug("Fast Charging state")
            elif(data[0] & 0x80):
                state = "Charging"
                _LOGGER.debug("Charging state")
            elif(data[0] & 0x20):
                state = "Discharging"
                _LOGGER.debug("Discharge state")
            else:
                state = "Idle"
                _LOGGER.debug("Idle state")

            self._is_online = bool(data[0] & 0x20)

            data = self._bus.read_i2c_block_data(self._addr, REG_BUSVOLTAGE, 0x06)
            charger_voltage = int(data[0] | data[1] << 8)
            self._charger_voltage_buf.append(charger_voltage)

            charger_current = int(data[2] | data[3] << 8)
            self._charger_current_buf.append(charger_current)

            charger_power = int(data[4] | data[5] << 8)
            self._charger_power_buf.append(charger_power)

            _LOGGER.debug("VBUS Voltage %5dmV"%charger_voltage)
            _LOGGER.debug("VBUS Current %5dmA"%charger_current)
            _LOGGER.debug("VBUS Power   %5dmW"%charger_power)

            data = self._bus.read_i2c_block_data(self._addr, REG_BATVOLTAGE, 0x0C)
            battery_voltage = int(data[0] | data[1] << 8)
            self._battery_voltage_buf.append(int(battery_voltage))

            _LOGGER.debug("Battery Voltage %d mV"%battery_voltage)
            battery_current = (data[2] | data[3] << 8)
            if(battery_current > 0x7FFF):
                battery_current -= 0xFFFF
            self._battery_current_buf.append(int(battery_current))
            _LOGGER.debug("Battery Current %d mA"%battery_current)

            soc = (int(data[4] | data[5] << 8))
            _LOGGER.debug("Battery Percent %d%%"%soc)

            remaining_battery_capacity = (data[6] | data[7] << 8)
            _LOGGER.debug("Remaining Capacity %d mAh"%remaining_battery_capacity)

            if not self._is_online:
                remaining_time = (data[8] | data[9] << 8)
                _LOGGER.debug("Run Time To Empty %d min"%remaining_time)
            else:
                remaining_time = (data[10] | data[11] << 8)
                _LOGGER.debug("Average Time To Full %d min"%remaining_time)

            data = self._bus.read_i2c_block_data(self._addr, REG_CELL_1_VOLTAGE, 0x08)
            cell1_voltage = (data[0] | data[1] << 8)
            cell2_voltage = (data[2] | data[3] << 8)
            cell3_voltage = (data[4] | data[5] << 8)
            cell4_voltage = (data[6] | data[7] << 8)
            _LOGGER.debug("Cell Voltage1 %d mV"%cell1_voltage)
            _LOGGER.debug("Cell Voltage2 %d mV"%cell2_voltage)
            _LOGGER.debug("Cell Voltage3 %d mV"%cell3_voltage)
            _LOGGER.debug("Cell Voltage4 %d mV"%cell4_voltage)

            charging = bool(state in ["Fast Charging","Charging"])

            self.data = {
                "charger_voltage": round(mean(self._charger_voltage_buf) / 1000, 2),
                "charger_current": round(mean(self._charger_current_buf), 2),
                "charger_power": round(mean(self._charger_power_buf) / 1000, 2),
                "battery_voltage": round(mean(self._battery_voltage_buf) / 1000, 2),
                "battery_current": round(mean(self._battery_current_buf), 2),
                "soc": round(soc, 1),
                "remaining_battery_capacity": round(
                    (remaining_battery_capacity * battery_voltage / 1000) / 1000, 2
                ),  # in Wh
                "remaining_time": remaining_time,
                "cell1_voltage": cell1_voltage / 1000,
                "cell2_voltage": cell2_voltage / 1000,
                "cell3_voltage": cell3_voltage / 1000,
                "cell4_voltage": cell4_voltage / 1000,
                "state": state,
                "online": self._is_online,
                "charging": charging,
            }
            #_LOGGER.warning("UPS_HAT_E DATA 1")
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
            self._writeByte(REG_REBOOT, 0x55)
