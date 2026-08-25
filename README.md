# Home Assistant integration for the UPS Hat (E) from Waveshare

Functionality is based on the [Waveshare wiki](https://www.waveshare.com/wiki/UPS_HAT_(E))
for this device.

_Note: This is for the (E) version only._

![UPS HAT (E) for Raspberry](https://github.com/CLusth/ups_hat_e/blob/master/images/UPS-HAT-E-details-1.jpg?raw=true)

## Installation

The integration can be installed using [HACS](https://hacs.xyz/). The integrations is not
available in the default repositories, so you will need to add the URL of this repository
as a custom repository to HACS (see [here](https://hacs.xyz/docs/faq/custom_repositories)).

Alternatively you can use the button below:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=CLusth&repository=ups_hat_e&category=Integration)

## Instructions

Add the integration through **Settings -> Devices & services -> Add integration**
and search for **Waveshare Pi UPS Hat (E)**. Enter the I2C address, device name,
unique ID, and scan interval in the setup form.

The scan interval can be changed later from the integration's **Configure** menu.

_Note: If you previosly have installed (v1.0.3 or earlier) this integration you need to remove old configuration from the configuran.yaml file_

### Example automation

Simple automation that trigger shutdown before the batttery is running out.

   ```
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

## Known issues

* The built in timer between triggering shutdown and when the power is cut is very short (~30s).
  There is a risk HA is not gracefully shutdown. To mitigate this I have added a configurable delay (15s) but it might not be enough.

* A reset of the HA will also trigger the UPS shutdown, i.e. there is currently nothing
  diffentiating between reset and shutdown. To mitigate this there is a built in condition
  that the shutdown is not performed if there is power from the changer.

## Aknowledgents

Many thanks to [@Orgjvr](https://github.com/Orgjvr) who wrote the original
[ups_hat_e](https://github.com/Orgjvr/ups_hat_e) integration which this is based on.
