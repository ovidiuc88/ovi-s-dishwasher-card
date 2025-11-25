from __future__ import annotations

import os
import shutil
from homeassistant.core import HomeAssistant
from .const import DOMAIN

PLATFORM_NAME = "Dishwasher Card"

def _copy_resource(integration_dir: str, rel_src: str, hass: HomeAssistant, dst_folder: str, dst_name: str) -> None:
    """Copy resource bundled in integration to the HA config."""
    src = os.path.join(integration_dir, rel_src)
    dst = hass.config.path(dst_folder, dst_name)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)

async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    """Set up the integration and copy bundled files into the user's config."""
    integration_dir = os.path.dirname(__file__)

    try:
        _copy_resource(integration_dir, "dashboard/dashboard_dishwasher.yaml", hass, "lovelace", "dashboard_dishwasher.yaml")
        _copy_resource(integration_dir, "package/dishwasher.yaml", hass, "packages", "dishwasher.yaml")
        _copy_resource(integration_dir, "www/dishwasher.jpeg", hass, "www", "dishwasher.jpeg")

        hass.components.persistent_notification.create(
            "Dishwasher Card files copied to your config (lovelace/dashboard_dishwasher.yaml, packages/dishwasher.yaml, www/dishwasher.jpeg). Please restart Home Assistant to apply.",
            title=PLATFORM_NAME
        )
    except Exception as exc:
        hass.components.persistent_notification.create(
            f"Failed to install Dishwasher Card files: {exc}",
            title=f"{PLATFORM_NAME} - Error"
        )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data or {}
    return True

async def async_unload_entry(hass: HomeAssistant, entry) -> bool:
    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return True
