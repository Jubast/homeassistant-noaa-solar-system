# AI Agent Instructions

This document provides guidance for AI coding agents working on this Home Assistant custom integration project.

## Project Overview

This is a Home Assistant custom integration for NOAA solar and space-weather data.

**Integration details:**

- **Domain:** `noaa_solar`
- **Title:** NOAA Solar
- **Repository:** Jubast/homeassistant-noaa-solar-system

**Key directories:**

- `custom_components/noaa_solar/` - Main integration code
- `config/` - Home Assistant configuration for local testing
- `scripts/` - Development scripts available in this repository

**Context-specific instructions:**

If you're using GitHub Copilot, path-specific instructions in `.github/instructions/*.instructions.md` provide additional guidance for specific file types (Python, YAML, JSON, etc.). This document serves as the primary reference for all agents.

## Local Development

Always prefer the repository scripts when available.

**Available scripts in this repo:**

- `scripts/setup` - Install dependencies and initialize local data directories
- `scripts/develop` - Start Home Assistant with this integration
- `scripts/lint` - Run Ruff linting with `--fix`

**Start Home Assistant:**

```bash
./scripts/develop
```

**Force restart (when HA is unresponsive or port conflicts):**

```bash
pkill -f "hass --config" || true && pkill -f "debugpy.*5678" || true && ./scripts/develop
```

- Kills any existing instance (hass + debugpy on port 5678) and starts fresh
- Avoids state confusion and port conflicts

**When to restart HA:** After modifying Python files, `manifest.json`, `services.yaml`, translations, or config flow changes.

**Reading logs:**

- Live: terminal where `./scripts/develop` runs
- File: `config/home-assistant.log` (most recent), `config/home-assistant.log.1` (previous)

**Adjusting log levels:**

- Integration logs: `custom_components.noaa_solar: debug` in `config/configuration.yaml`

## Architecture

**Data Flow:** Entities -> Coordinator -> API Client (never skip layers)

**Current flat module structure:**

- `custom_components/noaa_solar/api.py` - API client (`NOAASpaceApi`)
- `custom_components/noaa_solar/coordinator.py` - All coordinator classes (`NOAASolarUpdateCoordinator` and subclasses)
- `custom_components/noaa_solar/config_flow.py` - Config flow handler (`NOAASolarConfigFlowHandler`)
- `custom_components/noaa_solar/entity.py` - Base entity class (`NOAASolarEntity`)
- `custom_components/noaa_solar/sensor.py` - Sensor entities
- `custom_components/noaa_solar/image.py` - Image entities
- `custom_components/noaa_solar/data.py` - Runtime data types
- `custom_components/noaa_solar/const.py` - Constants
- `custom_components/noaa_solar/utils/` - Shared helper utilities

**Naming conventions:**

- Domain: `noaa_solar`
- Title: `NOAA Solar`
- Class prefix: `NOAASolar`

**Key patterns:**

- Entity MRO: `(PlatformEntity, NOAASolarEntity)` — order matters
- Unique IDs: `{entry_id}_{suffix}` (set per entity)
- Services: register in `async_setup()`, NOT `async_setup_entry()` (Quality Scale requirement)
- Config entry runtime data: `entry.runtime_data`

## Working With Developers

**For workflow basics (small changes, translations, tests, session management):** See `.github/copilot-instructions.md` for quick-reference guidance.

### When Instructions Conflict With Requests

If a developer requests something that contradicts these instructions:

1. **Clarify the intent** - Ask if they want you to deviate from the documented guidelines
2. **Confirm understanding** - Restate what you understood to avoid misinterpretation
3. **Suggest instruction updates** - If this represents a permanent change in approach, offer to update these instructions
4. **Proceed once confirmed** - Follow the developer's explicit direction after clarification

### Maintaining These Instructions

Instructions should evolve as the project matures:

- Refine guidelines based on actual project needs
- Remove outdated rules that no longer apply
- Consolidate redundant sections to prevent bloat
- Keep files focused

**Propose updates when:**

- You notice repeated deviations from documented patterns
- Instructions become outdated or contradict actual code
- New patterns emerge that should be standardized

### Documentation vs. Instructions

**Three types of content with clear separation:**

1. **Agent Instructions** - How AI should write code (`.github/instructions/`, `AGENTS.md`)
2. **Developer Documentation** - Architecture and design decisions (`docs/development/`)
3. **User Documentation** - End-user guides (`docs/user/`)

**AI Planning:** Use `.ai-scratch/` for temporary notes (never committed)

**Rules:**

- NEVER create random markdown files in code directories
- NEVER create documentation in `.github/` unless it's a GitHub-specified file
- ALWAYS ask first before creating permanent documentation
- Prefer module docstrings over separate markdown files

### Session and Context Management

**Commit suggestions:**

When a task completes and the developer moves to a new topic, suggest committing changes. Offer a commit message based on the work done.

**Commit rules (CRITICAL):**

- **Never commit automatically** - only commit when the developer explicitly requests it
- A previous commit request is NOT a standing permission; each commit requires a fresh explicit instruction
- **Never ask about pushing** - the developer always handles `git push` themselves; do not offer or suggest it

**Commit message format:** Follow [Conventional Commits](https://www.conventionalcommits.org/) - see `.github/instructions/noaa_solar.commit-message.instructions.md` for full conventions, types, scopes, and examples.

## Custom Integration Flexibility

**This is a CUSTOM integration, not a Home Assistant Core integration.** While we follow Core patterns for quality and maintainability, we have more flexibility in implementation decisions:

**Third-party libraries (PyPI):**

- Prefer existing PyPI libraries when maintained and fit the use case
- Build custom API client when:
  - Device/service uses simple REST API (HTTP, JSON)
  - Available libraries are unmaintained, bloated, or poorly designed
  - Using `aiohttp` + `json` is more maintainable than a framework

**Decision process:**

1. Research available libraries (PyPI, GitHub)
2. Evaluate: Maintained? Async? Well-documented? Dependency footprint?
3. Consider protocol: Simple REST -> aiohttp; Complex OAuth2 -> library; Standard (MQTT) -> industry library

**Quality Scale expectations:**

As an AI agent, **aim for Silver or Gold Quality Scale** when generating code:

- Always implement: Type hints, async patterns, proper error handling, service registration in `async_setup()`, diagnostics with `async_redact_data()`, device info
- When applicable: Config flow with validation, reauth flow, repair flows
- Can defer: Multiple config entries, advanced discovery, extensive test coverage

**Developer expectation:** Generate production-ready code. Implement HA standards with reasonable effort.

## Code Style and Quality

**Python:** 4 spaces, 120 char lines, double quotes, full type hints, async for all I/O

**YAML:** 2 spaces, modern HA syntax (no legacy `platform:` style)

**JSON:** 2 spaces, no trailing commas, no comments

**Validation:** Run `scripts/lint` before committing (Ruff format + lint with auto-fix).

**For comprehensive standards, see:**

- `.github/instructions/noaa_solar.python.instructions.md` - Python patterns, imports, type hints
- `.github/instructions/noaa_solar.yaml.instructions.md` - YAML structure and HA-specific patterns
- `.github/instructions/noaa_solar.json.instructions.md` - JSON formatting and schema validation
- `.github/instructions/noaa_solar.shell.instructions.md` - Shell script style and shellcheck

**GitHub Copilot users:** These instruction files are automatically provided based on file type.

## Project-Specific Rules

### Integration Identifiers

This integration uses the following identifiers consistently:

- **Domain:** `noaa_solar`
- **Title:** NOAA Solar
- **Class prefix:** `NOAASolar`

**When creating new files:**

- Use the domain `noaa_solar` for all DOMAIN references
- Prefix all integration-specific classes with `NOAASolar`
- Use "NOAA Solar" as the display title
- Never hardcode different values

### Integration Structure

**Current flat structure - do NOT restructure into subpackages without explicit approval:**

- `api.py` - API client
- `coordinator.py` - All coordinator classes
- `config_flow.py` - Config flow handler
- `entity.py` - Base entity class
- `sensor.py` - All sensor entities
- `image.py` - All image entities
- `data.py` - Runtime data types
- `const.py` - Constants
- `utils/` - Shared helper utilities

**If adding a new platform:** prefer a flat module (e.g., `switch.py`) unless complexity clearly requires a package. Register the new platform in `manifest.json`.

**Do NOT create:**

- `helpers/`, `ha_helpers/`, `common/`, `shared/`, `lib/` - use `utils/` instead
- New top-level packages without explicit approval

**Key patterns:**

- Entities read `coordinator.data` only - never call API directly
- Use `EntityDescription` dataclasses for static entity metadata
- Keep files focused (200-400 lines); split large modules when needed

**For detailed patterns, see:**

- `.github/instructions/noaa_solar.entities.instructions.md` - Entity platform patterns
- `.github/instructions/noaa_solar.coordinator.instructions.md` - Coordinator implementation
- `.github/instructions/noaa_solar.api.instructions.md` - API client patterns

### Device Info

All entities provide consistent device info via `NOAASolarEntity`. The base class configures device info from entry data - understand it before overriding.

### Integration Manifest

Current `manifest.json` key settings:

- `integration_type: hub` - aggregates multiple NOAA data sources
- `iot_class: cloud_polling` - fetches from NOAA web services
- `config_flow: true`

See `.github/instructions/noaa_solar.manifest.instructions.md` for comprehensive manifest documentation.

## Home Assistant Patterns

**Config flow:**

- Implemented in `custom_components/noaa_solar/config_flow.py`
- Support user setup, reauth, reconfigure as needed
- Always set unique_id for discovered entries

See `.github/instructions/noaa_solar.config_flow.instructions.md` for comprehensive patterns.

**Service actions (if added):**

- Define in `services.yaml` with full descriptions
- Implement handlers in `__init__.py` or a dedicated module
- **Register in `async_setup()`** - NOT in `async_setup_entry()` (Quality Scale!)
- Format: `noaa_solar.<action_name>`

See `.github/instructions/noaa_solar.service_actions.instructions.md` for service patterns.

**Coordinator:**

- Entities -> Coordinator -> API Client (never skip layers)
- Raise `ConfigEntryAuthFailed` (triggers reauth) or `UpdateFailed` (retry)
- Use `async_config_entry_first_refresh()` for first update

See `.github/instructions/noaa_solar.coordinator.instructions.md` and `.github/instructions/noaa_solar.api.instructions.md` for details.

**Entities:**

- Inherit from platform base + `NOAASolarEntity` (order matters for MRO)
- Read from `coordinator.data`, never call API directly
- Use `EntityDescription` for static metadata

See `.github/instructions/noaa_solar.entities.instructions.md` for entity patterns.

**Repairs:**

- Create `repairs.py` in integration root when needed (Gold Quality Scale)
- Use `async_create_issue()` with severity levels (WARNING, ERROR, CRITICAL)
- Implement `RepairsFlow` for guided user fixes
- Delete issues after successful repair

See `.github/instructions/noaa_solar.repairs.instructions.md` for comprehensive patterns.

**Entity availability:**

- Set `_attr_available = False` when device/data is unreachable
- Update availability based on coordinator success/failure
- Don't raise exceptions from `@property` methods

**State updates:**

- Use `self.async_write_ha_state()` for immediate updates
- Let coordinator handle periodic updates
- Minimize API calls (batch requests when possible)

**Setup failure handling:**

- `ConfigEntryNotReady` - Device offline/timeout, auto-retry, don't log manually (HA logs at debug)
- `ConfigEntryAuthFailed` - Expired credentials, triggers reauth flow, alternative: `entry.async_start_reauth()`

**Diagnostics:**

- **CRITICAL:** Use `async_redact_data()` from `homeassistant.helpers.redact` to remove sensitive data
- Redact: API keys, tokens, location data, personal information

See `.github/instructions/noaa_solar.diagnostics.instructions.md` for comprehensive patterns.

## Workflow Expectations

### General

1. **Small, focused changes** - avoid large refactorings unless explicitly requested
2. **Implement features completely** - even if spanning 5-8 files
   - Example: New sensor needs entity class + coordinator data key + translations -> implement all together
   - Example: Bug fix requiring changes in coordinator + entity + error handling -> do all at once
3. **Multiple independent features:** implement one at a time, suggest commit between each
4. **Large refactoring (architectural changes):** propose a plan first, get explicit confirmation

**Important: Do NOT write tests unless explicitly requested.** Focus on implementing functionality. The developer decides when and if tests are needed.

### Translation Strategy

- Business logic first, translations later
- Update `en.json` only when asked or at major feature completion
- NEVER update other language files automatically - extremely time-consuming
- Ask before updating multiple translation files
- Use translation keys in code (e.g., `translation_key="my_sensor"`) - functionality works without translations

## Research and Validation

**When uncertain, consult official documentation:**

- **Always check current patterns** in [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- **Read the blog** at [Home Assistant Developer Blog](https://developers.home-assistant.io/blog/) for recent changes and best practices
- **Search for examples** using Google: `site:developers.home-assistant.io [your topic]`
- **Verify with tools** before assuming - run `scripts/lint` to catch issues early

**Don't rely on assumptions:**

- Home Assistant APIs and patterns evolve frequently
- What worked in older versions may be deprecated
- Use official docs and working examples over guesswork
- When in doubt, search for recent integration examples in Home Assistant Core

**Context gathering strategy:**

1. **First pass** - semantic_search to find relevant areas (1-2 queries)
2. **Second pass** - Read the 3-5 most relevant files identified
3. **Evaluate** - Do you have enough context to proceed? If yes, start implementation
4. **Third pass (if needed)** - Read 2-3 additional specific files for missing details
5. **Decision point** - After ~10 file reads total, either proceed or ask specific questions; never continue searching indefinitely

**Error recovery strategy:**

1. **First attempt** - Fix the specific error reported by the tool
2. **Second attempt** - If it fails again, reconsider your approach (maybe your understanding was wrong)
3. **Third attempt** - If still failing, ask for clarification rather than looping indefinitely

## Breaking Changes

**Always warn the developer before making changes that:**

- Change entity IDs or unique IDs (users' automations will break)
- Modify config entry data structure (existing installations will fail)
- Change state values or attributes format (dashboards and automations affected)
- Alter service call signatures (user scripts will break)
- Remove or rename config options (users must reconfigure)

**Never do without explicit approval:**

- Removing config options (even if "unused")
- Changing service parameters or return values
- Modifying how data is stored in config entries
- Renaming entities or changing their device classes
- Changing unique_id generation logic

**How to warn:**

> "This change will modify the entity ID format from `sensor.device_name` to `sensor.device_name_sensor`. Existing users' automations and dashboards will break. Should I proceed, or would you prefer a migration path?"

**When breaking changes are necessary:**

- Document the breaking change in commit message (`BREAKING CHANGE:` footer)
- Consider providing migration instructions
- Suggest version bump (major version change)

## File Changes

**Single logical feature or fix:**

- Implement completely even if it spans 5-8 files
- Example: New sensor needs entity class + coordinator data key + translations -> implement all together
- Example: Bug fix requires changes in coordinator + entity + error handling -> do all at once

**Multiple independent features:**

- Implement one at a time
- After completing each feature, suggest committing before proceeding to the next

**Large refactoring (>10 files or architectural changes):**

- Propose a plan first before starting implementation
- Get explicit confirmation from developer

## Tool Parallelization

**Safe to call in parallel:**

- Multiple `read_file` operations (different files or different sections of same file)
- `file_search` + `read_file` + `grep_search` (independent read-only operations)
- `semantic_search` followed by parallel `read_file` of results (but only 1 semantic_search at a time)

**Never call in parallel:**

- Multiple `run_in_terminal` commands (execute sequentially, wait for output)
- Multiple `replace_string_in_file` on the same file (use `multi_replace_string_in_file` instead)
- `semantic_search` with other `semantic_search` (execute one at a time)

**Best practices:**

- Batch independent read operations together in one parallel call
- After gathering context in parallel, provide a brief progress update before proceeding
- For file edits, use `multi_replace_string_in_file` when making multiple changes to the same file
- Terminal commands must always be sequential - wait for output before running the next command

## Instruction Files

Path-specific guidance lives in `.github/instructions/noaa_solar.*.instructions.md`.

- Keep instruction references aligned with actual repository file structure.
- If repository structure evolves (e.g., moving from flat modules to packages), update these instructions accordingly.
- When modifying or creating files, load the relevant instruction file for that file type.

## Additional Resources

- [Home Assistant Developer Docs](https://developers.home-assistant.io/) - Primary reference
- [Integration Quality Scale](https://developers.home-assistant.io/docs/integration_quality_scale_index)
- [Architecture Docs](https://developers.home-assistant.io/docs/architecture_index)
- [Ruff Rules](https://docs.astral.sh/ruff/rules/) - Linter documentation
- See `CONTRIBUTING.md` for contribution guidelines
