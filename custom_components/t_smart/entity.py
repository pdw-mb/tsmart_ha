from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import (
    DOMAIN,
)
from .coordinator import DeviceDataUpdateCoordinator

from typing import Any


class TSmartCoordinatorEntity(CoordinatorEntity[DeviceDataUpdateCoordinator]):
    def __init__(self, coordinator: DeviceDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._tsmart = coordinator.device
        self._attr_unique_id = self._tsmart.device_id

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within our domain
                (DOMAIN, self.unique_id)
            },
            name=self._tsmart.name,
            manufacturer="Tesla Ltd.",
            model="T-Smart",
        )
