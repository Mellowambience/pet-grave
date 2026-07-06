# 🕯️ Pet Grave

*Tend a moonlit graveyard for lost pet spirits — befriend them by day, defend them by night.*

**▶ Play in your browser:** https://mellowambience.github.io/pet-grave/

No install, no account. Works on desktop and mobile. Your progress saves locally in the browser (use **Export Save** in the menu to move it between devices).

## What is this?

Pet Grave is a cozy-haunted, single-file HTML5 canvas game. You are the gravekeeper of a small afterlife garden:

- **By day** — wander out, find lost pet spirits, and win their trust in gentle timing duels. Bonded pets fight beside you or live around your memorial fire.
- **By night** — corruption surges from the dark. Defend the sanctuary with your pack, spells, and lantern light.
- **Forever** — nothing you love resets. Fallen pets return as ghost guardians; the village, your friendships, and the forest you plant all persist.

Systems under the hood: bonding duels, a pet village with jobs and moods, talents and gear, a wandering merchant economy, memory trees with fast travel, a branching story, day/night surge director, procedural creature roster, fully procedural audio, and two additive modules (the Rift meta-layer and a 4.5D terrain pass).

## Controls

Press **❔ HOW TO PLAY** on the title screen for the full guide. The short version: **WASD**/tap to move, **E** to interact with whatever is nearest, **Tab** for your ledger, **Esc** for the menu. Touch controls appear automatically on mobile.

## Running locally

```bash
git clone https://github.com/Mellowambience/pet-grave.git
cd pet-grave
python3 -m http.server 5173
# open http://localhost:5173
```

Any static server works. The game is one `index.html`; art loads from `Content/`.

## Repository layout

| Path | What it is |
|---|---|
| `index.html` | The entire game — CSS, markup, and all JS (main game + Rift + 4.5D modules) |
| `Content/Art/Generated/GlowGarden_v2/` | Active runtime art pack (creatures, props, VFX, HD2D props) |
| `Content/Art/Generated/MemorialGarden_v1/` | Next-gen art pack: menu backdrop is live; atlases/layer system are source material for future slicing |
| `docs/` | QA goals, visual-refresh and mobile QA notes |
| `tools/` | Python creature-layer generator |
| `VISION.md` | Icebox for future ideas — one line each, reviewed between releases |

## v0.2 changelog

- Added `<meta viewport>` — mobile devices now render at device width (touch controls were previously defeated by desktop-width scaling on real phones)
- Fixed night-surge NPC panic loop that spammed "surge! to camp!" speech bubbles every other frame (~90/sec) during surges
- New **HOW TO PLAY** overlay — every control is now discoverable (Space/right-click cast, Shift dash, C command wheel, F look filter, T/G/R, 5 terrain); title-screen key wall replaced with a four-key summary
- Mobile parity: new 🌳 TREE and 🗺 PATH buttons — touch players can now plant memory trees and use lantern fast-travel
- `G` (lantern paths) no longer opens on top of other open panels
- Removed 85 unused art files (−11 MB); moved working notes into `docs/`
- Emoji favicon, page description, theme color

*Built with canvas, web audio, and a great deal of care.*
