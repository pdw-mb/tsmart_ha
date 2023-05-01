import voluptuous as vol
import logging

from homeassistant.const import (
        CONF_IP_ADDRESS,
        UnitOfTemperature,
    )
from homeassistant.components.climate import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.climate import (
    ATTR_HVAC_MODE,
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_COMFORT,
    PRESET_ECO,
    PRESET_NONE,
    ClimateEntity,
    HVACMode,
    ClimateEntityFeature,
)
from .tsmart import TSmart, TSmartMode
from .const import (
    DOMAIN, 
    DEVICE_IDS,
    PRESET_MANUAL,
    PRESET_SMART,
    PRESET_TIMER,
    )

from datetime import timedelta

_LOGGER = logging.getLogger(__name__)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
    }
)


SCAN_INTERVAL = timedelta(seconds=5)

PRESET_MAP = {
    PRESET_MANUAL: TSmartMode.MANUAL,
    PRESET_ECO: TSmartMode.ECO,
    PRESET_SMART: TSmartMode.SMART,
    PRESET_TIMER: TSmartMode.TIMER,
    PRESET_AWAY: TSmartMode.TRAVEL,
    PRESET_BOOST: TSmartMode.BOOST
}

class TSmartEntity(ClimateEntity):

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT]
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE
    _attr_preset_modes = list(PRESET_MAP.keys())
    _attr_icon = "mdi:water-boiler"
    
    def __init__(self, tsmart) -> None:
        self._tsmart = tsmart
        self._attr_unique_id = self._tsmart.device_id

    async def async_update(self):
        await self._tsmart._async_get_status()

    @property
    def hvac_mode(self):
        return HVACMode.HEAT if self._tsmart.power else HVACMode.OFF

    async def async_set_hvac_mode(self, hvac_mode):
        await self._tsmart._async_control_set(hvac_mode == HVACMode.HEAT, PRESET_MAP[self.preset_mode], self.current_temperature)

    async def async_set_preset_mode(self, preset_mode):
        await self._tsmart._async_control_set(self.hvac_mode == HVACMode.HEAT, PRESET_MAP[preset_mode], self.current_temperature)

    @property
    def current_temperature(self):
        return self._tsmart.temperature

    @property
    def target_temperature(self):
        return self._tsmart.setpoint

    def _climate_preset(self, tsmart_mode):
        return next((k for k, v in PRESET_MAP.items() if v == tsmart_mode), None)

    @property
    def preset_mode(self):
        return self._climate_preset(self._tsmart.mode)

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self.unique_id)
            },
            name = self._tsmart.name,
            name_by_user = self._tsmart.name,
            manufacturer = "Tesla Ltd.",
            model = "T-Smart",
        )

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:

    _LOGGER.error("setup_platform called")
    ip = config[CONF_IP_ADDRESS]
    #add_entities([TSmartEntity(TSmart(ip))])

async def async_discover_devices(hass: HomeAssistant) -> list[TSmartEntity]:
    """Attempt to discover new lights."""
    devices = await TSmart.async_discover()

    # Filter out already discovered lights
    new_devices = [
        d
        for d in devices
        if d.device_id not in hass.data[DOMAIN][DEVICE_IDS]
    ]

    devices = []
    for device in new_devices:
        hass.data[DOMAIN][DEVICE_IDS].add(device.device_id)
        devices.append(TSmartEntity(device))

    return devices

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    devices = await async_discover_devices(hass)
    async_add_entities(devices)
    


#async def async_setup_entry(hass, config_entry, async_add_devices):
#    """Set up entry."""
#    _LOGGER.info(config_entry)
#    async_add_devices([
#        #TSmartEntity(TSmart("192.168.0.160")),
#        #TSmartEntity(TSmart("192.168.0.161"))
#        ], True)


