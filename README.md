# Home Assistant integration for the UPS Hat (E) from Waveshare

Functionality is based on the [Waveshare wiki](https://www.waveshare.com/wiki/UPS_HAT_(E))
for this device.

_Note: This is for the (E) version only._

## Instructions

### configuration.yaml

   ```
   ups_hat_e:
     addr: 0x2d                # Optional, default 0x2d
     name: UPS                 # Optional, default HA Pi UPS
     unique_id: ups_hat_e      # Optional, default ha_pi_ups
     scan_interval: 60         # Optional, default 30 seconds
   ```

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
  There is a risk HA is not gracefully shutdown. To mitigate this I have added a experimantal
  extra delay (10s) but it might not be enough.

* A reset of the HA will also trigger the UPS shutdown, i.e. there is currently nothing
  diffentiating between reset and shutdown. To mitigate this there is a built in condition
  that the shutdown is not performed if there is power from the changer.

## Aknowledgents

Many thanks to [@Orgjvr](https://github.com/Orgjvr) who write the original
[ups_hat_e](https://github.com/Orgjvr/ups_hat_e) integration which this is based on.
