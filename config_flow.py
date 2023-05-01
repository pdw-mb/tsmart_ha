"""Config flow for T-Smart Thermostat integration."""
from __future__ import annotations

import logging
from typing import Any
from .tsmart import TSmart

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    # TODO Check if there are any devices that can be discovered in the network.
    devices = await TSmart.async_discover()
    return len(devices) > 0

config_entry_flow.register_discovery_flow(DOMAIN, "T-Smart Thermostat", _async_has_devices)
