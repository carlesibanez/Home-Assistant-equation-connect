
# Home Assistant Equation Connect

This is an Unofficial Home Assistant (HA) integration for Equation radiators sold at Leroy Merlin, which can be controlled using the EquationConnect mobile app.  
This integration creates a HA [`ClimateEntity`](https://developers.home-assistant.io/docs/core/entity/climate/) for each radiator a user has, therefore with the HA climate card the temperature can be controlled as well as turning the radiator on and off.  
The `equation_connect` integration uses the [EquationConnect](https://github.com/carlesibanez/EquationConnect) python package to handle the calls to the Firebase API. For further details on how the API works refer to the EquationConnect package documentation.


## Installation

To use the integration, download the latest release and copy the `equation_connect` directory in `custom_components` to your `custom_components` directory (in your `homeassistant` directory, or your `config` directory if using Docker). You might need to restart HA after copying the integration for HA to detect it. Then follow these steps:

1. Navigate to HA Settings, and click on `Devices & Services`.
2. Click the `Add Integration` button in the bottom right of the page. 
3. In the pop up window look for **Equation Connect (Unofficial)** and click it to set it up.
4. On the new window, fill the *email* and *password* fields. These are the same credentials used to sign in on the app.
5. If everything went good, click `Finish`. The radiators should now be visible as different entities.

    
## Current Features and TODO's

- [x]  Power ON/OFF each radiator  
- [x]  Change radiator temperature  
- [ ]  Change radiator mode (ICE/ECO/COMFORT)
- [ ]  Represent each radiator as one device. (To manage different properties, e.g. backlight, mode...)  
- [ ]  Publish the integration on HACS.



