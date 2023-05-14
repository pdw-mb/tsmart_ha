from __future__ import annotations
from homeassistant.core import HomeAssistant
from .const import (
    DOMAIN,
    COORDINATORS,
    DEVICE_IDS,
)
from .coordinator import DeviceDataUpdateCoordinator
from .tsmart import TSmart


class DiscoveryService:
    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        hass.data[DOMAIN].setdefault(COORDINATORS, [])

    async def async_discover_devices(self) -> list[TSmartEntity]:
        """Attempt to discover new devices."""
        devices = await TSmart.async_discover()

        # Filter out already discovered devices
        new_devices = [
            d for d in devices if d.device_id not in self.hass.data[DOMAIN][DEVICE_IDS]
        ]

        devices = []
        for device in new_devices:
            coordo = DeviceDataUpdateCoordinator(self.hass, device)
            self.hass.data[DOMAIN][COORDINATORS].append(coordo)
            self.hass.data[DOMAIN][DEVICE_IDS].add(device.device_id)

        return devices
