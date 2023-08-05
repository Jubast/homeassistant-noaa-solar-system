# NOAA Solar

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

_Integration for Home Assistant to fetch Solar data from [NOAA Rest API][noaa_rest_api]._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Solar activity, wind and magnetic fields data.
`image` | Gifs of solar objects (currently lasco_c3 and suvi_304 only)

![Alt text](/images/dashboard.png "Solar Sensor and images.")

## Installation

You can install the component using either the HACS add-on or manually.

### HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Jubast&repository=homeassistant-noaa-solar-system&category=integration)

Or:

1. Go to you `HACS` integration, then `Integrations`.
1. Click the three dots in the right upper corner, then `Custom Repositories`.
1. Enter "Repository=`Jubast/homeassistant-noaa-solar-system`" and "Category=`Integration`".
1. Press `Explore and download repositories` and search for `noaa solar`, then `Download`.

### Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `noaa_solar`.
1. Download _all_ the files from the `custom_components/noaa_solar/` directory (folder) in this repository (or Release .zip).
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "NOAA Solar"

## Configuration is done in the UI

Default settings should be fine for most use cases.

1. Enter the url of the NOAA Rest API.
1. Enter the poll interval.

![Alt text](/images/configuration.png "Configuration example.")

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[noaa_rest_api]: https://services.swpc.noaa.gov/
[commits-shield]: https://img.shields.io/github/commit-activity/y/Jubast/homeassistant-noaa-solar-system.svg?style=for-the-badge
[commits]: https://github.com/Jubast/homeassistant-noaa-solar-system/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/ludeeus/integration_blueprint.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-jubast-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ludeeus/integration_blueprint.svg?style=for-the-badge
[releases]: https://github.com/Jubast/homeassistant-noaa-solar-system/releases
