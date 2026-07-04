# Pet Grave Visual Refresh Notes

## Status

Memorial Garden v1 art pack generated locally.

The title/menu background is wired into `index.html` and verified in the browser. Milo and Pip are now sliced from the Memorial Garden creature atlas and wired as the first production creature candidates. The remaining creature and prop atlases are saved as source candidates, but are not yet sliced into production assets.

Animation is now a production rule: every in-game visual should have authored animation or a lightweight procedural motion fallback before it is considered finished.

## New Art Pack

Path:

`Content/Art/Generated/MemorialGarden_v1`

Files:

- `Concepts/PetGrave_MemorialGarden_KeyArt_v1.png`
- `Menu/PetGrave_MenuBackdrop_MemorialGarden_v1.png`
- `Creatures/milo.png`
- `Creatures/pip.png`
- `Atlases/PetGrave_CreatureAtlas_MemorialGarden_v1.png`
- `Atlases/PetGrave_PropsTerrainAtlas_MemorialGarden_v1.png`
- `ART_PACK_MANIFEST.md`

## What Changed In Game

- The title/menu background now uses:

`Content/Art/Generated/MemorialGarden_v1/Menu/PetGrave_MenuBackdrop_MemorialGarden_v1.png`
- The title/menu now has ambient animated motes, garden glow, and soft breathing light.
- Primary menu and mobile action controls now have responsive motion states.
- Non-essential CSS animation respects reduced-motion preferences.
- The title/menu overlay is fixed above the playfield so the animated backdrop is visible when the menu is open.
- Milo and Pip now use Memorial Garden cropped creature PNGs while the rest of the creature cast remains on the existing procedural renderer.

## Visual Direction

- Cozy-haunted memorial garden
- More emotional and less generic graveyard
- Amber lantern safety against deep plum night
- Pale mint spirit pets
- Moss, flowers, stone, bramble corruption at the edges
- Tender ARPG mood

## QA

Tested locally at:

`http://127.0.0.1:5173`

Passed:

- Game boots
- Menu opens
- New menu background loads
- Ambient menu animation is visible
- Mobile controls have animated press and primary-action states
- Mobile gameplay controls remain visible and usable after continuing a save
- No console errors or warnings
- No horizontal overflow on desktop QA viewport

## Animation Standard

Required for any imported production asset:

1. Creatures need at least idle, move, hurt, and cast or interact states. Static source art may ship only if the runtime adds bob, blink, glow, or squash motion.
2. Spirit pets need aura movement, tail/ear/wing secondary motion where applicable, and a clear active-state change.
3. Props need ambient loops when they imply energy or nature: lantern flicker, fire pulse, flower sway, water shimmer, mist drift, and corrupted bramble twitch.
4. UI needs responsive state motion: hover/focus/press/disabled, plus reduced-motion fallbacks.
5. Backgrounds need slow parallax, particles, light breathing, or shader-style movement so screenshots feel alive without hurting mobile performance.

## Next Visual Pass

1. Browser-test the Milo/Pip production slices on desktop and mobile.
2. Tune scale and anchors if either character reads too large, too small, or too detached from the ground shadow.
3. Pick the next small subset:
   - `lume`
   - `campfire`
   - `lantern_posts`
   - `flowers`
4. Remove chroma-key from that subset.
5. Slice approved items into individual PNGs.
6. Normalize scale and anchor points.
7. Create or simulate animation states for that subset before wiring them into the game.
8. Browser-test boot, menu, gameplay, mobile controls, animation smoothness, and missing asset fallbacks.
9. Only then decide whether to replace the full GlowGarden pack.

## Publish Status

Local only. Do not push to GitHub Pages until approved.
