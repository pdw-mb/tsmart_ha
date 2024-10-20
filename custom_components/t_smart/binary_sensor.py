"""Binary Sensor platform for t_smart."""

from datetime import timedelta

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    COORDINATORS,
    DOMAIN,
)
from .entity import TSmartCoordinatorEntity

SCAN_INTERVAL = timedelta(seconds=5)


class TSmartBinarySensorEntity(TSmartCoordinatorEntity, BinarySensorEntity):
    """t_smart Binary Sensor class."""

    _attr_device_class = BinarySensorDeviceClass.POWER

    # Inherit name from DeviceInfo, which is obtained from actual device
    _attr_has_entity_name = True
    _attr_name = "Relay"

    @property
    def is_on(self):
        """Is the relay on."""
        return self._tsmart.relay


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATORS][config_entry.entry_id]
    async_add_entities([TSmartBinarySensorEntity(coordinator)])
