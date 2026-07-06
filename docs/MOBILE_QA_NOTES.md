# Pet Grave Mobile QA Notes

## Browser/environment tested

- Local static server: `http://127.0.0.1:5173`
- Mobile viewport: 390 x 844
- Browser: Codex in-app browser

## What changed

- Added touch-friendly mobile controls.
- Added a left D-pad for movement.
- Added action buttons for interact, cast, dash, limit, hub, and home/recall.
- Added touch-to-move support on the canvas.
- Added touch support for battle timing taps.
- Updated visible control copy from click-only to tap-aware.
- Adjusted mobile HUD, hint, battle text, and controls spacing.

## What works

- Game boots locally with no console errors.
- Mobile controls appear on touch/coarse pointer screens.
- Start menu fits the mobile viewport.
- In-game HUD, hint, D-pad, and action buttons are visible.
- No horizontal overflow was detected in the tested mobile viewport.
- Begin flow works and enters gameplay.

## Remaining mobile follow-up

- Test on a real phone for thumb comfort and safe-area behavior.
- Tune D-pad/action button size if it feels crowded on smaller devices.
- Consider a collapsible controls toggle after a longer playtest.
- Consider a dedicated mobile onboarding card before the first run.

## Publish status

Local patch only. Do not push to GitHub Pages until approved.
