# Pet Grave v0.2 — Visual Consistency Pass

## What changed

This branch replaces the messy mixed visual state with a focused single-file browser build centered on one coherent art direction:

- Unified cozy-haunted palette: deep plum night, mint spirits, amber lantern safety, rose accents, and soft lavender UI.
- Fully procedural canvas art so the menu, world tiles, trees, graves, flowers, pets, player wisp, lanterns, particles, and prompts all share the same style.
- Readable player avatar: the keeper is now a golden wisp with a constant glow, face, halo ring, shadow, and bobbing idle motion.
- Consistent pet visuals: Pip, Lume, and Capkin use the same ghost-body language with matching bob, breathe, aura, ring, and rescue-state effects.
- Animation standard applied in-game: lantern flicker, tree bob, flower sway, pet breathing, player glow, target beacon pulse, movement target ring, mist drift, spark particles, rescue ripple.
- Cleaner HUD: heart, trust, glow, objective, rescued pets, lanterns, and save status only.
- First-rescue onboarding: tutorial card, objective text, prompt text, target beacon line, and highlighted pet ring.
- Safer text rendering for toasts and most UI; user-entered save text is parsed, not injected.
- Save/export/import tools moved into a journal overlay.
- Low-FX toggle and debug toggle for performance checks.
- Mobile controls retained with D-pad and action buttons.

## Why this approach

The old build had strong ideas but visual inconsistency between imported art, procedural sprites, dense HUD panels, tiny character readability, and unclear first action. This pass prioritizes a playable, stable, coherent vertical slice before adding more systems back.

## QA performed

- Parsed the script with Node via `new Function(script)` to catch syntax errors.
- Verified the generated file size and single-file structure.
- Attempted headless browser screenshot QA, but local browser navigation was blocked in the container environment by administrator policy. This needs a final GitHub Pages/browser smoke test after the PR is available.

## Recommended next pass

1. Smoke test the PR build in a real browser through GitHub Pages or local static server.
2. Decide whether to keep this as the new main prototype or preserve the old complex systems behind a legacy file.
3. Add a small combat or day/night loop back only after movement, bonding, saving, and visuals feel good.
4. If using production PNG art again, slice only one asset family at a time and match the procedural scale, shadow, anchor, and animation rules from this build.
