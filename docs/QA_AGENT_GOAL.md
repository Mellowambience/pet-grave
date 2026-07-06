# Pet Grave — Browser QA + Stabilization Goal

> Run the game in a real browser, perform a full QA pass, then patch the smallest set of issues needed to make Pet Grave stable, playable, and ready to embed later as an Aether Haven arcade cartridge.

## Context

Pet Grave is currently a single-file HTML5 Canvas 2D game in `index.html`. It has strong prototype systems: isometric movement, pet bonding, ghost guardians, biomes, village upgrades, combat, talents, codex, procedural audio, save/export/import, and atmospheric canvas rendering.

Do **not** rewrite the game into PixiJS yet. The first goal is to stabilize the existing Canvas version.

## First task: run it

1. Clone the repo.
2. Start a local static server from the repo root.
3. Open the game in Chrome.
4. Open DevTools console.
5. Play for at least 20 minutes.
6. Record every console error, missing asset, input bug, soft-lock, UI issue, performance drop, and confusing moment.

Suggested commands:

```bash
# from repo root
python -m http.server 5173
# open http://localhost:5173
```

If Python is unavailable, use any static server. Do not rely only on opening the file directly if asset loading behaves differently.

## QA checklist

### Boot / loading

- The page loads without JavaScript errors.
- Canvas fills the viewport.
- HUD appears.
- Menu appears and buttons work.
- Art assets load from `Content/Art/Generated/GlowGarden_v2`.
- Missing assets fall back gracefully.
- Audio starts only after user interaction.

### Input

- WASD movement works.
- Click-to-move works.
- E interaction works for bonding/tending/talking.
- Q limit break works when available.
- R memorial/recall works.
- Tab ledger opens and closes.
- Escape closes overlays where appropriate.
- Mouse/touch does not get stuck.

### Core loop

- Player can start a run.
- First lost pet can be found.
- Bonding works.
- Pets join active pack or village reserve correctly.
- Combat starts and ends correctly.
- Player can take damage and recover.
- Pet ghost guardian mechanic triggers correctly.
- Game over and respawn work.
- Loot can be collected.
- XP, level, talents, glowdust, focus, and limit update.

### UI overlays

- Hub tabs render: Team, Village, Skills, Codex, Talents, Bag, Journal.
- Cards do not overflow badly on small screens.
- Tooltips/toasts do not block important controls.
- Save export/import panel works.
- Credits and victory/game-over overlays close correctly.

### Save / persistence

- Progress saves after bonding, leveling, moving pets, changing village state, collecting loot, and respawning.
- Refresh restores expected state.
- Export creates valid save text.
- Import restores valid save text.
- Invalid import fails safely.

### Performance

- Play 10+ minutes without runaway slowdown.
- Particle counts do not grow forever.
- Enemies, loot, spell VFX, battle VFX, toasts, markers, and zaps clean up correctly.
- Low-FX mode, if present, improves performance.
- Canvas DPR scaling does not destroy FPS on high-DPI displays.

### Mobile / responsive

- Page fits mobile viewport.
- HUD remains readable.
- Touch click-to-move works or fails gracefully.
- Overlays remain scrollable.
- No critical controls require unavailable keyboard input without alternatives.

## Patches to prioritize

Patch only confirmed issues. Prefer small, safe changes.

High priority:

1. Fix boot-breaking JS errors.
2. Fix missing/incorrect asset paths.
3. Fix save/load/export/import bugs.
4. Fix input soft-locks.
5. Fix overlay close issues.
6. Fix runaway arrays / memory leaks.
7. Replace unsafe `innerHTML` paths where user-controlled content could ever enter.
8. Add clear on-screen controls for first-time players.
9. Add a visible version string and QA notes.

Medium priority:

1. Improve mobile fallback controls.
2. Add pause/resume behavior when tab loses focus.
3. Add low-FX toggle if not working.
4. Add a debug toggle for FPS/entity counts.
5. Improve onboarding copy: what is my goal, how do I bond, what happens at night?

Do not prioritize:

- PixiJS migration.
- TypeScript conversion.
- Full module refactor.
- Multiplayer.
- AI companion chat.
- Payments.
- Crypto.
- Asset overhauls.

## Suggested small code improvements

Only implement after the browser QA confirms the game boots.

### Safer toast rendering

Audit `toast(html, deadly)` and similar UI code. If any user-controlled data can reach `innerHTML`, replace with DOM node creation or sanitize aggressively. Keep intentional simple formatting only if all inputs are trusted constants.

### Entity cleanup audit

Check these arrays over time:

- `particles`
- `markers`
- `loot`
- `enemies`
- `shots`
- `pshots`
- `spellVfx`
- `bfx`
- `toasts`
- `zaps`

Ensure each has lifecycle cleanup.

### QA debug overlay

Add a hidden debug overlay toggled by backtick or F3:

```txt
FPS
particles
critters
enemies
loot
spellVfx
save status
biome
phase
```

This helps future QA without changing the normal player experience.

## Relationship to Aether Haven

Pet Grave should remain its own game for now. Later, it can become:

**Aether Haven Arcade Cartridge #1: Pet Grave — Memorial Garden**

Keep its emotional mechanics as design DNA for Aether Haven:

- bonding instead of capturing;
- pets changing a village/realm;
- friendship stages;
- ghost guardians;
- memorial fire;
- cozy-dangerous biomes;
- journal/memory systems.

Do not force it into the main Aether Haven codebase until it is stable.

## Final report format

After QA and patches, write:

```md
# Pet Grave QA Report

## Browser/environment tested

## Time played

## What works

## Critical bugs fixed

## Remaining bugs

## Performance notes

## Mobile notes

## Files changed

## How to run

## Suggested next pass

## Aether Haven reuse notes
```

## Acceptance criteria

This pass is complete when:

- the game boots from a local static server;
- no boot-breaking console errors remain;
- movement, bonding, combat, save, respawn, and hub overlays work;
- the game can be played for at least 20 minutes without severe slowdown;
- any committed fixes are small and documented;
- a QA report is included in the repo.
