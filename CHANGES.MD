Moved tsmart library into custom component to allow rearchitecture of both, can be moved back into library.
Re-ordered params of TSmart class, mandatory IP but optional id & name to allow resolution later.
New async_get_configuration method within library to allow getting of device_id and name, don't get all fields as we won't need them.

Coordinators now loaded at platform init and shared between entities of the same device.

Discovery now in config flow with timeout prompting for manual IP.

Config flow now allows re-configure to change IP.

Config entries store IP address, id and name of device and used at component load rather than discovery, allows device to come online after HA start and be recognised.

Updated readme with HACS easy install link, also specifying to use a fixed IP.

Added min HA version checking to be 2024.2 to cope with new climate requirements.
