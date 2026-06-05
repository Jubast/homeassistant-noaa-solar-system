---
agent: "agent"
tools: ["search/codebase", "edit", "search", "runCommands"]
description: "Add a new entity to an existing device while maintaining proper device grouping"
---

# Add Entity to Device

Your goal is to add a new entity to an existing device in this Home Assistant integration.

If not provided, ask for:

- Entity type (sensor, binary_sensor, switch, number, select, etc.)
- Entity name and purpose
- Which device it belongs to
- Data source from coordinator

## Requirements

**Entity Implementation:**

- Add the entity class in the appropriate platform module (for example `sensor.py` or `image.py`)
- Inherit from `NOAASolarEntity` and platform base class
- Ensure `device_info` property returns same identifiers as other entities on this device
- Coordinate device_info generation via shared helper(s) in `utils/` when needed

**Device Grouping:**

- All entities for the same physical device must return identical `device_info`
- Use consistent device identifiers (via_device, serial number, or unique ID)
- Ensure manufacturer, model, and name match across entities
- Consider using shared device info generator if multiple entities exist

**Platform Registration:**

- Add entity setup/registration in the platform module where `async_setup_entry` is defined
- Maintain alphabetical order if applicable
- Ensure entity description includes all required fields

**Coordinator Data:**

- Entity must read from `self.coordinator.data`
- Access shared device state via coordinator
- Handle missing data gracefully (set `_attr_available = False`)
- Never fetch data directly in entity

**Translations:**

- Add entity name and description to `translations/en.json`
- Update `translations/de.json` with German translation
- Keep naming consistent with other entities on the device

**Verification:**

- Restart Home Assistant to load new entity
- Verify entity appears under correct device in UI
- Check that all entities for device are grouped together
- Confirm entity state updates correctly

**Code Quality:**

- Follow existing entity patterns for this device
- Use consistent naming scheme for entity_id
- Add proper docstrings (Google-style)
- Run `scripts/lint` to validate before completion

**Related Files:**

- Platform module: `custom_components/noaa_solar/[platform].py`
- Shared helpers: `custom_components/noaa_solar/utils/`
- Translations: `translations/*.json`
- Documentation: Reference [#file:docs/development/ARCHITECTURE.md]

**DO NOT create tests unless explicitly requested.**
