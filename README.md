This is a fork of https://github.com/pdw-mb/tsmart_ha, rearchitected to support manual IP addresses, choice of sensors and identification of thermostats when they are turned on after HA has started.

As this has moved to IP addresses rather than broadcast discovery you will need a fixed IP address on your thermostat and re-add it when changing to this integration.

When merged into the pdw-mb HACS version you should switch to using that.

# Tesla T-Smart thermostat Home Assistant integration


### Manual Installation

* You should take the latest zip from releases 
* To install, place the contents of the zip into the `<config directory>/custom_components` folder of your Home Assistant installation.  
* Restart Home Assistant  


## Discover thermostats

After restarting Home Assistant:

* Go to Settings -> Devices & services -> Add Integration.

* Find "T-Smart Thermostat" and click on it.

* Click "OK" and any thermostats on your network should be discovered, or you can manually enter their IP address if not found.  
Thermostats must have a fixed IP address to avoid re-discovery.

* If your change the IP address of your thermostat you will have to modify this in the integration by going into settings/configure.

* By default the integration takes the average of both sensors within the thermostats, this can be changed by going into settings, configuring the thermostat and choosing a different temperature mode. For vertical thermostats the High setting will match the display and the app.

<!---->
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
