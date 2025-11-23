
import os, shutil
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry):
    integration_dir = os.path.dirname(__file__)

    def copy_asset(rel_path, target_rel):
        src = os.path.join(integration_dir, rel_path)
        dst = hass.config.path(target_rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

    try:
        copy_asset("assets/dishwasher.jpeg", "www/dishwasher.jpeg")
        copy_asset("lovelace/dashboard.yaml", "lovelace/dishwasher_dashboard.yaml")
        copy_asset("package/dishwasher.yaml", "packages/dishwasher.yaml")

        hass.components.persistent_notification.create(
            "Dishwasher Card installed. Restart Home Assistant.",
            title="Installer",
        )
    except Exception as err:
        hass.components.persistent_notification.create(
            f"Installation failed: {err}", title="Installer"
        )
    return True
