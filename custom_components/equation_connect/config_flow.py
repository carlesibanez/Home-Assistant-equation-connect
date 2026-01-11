import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.core import callback
from .const import DOMAIN
from EquationConnectSDK.EquationConnectAPI import API

import homeassistant.helpers.config_validation as cv

class EquationConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)
            email = user_input["email"]
            password = user_input["password"]

            # Initialize API
            api = API(email, password, session)

            # Attempt authentication here to verify credentials
            try:
                user = await api.authenticate()

                if not user:
                    errors["base"] = "invalid_auth"
                else:
                    return self.async_create_entry(
                        title=email,
                        data=user_input
                    )
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("email"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
        )
