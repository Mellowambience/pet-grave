#!/usr/bin/env python3
"""
Pet Grave creature layer generator.

This adapts the useful HashLips ideas for Pet Grave without the NFT framing:
ordered layers, weighted traits, deterministic DNA, metadata, and animation
strips. The renderer is anatomy-first: every trait attaches to a named body
part and every animation state moves joints inside conservative constraints.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw


CANVAS = (320, 360)
BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = BASE_DIR / "Content/Art/Generated/MemorialGarden_v1/LayerSystem/pet-grave-creature-layers.json"
DEFAULT_OUT = BASE_DIR / "Content/Art/Generated/MemorialGarden_v1/LayerSystem/build"


@dataclass(frozen=True)
class Trait:
    name: str
    weight: int
    data: dict[str, Any]


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def weighted_choice(rng: random.Random, traits: list[Trait]) -> Trait:
    total = sum(max(0, t.weight) for t in traits)
    if total <= 0:
        raise ValueError("Trait weights must sum above zero")
    pick = rng.randrange(total)
    for trait in traits:
        pick -= max(0, trait.weight)
        if pick < 0:
            return trait
    return traits[-1]


def build_traits(config: dict[str, Any], rng: random.Random) -> dict[str, Trait]:
    selected: dict[str, Trait] = {}
    for layer in config["layers"]:
        traits = [
            Trait(t["name"], int(t.get("weight", 1)), t)
            for t in layer["traits"]
        ]
        selected[layer["id"]] = weighted_choice(rng, traits)
    return selected


def trait_dna(species_id: str, seed: str, selected: dict[str, Trait]) -> str:
    raw = {
        "species": species_id,
        "seed": seed,
        "traits": {layer: trait.name for layer, trait in selected.items()},
    }
    return hashlib.sha1(json.dumps(raw, sort_keys=True).encode("utf-8")).hexdigest()


def hex_to_rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = value.strip().lstrip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), alpha)


def add(p: tuple[float, float], dx: float, dy: float) -> tuple[float, float]:
    return (p[0] + dx, p[1] + dy)


def ellipse(draw: ImageDraw.ImageDraw, center: tuple[float, float], rx: float, ry: float, fill: str, outline: str | None = None, width: int = 1) -> None:
    x, y = center
    draw.ellipse((x - rx, y - ry, x + rx, y + ry), fill=fill, outline=outline, width=width)


def polygon(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], fill: str, outline: str | None = None) -> None:
    draw.polygon(points, fill=fill, outline=outline)


def rig_pose(state: str, frame: int, frames: int) -> dict[str, float]:
    phase = frame / max(1, frames)
    wave = math.sin(phase * math.tau)
    trot = math.sin(phase * math.tau * 2)
    if state == "walk":
        return {
            "body_y": wave * 3.0,
            "head_y": wave * 2.0 - 1.0,
            "tail_a": wave * 8.0,
            "fore_a": trot * 6.0,
            "hind_a": -trot * 6.0,
            "ear_a": wave * 2.0,
            "squash": 1.0 + abs(wave) * 0.015,
        }
    if state == "interact":
        reach = math.sin(min(1.0, phase) * math.pi)
        return {
            "body_y": -reach * 5.0,
            "head_y": -reach * 8.0,
            "tail_a": reach * 12.0,
            "fore_a": -reach * 14.0,
            "hind_a": reach * 5.0,
            "ear_a": -reach * 4.0,
            "squash": 1.0 + reach * 0.025,
        }
    if state == "hurt":
        recoil = math.sin(min(1.0, phase) * math.pi)
        return {
            "body_y": recoil * 3.0,
            "head_y": recoil * 4.0,
            "tail_a": -recoil * 18.0,
            "fore_a": recoil * 8.0,
            "hind_a": recoil * 8.0,
            "ear_a": recoil * 12.0,
            "squash": 1.0 - recoil * 0.035,
        }
    return {
        "body_y": wave * 1.5,
        "head_y": wave * 1.1,
        "tail_a": wave * 6.0,
        "fore_a": wave * 2.0,
        "hind_a": -wave * 1.5,
        "ear_a": wave * 1.2,
        "squash": 1.0 + wave * 0.01,
    }


def rotate(point: tuple[float, float], origin: tuple[float, float], degrees: float) -> tuple[float, float]:
    radians = math.radians(degrees)
    px, py = point
    ox, oy = origin
    qx = ox + math.cos(radians) * (px - ox) - math.sin(radians) * (py - oy)
    qy = oy + math.sin(radians) * (px - ox) + math.cos(radians) * (py - oy)
    return (qx, qy)


def draw_creature(config: dict[str, Any], selected: dict[str, Trait], state: str, frame: int, frames: int) -> Image.Image:
    img = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    pose = rig_pose(state, frame, frames)

    palette = selected["palette"].data
    body_trait = selected["body"].data
    ear_trait = selected["ears"].data
    tail_trait = selected["tail"].data
    charm_trait = selected["charm"].data
    aura_trait = selected["aura"].data

    base = palette["base"]
    shade = palette["shade"]
    accent = palette["accent"]
    core = palette["core"]
    outline = "#4b332b"

    body = (160, 228 + pose["body_y"])
    head = (150, 166 + pose["head_y"])
    neck = (145, 196 + pose["body_y"] * 0.7)
    hind_leg_l = (122, 270 + pose["body_y"])
    hind_leg_r = (180, 270 + pose["body_y"])
    fore_leg_l = (132, 264 + pose["body_y"])
    fore_leg_r = (170, 264 + pose["body_y"])

    # Ground contact comes first so every limb reads attached to the same plane.
    ellipse(draw, (160, 306), 76, 20, "rgba(14,8,22,70)")

    if aura_trait["shape"] != "none":
        pulse = 0.6 + 0.4 * math.sin((frame / max(1, frames)) * math.tau)
        aura_alpha = int(45 + 35 * pulse)
        ellipse(draw, (160, 222), 110, 92, hex_to_rgba(core, aura_alpha))

    # Tail attaches behind the pelvis, then legs/body/head stack forward.
    tail_root = (205, 232 + pose["body_y"])
    tail_tip = rotate((250, 174 + pose["body_y"]), tail_root, pose["tail_a"])
    if tail_trait["shape"] == "plume":
        ellipse(draw, tail_tip, 32, 58, shade, outline, 3)
        ellipse(draw, add(tail_tip, -9, -9), 20, 36, base, None)
    elif tail_trait["shape"] == "wisp":
        polygon(draw, [tail_root, tail_tip, add(tail_tip, -22, 40), add(tail_root, -6, 18)], shade, outline)
        ellipse(draw, tail_tip, 20, 28, core, None)
    else:
        ellipse(draw, tail_tip, 24, 28, shade, outline, 3)

    for center, angle in [(hind_leg_l, pose["hind_a"]), (hind_leg_r, -pose["hind_a"])]:
        foot = rotate(add(center, 0, 30), center, angle)
        ellipse(draw, add(foot, 0, 8), 17, 10, shade, outline, 2)
        ellipse(draw, center, 14, 36, base, outline, 2)

    ellipse(draw, body, 78 * pose["squash"], 62 / pose["squash"], base, outline, 3)
    ellipse(draw, add(body, -20, 6), 52, 44, shade, None)
    ellipse(draw, neck, 38, 38, base, outline, 2)

    if body_trait.get("marking") == "moss-mantle":
        for i in range(8):
            x = 92 + i * 17
            y = 204 + math.sin(i) * 8 + pose["body_y"]
            polygon(draw, [(x, y), (x + 18, y + 8), (x + 8, y + 28), (x - 8, y + 14)], accent, "#557343")
    elif body_trait.get("marking") == "moon-socks":
        for center in [hind_leg_l, hind_leg_r, fore_leg_l, fore_leg_r]:
            ellipse(draw, add(center, 0, 32), 15, 11, "#fff3d0", None)

    for center, angle in [(fore_leg_l, pose["fore_a"]), (fore_leg_r, -pose["fore_a"])]:
        paw = rotate(add(center, 0, 29), center, angle)
        ellipse(draw, center, 12, 35, base, outline, 2)
        ellipse(draw, add(paw, 0, 8), 16, 10, "#f9ddbc", outline, 2)

    # Head and facial features stay above the neck. Ears attach to skull landmarks.
    ellipse(draw, head, 58, 52, base, outline, 3)
    ellipse(draw, add(head, -8, 12), 36, 26, "#fbe4c4", None)
    ear_left_root = add(head, -37, -31)
    ear_right_root = add(head, 28, -34)
    if ear_trait["shape"] == "leaf":
        left = [ear_left_root, rotate(add(ear_left_root, -18, -54), ear_left_root, pose["ear_a"]), add(ear_left_root, 22, -12)]
        right = [ear_right_root, rotate(add(ear_right_root, 22, -55), ear_right_root, -pose["ear_a"]), add(ear_right_root, -20, -10)]
    else:
        left = [ear_left_root, rotate(add(ear_left_root, -12, -64), ear_left_root, pose["ear_a"]), add(ear_left_root, 24, -9)]
        right = [ear_right_root, rotate(add(ear_right_root, 18, -64), ear_right_root, -pose["ear_a"]), add(ear_right_root, -22, -8)]
    polygon(draw, left, shade, outline)
    polygon(draw, right, shade, outline)
    polygon(draw, [add(left[0], 4, -8), add(left[1], 3, 18), add(left[2], -7, -3)], "#f2b7a4")
    polygon(draw, [add(right[0], -4, -8), add(right[1], -3, 18), add(right[2], 7, -3)], "#f2b7a4")

    eye_y = head[1] - 2
    ellipse(draw, (head[0] - 23, eye_y), 8, 12, "#17212a")
    ellipse(draw, (head[0] + 21, eye_y), 8, 12, "#17212a")
    ellipse(draw, (head[0] - 20, eye_y - 4), 3, 4, "#e9ffff")
    ellipse(draw, (head[0] + 24, eye_y - 4), 3, 4, "#e9ffff")
    ellipse(draw, (head[0], head[1] + 15), 5, 4, "#6f3f34")
    draw.arc((head[0] - 12, head[1] + 16, head[0] + 2, head[1] + 28), 10, 80, fill="#6f3f34", width=2)
    draw.arc((head[0] - 2, head[1] + 16, head[0] + 12, head[1] + 28), 100, 170, fill="#6f3f34", width=2)

    if charm_trait["shape"] == "bell":
        ellipse(draw, (head[0] + 2, head[1] + 54), 11, 13, core, outline, 2)
        draw.line((head[0] - 30, head[1] + 46, head[0] + 32, head[1] + 47), fill=accent, width=5)
    elif charm_trait["shape"] == "flower":
        for i in range(5):
            a = i * math.tau / 5
            ellipse(draw, (head[0] + 42 + math.cos(a) * 7, head[1] + 30 + math.sin(a) * 7), 6, 5, "#f4a3b7")
        ellipse(draw, (head[0] + 42, head[1] + 30), 4, 4, core)

    return img


def save_strip(frames: list[Image.Image], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    strip = Image.new("RGBA", (CANVAS[0] * len(frames), CANVAS[1]), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        strip.alpha_composite(frame, (i * CANVAS[0], 0))
    strip.save(path)


def generate(config_path: Path, output_dir: Path, species_id: str, seed: str, frames: int) -> dict[str, Any]:
    config = load_config(config_path)
    species = next((s for s in config["species"] if s["id"] == species_id), None)
    if not species:
        raise ValueError(f"Unknown species id: {species_id}")
    rng = random.Random(f"{species_id}:{seed}")
    selected = build_traits(config, rng)
    dna = trait_dna(species_id, seed, selected)
    creature_dir = output_dir / species_id
    creature_dir.mkdir(parents=True, exist_ok=True)

    states = config["animationStates"]
    for state in states:
        state_id = state["id"]
        state_frames = int(state.get("frames", frames))
        rendered = [draw_creature(config, selected, state_id, i, state_frames) for i in range(state_frames)]
        save_strip(rendered, creature_dir / f"{state_id}_strip.png")
        if state_id == "idle":
            rendered[0].save(creature_dir / "preview.png")

    metadata = {
        "name": species["displayName"],
        "speciesId": species_id,
        "seed": seed,
        "dna": dna,
        "anatomy": config["anatomy"],
        "traits": [
            {"trait_type": layer_id, "value": trait.name}
            for layer_id, trait in selected.items()
        ],
        "animationStates": [s["id"] for s in states],
        "compiler": "Pet Grave Layer System",
        "sourceInfluence": "HashLips-style ordered weighted layers, adapted for anatomy-aware game sprites.",
    }
    with (creature_dir / "metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Pet Grave layered creature sprites.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--species", default="gravepup")
    parser.add_argument("--seed", default="memorial-garden")
    parser.add_argument("--frames", type=int, default=8)
    args = parser.parse_args()
    metadata = generate(args.config, args.out, args.species, args.seed, args.frames)
    print(json.dumps({"generated": metadata["name"], "dna": metadata["dna"], "out": str(args.out / args.species)}, indent=2))


if __name__ == "__main__":
    main()
