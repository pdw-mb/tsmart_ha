[![hacs][hacsbadge]][hacs]

# Tesla T-Smart thermostat Home Assistant integration

This repository provides a custom component for enabling a [Tesla T-Smart immersion heater thermostat](https://www.teslauk.com/product/7795/t-smart-thermostat) to be used with [Home Assistant](https://home-assistant.io).

**This is a community developed and maintained project, and is not supported or endorsed by Tesla (UK) Ltd.**

## Installation

You can install the component using either the [HACS add-on](https://hacs.xyz) or manually.

### HACS Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=pdw-mb&repository=tsmart_ha&category=Integration)

Or

* Search for `T-Smart Thermostat` in HACS and install it under the "Integrations" category.
* Click Download

Restart Home Assistant  
In the HA UI go to Settings -> Integrations click "+" and search for "T-Smart Thermostat"

### Manual Installation

* You should take the latest [published release](https://github.com/pdw-mb/tsmart_ha/releases).  
* To install, place the contents of `custom_components` into the `<config directory>/custom_components` folder of your Home Assistant installation.  
* Restart Home Assistant  


## Discover thermostats

After restarting Home Assistant:

* Go to Settings -> Devices & services -> Add Integration.

* Find "T-Smart Thermostat" and click on it.

* Click "OK" and any thermostats on your network should be discovered, or you can manually enter their IP address if not found.  
Thermostats must have a fixed IP address to avoid re-discovery.

<!---->
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
