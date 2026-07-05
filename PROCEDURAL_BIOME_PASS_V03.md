# Pet Grave v0.3 — Procedural Biome + Visual Hierarchy Pass

## What this pass fixes

This pass directly addresses the issue that the live/playtested art still felt like the old build:

- The painted/background-heavy presentation is removed from the prototype runtime.
- The playfield is now generated procedurally from a world seed.
- The background is intentionally quiet: dark gradient, dim stars, faint silhouettes, and a soft moon glow only.
- The visual storytelling now lives in the generated map layer instead of a distracting backdrop image.

## Procedural generation added

The world now generates from a deterministic seed. Same seed means the same:

- biome layout
- tile variation
- sanctuary position
- landmark clearings
- connecting paths
- prop scatter
- pet encounter positions
- fog pockets

Biomes currently included:

- Memorial Garden
- Willow Marsh
- Lantern Grove
- Moon Meadow
- Stone Orchard
- Mist Hollow

Generation passes:

1. Build seeded noise fields for moisture, gloom, bloom, and stone density.
2. Assign a biome to each tile.
3. Place the sanctuary clearing at the center.
4. Place four landmark/pet clearings around the map.
5. Connect clearings with readable memorial paths.
6. Scatter biome-specific props by weighted rules.
7. Add fog patches and ambience.
8. Spawn pets in encounter clearings.

## Visual hierarchy changes

The game now prioritizes:

1. Player and pet readability.
2. Active objective beacon.
3. Sanctuary and paths.
4. Biome props and landmarks.
5. Background atmosphere.

The new runtime avoids the old problem where the background painting competed with the actual game board.

## Player-facing changes

- New title: `Pet Grave v0.3 — Procedural Biomes`.
- Seed input on the start menu.
- Random seed and daily seed options.
- Press `N` to generate a new world.
- Biome banner appears when entering a new biome.
- Journal shows seed, biome coverage, rescued pets, low-FX status, debug status, and prop count.
- Objective text names the pet and biome.
- Beacon line points from the player to the next lost pet.

## QA notes

- Updated `index.html` on branch `visual-consistency-pass-v02`.
- This updates draft PR #3 rather than opening a separate branch, so the existing PR now contains the stronger v0.3 procedural pass.
- Needs browser smoke test through branch checkout or a GitHub Pages preview before merge.

## Next improvements

1. Add per-biome ambient sound and music mood.
2. Add biome-specific pet behavior/event tables.
3. Reintroduce bonding minigames only after visual readability is accepted.
4. Add collision/blocked tiles around dense props.
5. Add screenshot QA at 1365x768, 1024x768, and mobile widths.
