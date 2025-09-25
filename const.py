"""Constants."""

DOMAIN = "ups_hat_e"
DEFAULT_ADDR = "0x2d"
DEFAULT_UNIQUE_ID = "ha_pi_ups"
DEFAULT_NAME = "HA Pi UPS"

CONF_ADDR = "addr"
CONF_SCAN_INTERVAL = "scan_interval"

SAMPLES = 3

# Registers
# https://www.waveshare.com/wiki/UPS_HAT_(E)_Register

# Automatically Rebooting Register
REG_REBOOT = 0x01

# Charging Register
# BIT7
# 1: charging
# 0: non-charging

# BIT6
# 1: fast charging
# 0: no fast charging

# BIT5
# 1: VBUS is powered
# 0: VBUS is not powered

# BIT4 BIT3
# Fixed: 00

# BIT2 BIT1 BIT0
# 000: standby, 001: trickle charge,
# 010: constant current charge; 011: constant voltage charge;
# 100: Charging pending, 101: Full state, 110: Charge timeout

REG_CHARGING = 0x02

# BUS VOLTAGE REGISTER (R)
REG_BUSVOLTAGE = 0x10

# POWER REGISTER (R)
REG_POWER = 0x14

# BAT VOLTAGE REGISTER (R)
REG_BATVOLTAGE = 0x20

# CURRENT REGISTER (R)
REG_CURRENT = 0x22

# BATTERY PERCENT REGISTER (R)
REG_BATSOC = 0x24

# Battery Remaining Capacity Register
REG_REM_BAT_CAP = 0x26

# Battery Remaining Discharge Time Register
REG_REM_BAT_TIME = 0x28

# Cell 1 Voltage Register
REG_CELL_1_VOLTAGE = 0x30

# Value to write when triger shutdown
CONST_SHUTDOWN_CMD = 0x55

ATTR_CAPACITY = "capacity"
ATTR_SOC = "soc"
ATTR_PSU_VOLTAGE = "psu_voltage"
ATTR_CHARGER_VOLTAGE = "charger_voltage"
ATTR_BATTERY_VOLTAGE = "battery_voltage"
ATTR_BATTERY_CURRENT = "battery_current"
ATTR_CHARGER_CURRENT = "charger_current"
ATTR_POWER = "power"
ATTR_CHARGING = "charging"
ATTR_FAST_CHARGING = "fast_charging"
ATTR_ONLINE = "online"
ATTR_BATTERY_CONNECTED = "battery_connected"
ATTR_LOW_BATTERY = "low_battery"
ATTR_POWER_CALCULATED = "power_calculated"
ATTR_REMAINING_BATTERY_CAPACITY = "remaining_battery_capacity"
ATTR_REMAINING_TIME = "remaining_time_min"
