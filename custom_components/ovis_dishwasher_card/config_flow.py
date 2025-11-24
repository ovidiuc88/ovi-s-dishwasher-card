import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import entity_registry
from .const import DOMAIN

class DishwasherFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Dishwasher Card."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """First step: select dishwasher entities."""
        er = await entity_registry.async_get_registry(self.hass)

        def list_entities(prefix):
            """Return all entities beginning with domain prefix."""
            return sorted(
                e.entity_id
                for e in er.entities.values()
                if e.entity_id.startswith(prefix + ".")
            )

        sensors = list_entities("sensor") or ["sensor.example_operation"]
        binary_sensors = list_entities("binary_sensor") or ["binary_sensor.example_door"]
        switches = list_entities("switch") or ["switch.example_power"]

        schema = vol.Schema({
            vol.Required(
                "operation_sensor",
                description="Sensor showing dishwasher operational state"
            ): vol.In(sensors),

            vol.Required(
                "door_sensor",
                description="Binary sensor reporting door open/closed"
            ): vol.In(binary_sensors),

            vol.Required(
                "power_switch",
                description="Switch that controls dishwasher power"
            ): vol.In(switches),

            vol.Optional(
                "water_forecast_sensor",
                default="",
                description="Optional water usage forecast sensor"
            ): vol.In(sensors + [""]),

            vol.Optional(
                "energy_forecast_sensor",
                default="",
                description="Optional energy usage forecast sensor"
            ): vol.In(sensors + [""]),
        })

        if user_input is not None:
            return self.async_create_entry(
                title="Dishwasher Card",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=schema
        )
