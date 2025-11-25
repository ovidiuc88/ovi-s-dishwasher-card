from __future__ import annotations

import logging
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector
from homeassistant.helpers import entity_registry as er_helper

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def _gather_entities(hass: HomeAssistant, domain_prefix: str) -> list[str]:
    """Return sorted list of entity_ids that belong to a given domain (sensor, switch...)."""
    return sorted([s.entity_id for s in hass.states.async_all() if s.entity_id.startswith(domain_prefix + ".")])


def _suggest_candidates(hass: HomeAssistant) -> dict:
    """Heuristic scan for dishwasher-like entities; returns suggested defaults (may be empty strings)."""
    suggestions = {
        "operation": "",
        "power": "",
        "door": "",
        "start_button": "",
        "stop_button": "",
        "progress": "",
    }

    terms = ("dishwash", "dishwasher", "home_connect", "bosch", "siemens", "dishcare")

    for st in hass.states.async_all():
        eid = st.entity_id.lower()
        name = (st.name or "").lower()
        for t in terms:
            if t in eid or t in name:
                domain = eid.split(".")[0]
                if domain == "sensor" and not suggestions["operation"]:
                    suggestions["operation"] = eid
                if domain == "switch" and not suggestions["power"]:
                    suggestions["power"] = eid
                if domain == "binary_sensor" and not suggestions["door"]:
                    suggestions["door"] = eid
                if domain == "button":
                    if not suggestions["start_button"]:
                        suggestions["start_button"] = eid
                    elif not suggestions["stop_button"]:
                        suggestions["stop_button"] = eid
                if domain == "sensor" and ("progress" in eid or "program" in eid) and not suggestions["progress"]:
                    suggestions["progress"] = eid

    # If nothing found for operation, pick first sensor as a fallback
    if not suggestions["operation"]:
        for st in hass.states.async_all():
            if st.entity_id.startswith("sensor."):
                suggestions["operation"] = st.entity_id
                break

    return suggestions


class DishwasherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the dishwasher card."""

    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Initial step: show auto-detect / manual form with entity selectors."""
        if user_input is not None:
            # Validate that operation entity exists
            if not user_input.get("operation_entity"):
                return await self._show_form(errors={"operation_entity": "required"})

            return self.async_create_entry(title="Dishwasher Card", data=user_input)

        # Prepare lists for selectors using state registry (works even when entity_registry is not available)
        sensor_list = _gather_entities(self.hass, "sensor")
        binary_list = _gather_entities(self.hass, "binary_sensor")
        switch_list = _gather_entities(self.hass, "switch")
        button_list = _gather_entities(self.hass, "button")

        # Avoid passing an empty list directly to vol.In (vol.In([]) would fail). Use a small fallback list.
        sensor_choices = sensor_list if sensor_list else ["sensor.example_operation"]
        binary_choices = binary_list if binary_list else ["binary_sensor.example_door"]
        switch_choices = switch_list if switch_list else ["switch.example_power"]
        button_choices = button_list if button_list else ["button.example_start"]

        suggestions = _suggest_candidates(self.hass)

        schema = vol.Schema({
            vol.Required("operation_entity", default=suggestions.get("operation", "")):
                vol.In(sensor_choices),
            vol.Optional("power_entity", default=suggestions.get("power", "")):
                vol.In(switch_choices + [""]),
            vol.Optional("door_entity", default=suggestions.get("door", "")):
                vol.In(binary_choices + [""]),
            vol.Optional("start_button", default=suggestions.get("start_button", "")):
                vol.In(button_choices + [""]),
            vol.Optional("stop_button", default=suggestions.get("stop_button", "")):
                vol.In(button_choices + [""]),
            vol.Optional("progress_entity", default=suggestions.get("progress", "")):
                vol.In(sensor_choices + [""]),
            vol.Optional("water_forecast", default=""):
                vol.In(sensor_choices + [""]),
            vol.Optional("energy_forecast", default=""):
                vol.In(sensor_choices + [""]),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    async def _show_form(self, errors: dict | None = None):
        """Helper to re-show the form with errors."""
        # fallback to simple re-run of main step (keeps code simple)
        return await self.async_step_user(None)
