import voluptuous as vol
import logging

from homeassistant.const import (
    UnitOfTemperature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)

from .const import (
    DOMAIN,
    COORDINATORS,
)
from .coordinator import DeviceDataUpdateCoordinator
from .entity import TSmartCoordinatorEntity

from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=5)


class TSmartBinarySensorEntity(TSmartCoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.POWER

    # Inherit name from DeviceInfo, which is obtained from actual device
    _attr_has_entity_name = True
    _attr_name = "Relay"

    @property
    def is_on(self):
        return self._tsmart.relay


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    for coordinator in hass.data[DOMAIN][COORDINATORS]:
        async_add_entities([TSmartBinarySensorEntity(coordinator)])
