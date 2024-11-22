
# Home Assistant Equation Connect

This is an Unofficial Home Assistant (HA) integration for Equation radiators sold at Leroy Merlin, which can be controlled using the EquationConnect mobile app.  
This integration creates a HA [`ClimateEntity`](https://developers.home-assistant.io/docs/core/entity/climate/) for each radiator a user has, therefore with the HA climate card the temperature can be controlled as well as turning the radiator on and off.  
The `equation_connect` integration uses the [EquationConnect](https://github.com/carlesibanez/EquationConnect) python package to handle the calls to the Firebase API. For further details on how the API works refer to the EquationConnect package documentation.


## Installation through HACS

To install the package through HACS, you can click this button, and then skip to step 4:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=carlesibanez&repository=Home-Assistant-equation-connect&category=Integration)

Otherwise, you can add the repository manually to HACS:  
1. Go to the HACS tabs on your Home Assistant installtion.
2. On the top right, click on the three dots. Then `Custom repositories` and add this repository:
    - __Repository__: [https://github.com/carlesibanez/Home-Assistant-equation-connect](https://github.com/carlesibanez/Home-Assistant-equation-connect)
    - __Type__: _Integration_
3. Click ADD to add it to your Custom repositories.
4. On the HACS search bar, look for _Equation Connect (Unofficial)_, click it to open the documentation and description.
5. On the bottom right, click _DOWNLOAD_. In case you want a specific version, use the dropdown on the pop up window to select it. Finally click _DOWNLOAD_.

Note: You eed to restart for the installation to take effect. Then continue with the [Initial setup](#initial-setup).


## Manual installation

To manually install the integration, download the latest release and copy the `equation_connect` directory in `custom_components` to your `custom_components` directory (in your `homeassistant` directory, or your `config` directory if using Docker). You might need to restart HA after copying the integration for HA to detect it. Then continue with the [Initial setup](#initial-setup).


## Initial setup

Once you have installed the integration, it is time to set it up.  
1. Navigate to HA Settings, and click on `Devices & Services` to open the dashboard. Or click the button below:  
[![Open your Home Assistant instance and show your integrations.](https://my.home-assistant.io/badges/integrations.svg)](https://my.home-assistant.io/redirect/integrations/)  
2. Click on `ADD INTEGRATION` in the bottom right and search for _Equation Connect (Unofficial)_.
4. On the new window, fill the *email* and *password* fields. These are the same credentials used to sign in on the app.
5. If everything went good, click `Finish`. The radiators should now be visible as different entities.

    
## Current Features and TODO's

- [x]  Power ON/OFF each radiator  
- [x]  Change radiator temperature  
- [x]  Represent each radiator as one device. (To manage different properties, e.g. backlight, mode...)  
- [ ]  Change radiator mode (ICE/ECO/COMFORT)
- [x]  Publish the integration on HACS.



