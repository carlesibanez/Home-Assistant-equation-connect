import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, PLATFORMS
from EquationConnectSDK.EquationConnectAPI import API

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Equation Connect integration from a config entry."""
    email = entry.data["email"]
    password = entry.data["password"]

    # Get the session
    session = async_get_clientsession(hass)

    # Initialize API
    api = API(email, password, session)

    user = await api.authenticate()
    if not user:
        return False # Setup failed

    try:
        _LOGGER.info(f"Authenticated user: {user['email']}")
        _LOGGER.info("Fetching devices from Equation Connect API...")
        devices = await api.get_devices()
        _LOGGER.info(f"Found {len(devices)} devices in Firebase.")
    except Exception as e:
        _LOGGER.error(f"Error fetching devices: {e}")
        return False

    # Store API instance in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["api"] = api
    hass.data[DOMAIN]["devices"] = devices

    # Set up platforms (like climate, switch)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload the Equation Connect integration."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        # Clean up data
        hass.data[DOMAIN].pop("api", None)
        hass.data[DOMAIN].pop("devices", None)
    return unload_ok
