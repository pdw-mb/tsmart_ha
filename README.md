# Tesla T-Smart thermostat Home Assistant integration

This repository provides a custom component for enabling a [Tesla T-Smart immersion heater thermostat](https://www.teslauk.com/product/7795/t-smart-thermostat) to be used with [Home Assistant](https://home-assistant.io).

## Installation

You can install the component using either the [HACS add-on](https://hacs.xyz) or manually.

### HACS Installation

Use this link:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=pdw-mb&repository=tsmart_ha&category=integration)

Or:

* In HACS, click the three dots, then "Custom Repositories", and add:
    * Repository = `pdw-mb/tsmart_ha`
    * Category = `integration`
* Click "Explore and download repositories", select "T-Smart thermostat", click "Download" and then restart Home Assistant

### Manual Installation

* Copy (or link) the `custom_components/t_smart/` directory from this repository into your `configuration/custom_components/` directory.

* Restart Home Assistant.

## Discover thermostats

After restarting Home Assistant:

* Go to Settings -> Devices & services -> Add Integration.

* Find "T-Smart Thermostat" and click on it.

* Click "OK" and any thermostats on your network should be discovered.

At present, thermostats that are not available when the integration is loaded (either initially, or when Home Assistant restarts) won't be discovered.  If you need to add thermostats, or thermostats are not detected during a Home Assistant restart, you should use the "Reload" option on the "..." menu for the integration.



