from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode, ClimateEntityFeature
from homeassistant.const import UnitOfTemperature
import asyncio
from .const import DOMAIN

# async def async_setup_entry(hass, config_entry, async_add_entities):
#     api = hass.data[DOMAIN]
#     devices = await hass.async_add_executor_job(api.get_devices) # Fetch all devices
#     entities = [EquationConnectThermostat(api, device) for device in devices if device.get("data", {}).get("type") == "radiator"]
#     async_add_entities(entities, True)

async def async_setup_entry(hass, config_entry, async_add_entities):
    api = hass.data[DOMAIN]["api"]
    devices = hass.data[DOMAIN]["devices"]
    entities = [EquationConnectThermostat(api, device) for device in devices if device.get("data", {}).get("type") == "radiator"]
    async_add_entities(entities, True)

class EquationConnectThermostat(ClimateEntity):
    def __init__(self, api, device):
        self._api = api
        self._device = device
        self._attr_name = "Thermostat" # device.get("data", {}).get("name", "Radiator")
        self._attr_unique_id = device.get("serialnumber")
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_hvac_mode = HVACMode.OFF

    @property
    def device_info(self):
        """Return device information to tie entities to a single device."""
        return {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": self._device["data"]["name"],  # or use another meaningful name
            "manufacturer": "Equation",  # Substitute with actual manufacturer if known
            "model": "Radiator",
            "sw_version": self._device["firmware_info"]["version"],
        }

    async def async_set_temperature(self, **kwargs):
        loop = asyncio.get_running_loop()
        temperature = kwargs.get("temperature")
        await loop.run_in_executor(None, self._api.set_device_temperature, self._attr_unique_id, temperature)

    async def async_set_hvac_mode(self, hvac_mode):
        loop = asyncio.get_running_loop()
        power_state = hvac_mode == HVACMode.HEAT
        await loop.run_in_executor(None, self._api.set_device_power, self._attr_unique_id, power_state)
        self._attr_hvac_mode = hvac_mode
        await self.async_update_ha_state()

    @property
    def hvac_modes(self):
        return [HVACMode.HEAT, HVACMode.OFF]
    
    @property
    def supported_features(self):
        """Return the list of supported features."""
        return ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF

    async def async_turn_on(self):
        """Handle turning on the device."""
        await self.async_set_hvac_mode(HVACMode.HEAT)
    
    async def async_turn_off(self):
        """Handle turning off the device."""
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_update(self):
        loop = asyncio.get_running_loop()
        device = await loop.run_in_executor(None, self._api.get_device, self._attr_unique_id)
        self._attr_target_temperature = device["data"]["temp"]
        self._attr_hvac_mode = HVACMode.HEAT if device["data"]["power"] else HVACMode.OFF
