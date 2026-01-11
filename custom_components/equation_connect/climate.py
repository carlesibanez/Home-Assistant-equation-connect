from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode, ClimateEntityFeature
from homeassistant.const import UnitOfTemperature
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    # Retrieve the API and Devices stored in __init__.py
    api = hass.data[DOMAIN]["api"]
    
    # NOTE: Ensure you fetched 'devices' in __init__.py using 'await api.get_devices()'
    # If not, you might need to fetch them here.
    devices = hass.data[DOMAIN].get("devices", []) 
    
    entities = [
        EquationConnectThermostat(api, device) 
        for device in devices 
        if device.get("data", {}).get("type") == "radiator"
    ]
    async_add_entities(entities, True)

class EquationConnectThermostat(ClimateEntity):
    def __init__(self, api, device):
        self._api = api
        self._device = device
        self._attr_name = "Radiator " + device.get("data", {}).get("name", "")
        # Using the serial number as the unique ID
        self._attr_unique_id = device.get("serialnumber")
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_hvac_mode = HVACMode.OFF

    @property
    def device_info(self):
        """Return device information to tie entities to a single device."""
        return {
            "identifiers": {(DOMAIN, self._attr_unique_id)},
            "name": self._device["data"]["name"],
            "manufacturer": "Equation",
            "model": "Radiator",
            "sw_version": self._device["firmware"]["firmware_version_device"],
        }

    @property
    def hvac_modes(self):
        return [HVACMode.HEAT, HVACMode.OFF]
    
    @property
    def supported_features(self):
        return ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get("temperature")
        
        # CHANGED: Direct await call (No more run_in_executor)
        await self._api.set_device_temperature(self._attr_unique_id, temperature)
        
        # Optimistically update the local state so the UI feels snappy
        self._attr_target_temperature = temperature
        self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        power_state = hvac_mode == HVACMode.HEAT
        
        # CHANGED: Direct await call
        await self._api.set_device_power(self._attr_unique_id, power_state)
        
        self._attr_hvac_mode = hvac_mode
        self.async_write_ha_state()

    async def async_turn_on(self):
        """Handle turning on the device."""
        await self.async_set_hvac_mode(HVACMode.HEAT)
    
    async def async_turn_off(self):
        """Handle turning off the device."""
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # CHANGED: Direct await call
        # This is much more efficient than spinning up a thread
        try:
            device = await self._api.get_device(self._attr_unique_id)
            
            if device:
                self._device = device # Update internal reference
                self._attr_target_temperature = device["data"]["temp"]
                self._attr_hvac_mode = HVACMode.HEAT if device["data"]["power"] else HVACMode.OFF
        except Exception:
            # It's good practice to catch errors here so one failed update 
            # doesn't crash the entity
            pass