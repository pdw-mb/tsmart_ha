"""Config flow for T-Smart Thermostat integration."""
from __future__ import annotations

import logging
import asyncio
from typing import Any
from tsmart import TSmart

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from homeassistant.const import (
    CONF_IP_ADDRESS,
)

from .const import (
    DOMAIN,
    DEVICE_IDS,
    CONF_DEVICE_ID,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): str,
    }
)

CONFIG_VERSION = 1

TIMEOUT = 5

def _base_schema(discovery_info=None):
    """Generate base schema."""
    base_schema = {}
    if discovery_info and CONF_IP_ADDRESS in discovery_info:
        base_schema.update(
            {
                vol.Required(
                    CONF_IP_ADDRESS,
                    description={"suggested_value": discovery_info[CONF_IP_ADDRESS]},
                ): str,
            }
        )
    else:
        base_schema.update({vol.Required(CONF_IP_ADDRESS): str})

    if discovery_info and CONF_DEVICE_ID in discovery_info:
        base_schema.update(
            {
                vol.Required(
                    CONF_DEVICE_ID,
                    description={"suggested_value": discovery_info[CONF_DEVICE_ID]},
                ): str,
            }
        )
    else:
        base_schema.update({vol.Required(CONF_DEVICE_ID): str})

    return vol.Schema(base_schema)

class TSmartConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for TSmart Thermostat."""

    VERSION = CONFIG_VERSION

    def __init__(self) -> None:
        """Initialize an instance of the TSmart config flow."""
        self.data_schema = _base_schema()
        self.discovery_info = None

    async def _discover(self, uuid=None):
        """Discover an unconfigured TSmart thermostat."""
        self.discovery_info = None

        devices = await TSmart.async_discover()

        # Filter out already discovered devices
        new_devices = [
            d for d in devices if d.device_id not in self.hass.data[DOMAIN][DEVICE_IDS]
        ]

        if len(new_devices) == 0:
            return

        new_device = new_devices[0]

        self.discovery_info = {
            CONF_IP_ADDRESS: new_device.ip,
            CONF_DEVICE_ID: new_device.device_id,
        }
        _LOGGER.debug("Discovered thermostat: %s", self.discovery_info)

        # update with suggested values from discovery
        self.data_schema = _base_schema(self.discovery_info)


    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            # Try to connect and do any error checking here
            device = TSmart(device_id = "X", ip = user_input[CONF_IP_ADDRESS])

            # Save instance
            if not errors:
                return self.async_create_entry(
                    title=f"T-Smart: {user_input[CONF_IP_ADDRESS]}", data=user_input
                )

        # no device specified, see if we can discover an unconfigured thermostat
        try:
            async with asyncio.timeout(TIMEOUT):
                await self._discover()
            return await self.async_step_edit()
        except TimeoutError:
            errors["base"] = "no_thermostat_found"

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_edit(self, user_input=None):
        """Edit a discovered or manually inputted thermostat."""
        errors = {}
        if user_input:
            error = await self._validate_input(user_input)
            if not error:
                return self.async_create_entry(
                    title=user_input[CONF_DEVICE_ID], data=user_input
                )
            errors["base"] = error

        return self.async_show_form(
            step_id="edit", data_schema=self.data_schema, errors=errors
        )

# async def _async_has_devices(hass: HomeAssistant) -> bool:
#     """Return if there are devices that can be discovered."""
#     # Stop as soon as we find any device.  Do a full scan later.
#     devices = await TSmart.async_discover(stop_on_first=True)
#     return len(devices) > 0


# config_entry_flow.register_discovery_flow(
#     DOMAIN, "T-Smart Thermostat", _async_has_devices
# )
