
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import entity_registry
from .const import DOMAIN

class DishwasherFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input:
            return self.async_create_entry(
                title="Dishwasher Setup", data=user_input
            )

        er = await entity_registry.async_get_registry(self.hass)

        def list_entities(prefix):
            return [
                e.entity_id
                for e in er.entities.values()
                if e.entity_id.startswith(prefix + ".")
            ]

        sensors = list_entities("sensor") or ["sensor.example_operation"]
        doors = list_entities("binary_sensor") or ["binary_sensor.example_door"]
        switches = list_entities("switch") or ["switch.example_power"]

        schema = vol.Schema({
            vol.Required("operation_sensor"): vol.In(sensors),
            vol.Optional("door_sensor"): vol.In(doors),
            vol.Optional("power_switch"): vol.In(switches),
        })

        return self.async_show_form(step_id="user", data_schema=schema)
