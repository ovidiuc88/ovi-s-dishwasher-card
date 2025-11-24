# Dishwasher Card – HACS Integration

This integration installs a Lovelace card and helper configuration for a Home Assistant–connected dishwasher (Home Connect or similar).

## Features

- Automatic enumeration of dishwasher entities during setup
- Clean configuration flow for selecting:
  - Operation state sensor
  - Door sensor
  - Power switch
- Lovelace card auto-generation (optional)
- Works with BSH / Home Connect appliances
- Optional compatibility with custom energy & water forecast sensors

## Installation (HACS)

1. Add this repository as a Custom Repository in HACS
2. Install “Dishwasher Card”
3. Restart Home Assistant
4. Go to **Settings → Devices & Services → Add Integration**
5. Select **Dishwasher Card**
6. Choose the entities that match your dishwasher

## Optional Sensors

You may optionally provide:

- `sensor.water_consumption_forecast`
- `sensor.energy_consumption_forecast`

These are typically provided by custom components.

## Files Installed

This integration may optionally install:

- `/config/www/dishwasher.jpeg`
- `/config/lovelace/dishwasher_card.yaml`
- `/config/packages/dishwasher.yaml`

## Requirements

- Home Connect integration (or any integration exposing dishwasher entities)
- Working dishwasher entities for:
  - Operation state
  - Door state
  - Power switch

## Maintainer

Anonymous / Community
