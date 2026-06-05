# GitHub Copilot Instructions

> **Comprehensive docs:** See [`AGENTS.md`](../AGENTS.md) at the repository root for full AI agent documentation.
>
> **Why two files?** This file is loaded automatically by GitHub Copilot. `AGENTS.md` serves non-Copilot agents (Claude Code, Cursor, etc.) who don't read this file. Some overlap is intentional. Path-specific `*.instructions.md` files provide detailed patterns per file type — avoid duplicating their content here.

## Project Identity

- **Domain:** `noaa_solar`
- **Title:** NOAA Solar
- **Class prefix:** `NOAASolar`
- **Main code:** `custom_components/noaa_solar/`
- **Validate:** `scripts/lint`
- **Start HA:** `./scripts/develop`
- **Setup deps:** `./scripts/setup`

Use these exact identifiers throughout the codebase. Never hardcode different values.

## Code Quality Baseline

- **Python:** 4 spaces, 120 char lines, double quotes, full type hints, async for all I/O
- **YAML:** 2 spaces, modern Home Assistant syntax (no legacy `platform:` style)
- **JSON:** 2 spaces, no trailing commas, no comments

Before considering any coding task complete:

```bash
scripts/lint      # Ruff format + lint with auto-fix
```

Generate code that passes these checks on first run.

## Current Architecture

**Data flow:** Entities -> Coordinator -> API Client (never skip layers)

**Current flat module structure (do NOT restructure without approval):**

- `api.py` - External API client (`NOAASpaceApi`, async aiohttp)
- `coordinator.py` - All data update coordinators (`NOAASolarUpdateCoordinator` and subclasses)
- `config_flow.py` - Config flow handler (`NOAASolarConfigFlowHandler`)
- `entity.py` - Base entity class (`NOAASolarEntity`)
- `sensor.py` - Sensor entities
- `image.py` - Image entities
- `utils/` - Integration-wide utilities

**Forbidden package names:** `helpers/`, `ha_helpers/`, `common/`, `shared/`, `lib/` — use `utils/` instead.

**Key patterns:**

- Entity MRO: `(PlatformEntity, NOAASolarEntity)` — order matters
- Unique IDs: `{entry_id}_{suffix}` per entity
- Services: register in `async_setup()`, NOT `async_setup_entry()`
- Config entry runtime data: `entry.runtime_data`

## Workflow Rules

1. **Small, focused changes** — avoid large refactorings unless explicitly requested
2. **Implement features completely** — even if spanning 5-8 files
   - Example: New sensor needs entity class + coordinator data + translations -> implement all together
   - Example: Bug fix touching coordinator + entity + error handling -> do all at once
3. **Multiple independent features:** implement one at a time, suggest commit between each
4. **Large refactoring:** propose plan first, get explicit confirmation
5. **Validation:** run `scripts/lint` before considering task complete

**Do NOT write tests unless explicitly requested.**

**Translation strategy:** Business logic first, translations later. Update `en.json` only when asked or at major feature completion. Never update other language files automatically.

## Research First

**Don't guess — look it up:**

1. Search [Home Assistant Developer Docs](https://developers.home-assistant.io/) for current patterns
2. Check the [developer blog](https://developers.home-assistant.io/blog/) for recent changes
3. Look at existing patterns in similar files in this integration
4. Run `scripts/lint` early and often — catch issues before they compound

**Home Assistant evolves rapidly** — verify current best practices rather than relying on outdated knowledge.

## Local Development

**Start Home Assistant:**

```bash
./scripts/develop
```

**Force restart (when HA is unresponsive or port conflicts):**

```bash
pkill -f "hass --config" || true && pkill -f "debugpy.*5678" || true && ./scripts/develop
```

**When to restart HA:** After modifying Python files, `manifest.json`, `services.yaml`, translations, or config flow changes.

**Logs:**

- Live: terminal where `./scripts/develop` runs
- File: `config/home-assistant.log` (most recent), `config/home-assistant.log.1` (previous)
- Debug level: `custom_components.noaa_solar: debug` in `config/configuration.yaml`

## Working With the Developer

**When requests conflict with these instructions:**

1. Clarify if deviation is intentional
2. Confirm you understood correctly
3. Suggest updating instructions if this is a permanent change
4. Proceed after confirmation

**Documentation rules:**

- NEVER create markdown files without explicit permission
- NEVER create "helpful" READMEs, GUIDE.md, NOTES.md, etc.
- NEVER create documentation in `.github/` unless it's a GitHub-specified file
- ALWAYS ask first before creating permanent documentation
- Prefer module/class/function docstrings over separate markdown files
- Use `.ai-scratch/` for temporary planning and notes (never committed)
- Developer docs go in `docs/development/` (ask first)
- User docs go in `docs/user/` (ask first)

**Session management:**

- When task completes and developer moves on: suggest commit with message
- Monitor context size — warn if getting large and a new topic starts
- Offer to create summary for fresh session if context is strained
- Suggest once, don't nag if declined

**Commit format:** [Conventional Commits](https://www.conventionalcommits.org/) — see `.github/instructions/noaa_solar.commit-message.instructions.md` for full conventions, types, scopes, and examples.

**Always check `git diff` first** — don't rely on session memory. Include all changes in your message.

**Commit rules (CRITICAL):**

- **Never commit automatically** — only commit when the developer explicitly requests it
- A previous commit request is NOT a standing permission; each commit requires a fresh explicit instruction
- **Never ask about pushing** — the developer always handles `git push` themselves; do not offer or suggest it

## Instructions Layout

Path-specific instruction files are in `.github/instructions/noaa_solar.*.instructions.md`.

When structure changes, update instruction files so their `applyTo` globs still match real files.
