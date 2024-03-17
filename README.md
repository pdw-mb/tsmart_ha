# Tesla T-Smart thermostat Home Assistant integration

This repository provides a custom component for enabling a [Tesla T-Smart immersion heater thermostat](https://www.teslauk.com/product/7795/t-smart-thermostat) to be used with [Home Assistant](https://home-assistant.io).

**This is a community developed and maintained project, and is not supported or endorsed by Tesla (UK) Ltd.**

## Installation

You can install the component using either the [HACS add-on](https://hacs.xyz) or manually.

### HACS Installation

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

This component is available as a default repository in HACS.  To enable it:

* Go to HACS
* Select "Integrations" 
* Click "Explore and Download Repositories"
* Search for "T-Smart" and select "T-Smart Thermostat"
* Click Download
* Restart Home Assistant

### Manual Installation

* Copy (or link) the `custom_components/t_smart/` directory from this repository into your `configuration/custom_components/` directory.

* Restart Home Assistant.

## Discover thermostats

After restarting Home Assistant:

* Go to Settings -> Devices & services -> Add Integration.

* Find "T-Smart Thermostat" and click on it.

* Click "OK" and any thermostats on your network should be discovered, or you can manually enter their IP address if not found.  
Thermostats should have a fixed IP address as the IP address.

