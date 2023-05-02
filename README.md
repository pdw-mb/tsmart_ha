# Tesla T-Smart thermostat Home Assistant integration

This repository provides a custom component for enabling a [Tesla T-Smart immersion heater thermostat](https://www.teslauk.com/product/7795/t-smart-thermostat) to be used with [Home Assistant](https://home-assistant.io).

## Installation

* Copy this repository ionto the `configuration/custom_components/` directory.  If
you have SSH access to your HA installation enabled, you can do it like this:

```
ssh root@homeassistant 
cd /configuration/custom_components
git clone https://github.com/pdw-mb/tsmart_ha.git
```

* Restart Home Assistant.

* Go to Settings -> Devices & services -> Add Integration.

* Find "T-Smart Thermostat" and click on it.

* Click "OK" and any thermostats on your network should be discovered.



