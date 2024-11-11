import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN
from .EquationConnect.EquationConnectAPI import EquationConnectAPI

import homeassistant.helpers.config_validation as cv

class EquationConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            email = user_input["email"]
            password = user_input["password"]

            # Attempt authentication here to verify credentials
            try:
                if await self.hass.async_add_executor_job(
                    self.authenticate, email, password
                ):
                    return self.async_create_entry(
                        title="Equation Connect",
                        data=user_input,
                    )
                else:
                    errors["base"] = "auth_error"
            except Exception:
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("email"): cv.string,
                    vol.Required("password"): cv.string,
                }
            ),
            errors=errors,
        )

    def authenticate(self, email, password):
        # Authenticate user with Equation Connect API
        try:
            api = EquationConnectAPI(email, password)
            return True if api.user else False
        except Exception:
            return False
