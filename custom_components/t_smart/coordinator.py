from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from datetime import timedelta

from tsmart import TSmart
from .const import (
    DOMAIN,
)

import logging

_LOGGER = logging.getLogger(__name__)


class DeviceDataUpdateCoordinator(DataUpdateCoordinator):
    """Manages polling for state changes from the device."""

    def __init__(self, hass: HomeAssistant, device: TSmart) -> None:
        """Initialize the data update coordinator."""
        DataUpdateCoordinator.__init__(
            self,
            hass,
            _LOGGER,
            name=f"{DOMAIN}-{device.device_id}",
            update_interval=timedelta(seconds=10),
        )
        self.device = device
        self._error_count = 0
        self._attr_unique_id = device.device_id

    async def _async_update_data(self):
        """Update the state of the device."""
        await self.device.async_get_status()
