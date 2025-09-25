# Home Assistant integration for the UPS Hat (E) from Waveshare

Functionality is based on the [Waveshare wiki](https://www.waveshare.com/wiki/UPS_HAT_(E))
for this device.

_Note: This is for the (E) version only._

## Instructions

configuration.yaml

   ```
   ups_hat_e:
     addr: 0x2d                # Optional, default 0x2d
     name: UPS                 # Optional, default HA Pi UPS
     unique_id: ups_hat_e      # Optional, default ha_pi_ups
     scan_interval: 60         # Optional, default 30 seconds
   ```

## Aknowledgents

Many thanks to [@Orgjvr](https://github.com/Orgjvr) who write the original [ups_hat_e](https://github.com/Orgjvr/ups_hat_e)
integration which this is based on.
