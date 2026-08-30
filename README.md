# Home Assistant integration for the UPS Hat (E) from Waveshare

Functionality is based on the [Waveshare wiki](https://www.waveshare.com/wiki/UPS_HAT_(E))
for this device.

_Note: This is for the (E) version only._

![UPS HAT (E) for Raspberry](https://github.com/CLusth/ups_hat_e/blob/master/images/UPS-HAT-E-details-1.jpg?raw=true)

## Prerequisites

Enable I2C on your RaspberryPi board. (See trouble shooting below)

## Installation

The integration can be installed using [HACS](https://hacs.xyz/). The integrations is not
available in the default repositories, so you will need to add the URL of this repository
as a custom repository to HACS (see [here](https://hacs.xyz/docs/faq/custom_repositories)).

Alternatively you can use the button below:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=CLusth&repository=ups_hat_e&category=Integration)

## Instructions

Add the integration through **Settings -> Devices & services -> Add integration**
and search for **Waveshare Pi UPS Hat (E)**. Enter the I2C address, device name,
unique ID, scan interval and shutdown delay in the setup form. They all have default values that should work.

The scan interval and shutdown delay can be changed later from the integration's **Configure** menu.

_Note: If you previosly have installed (v1.0.3 or earlier) you need to remove the old configuration from the configuran.yaml file_

### Example automation

Simple automation that trigger shutdown before the batttery is running out.

```yaml
alias: Low battery shutdown
description: "Shutdown HA when SoC is belew the threshold."
triggers:
  - trigger: numeric_state
    entity_id:
      - sensor.ups_hat_e_soc
    below: 10
conditions: []
actions:
  - action: hassio.host_shutdown
    metadata: {}
    data: {}
mode: single
```

## Trouble shooting

### Problem with I2C

```text
Error during setup of component waveshare_ups_hat: [Errno 2] No such file or directory: '/dev/i2c-1'
```

The I2C bus is not enabled on you RaspberryPi board.

#### Solution

* Use [HassOSConfigurator](https://github.com/adamoutler/HassOSConfigurator) to enable I2C from Home Assitant. (Don't forget to reboot twice)

or

* Use raspi-config CLI application, see [Waveshare wiki](https://www.waveshare.com/wiki/UPS_HAT_(E)) for details.

### Problem with old config

```text
The 'waveshare_ups_hat' integration does not support YAML setup, please remove it from your configuration
```

#### Solution

 1. Remove all old configuration for Waveshare_ups_hat_e in your configuration.yaml.
 2. Restart Home Assistant

### Problem with Old entities becomes "Unavaialbe" after update.

Newer versions of this integration uses UI configuration instead of YAML, that will create duplicates of all entities.

#### Solution

 1. Remove all the old entilies beloning to the device. They are easy to filter out in the **Settings -> Devices & services -> Entities** page.
 2. Open each (avalable) entity belonging to the device and change the Entity ID, iether manually or just click the "Restore Entitiy ID". Most likely the only thing that differs is that they have an extra "_2" postfix.

## Known issues

* The built in timer between triggering shutdown and when the power is cut is very short (~30s).
  There is a risk HA is not gracefully shutdown. To mitigate this I have added a configurable delay but it might not be enough.
  Its very hard to get a graceful shutdown.
* A reset of the HA will also trigger the UPS shutdown, i.e. there is currently nothing
  diffentiating between reset and shutdown. To mitigate this there is a built in condition
  that the shutdown is not performed if there is power from the changer.

## Aknowledgents

Many thanks to [@Orgjvr](https://github.com/Orgjvr) who wrote the original
[ups_hat_e](https://github.com/Orgjvr/ups_hat_e) integration which this is based on.
