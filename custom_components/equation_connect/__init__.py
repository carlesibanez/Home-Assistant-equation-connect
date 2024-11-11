import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, PLATFORMS
from .EquationConnect.EquationConnectAPI import API

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Equation Connect integration from a config entry."""
    email = entry.data["email"]
    password = entry.data["password"]

    # Initialize API
    api = await hass.async_add_executor_job(API, email, password)
    hass.data[DOMAIN] = api

    # Set up platforms (like climate, switch)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload the Equation Connect integration."""
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data.pop(DOMAIN)
    return True
