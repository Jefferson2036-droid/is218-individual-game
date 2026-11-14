"""Render Arena Climb fighter sprites with Blender.

Imports one model per fighter, tints it for each gear item, and renders a
transparent PNG of every fighter + gear combination.

Run from the repository root (Blender must be installed):

    /Applications/Blender.app/Contents/MacOS/Blender --background \
        --python art/blender/make_sprites.py -- \
        --models art/models --out art/renders

Expected model files in --models (any one format per fighter):
    knight.glb | knight.gltf | knight.fbx | knight.obj
    archer.glb | ...
    wizard.glb | ...

Output: art/renders/<fighter>-<gear>.png, e.g. knight-gold-armor.png

Status: written 2026-11-13, NOT RUN yet (Blender was not installed when
this was written). Expect to adjust camera framing once real models load.
"""

import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

# Gear tints (RGB 0-1). "starter" means the model's own colors.
# Keep ids in sync with docs/game-design.md and the prototype's ITEMS list.
GEAR = {
    "knight": {
        "starter": None,
        "gold-armor": (0.91, 0.69, 0.29),
        "dragon-shield": (0.84, 0.27, 0.27),
    },
    "archer": {
        "starter": None,
        "flame-bow": (1.00, 0.48, 0.24),
        "shadow-cloak": (0.56, 0.56, 0.72),
    },
    "wizard": {
        "starter": None,
        "storm-staff": (0.31, 0.76, 0.97),
        "arcane-purple": (0.75, 0.41, 1.00),
    },
}

MODEL_EXTENSIONS = (".glb", ".gltf", ".fbx", ".obj")


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Render Arena Climb sprites")
    parser.add_argument("--models", default="art/models", help="folder with knight/archer/wizard model files")
    parser.add_argument("--out", default="art/renders", help="folder for rendered PNGs")
    parser.add_argument("--size", type=int, default=512, help="square image size in pixels")
    parser.add_argument("--only", choices=sorted(GEAR), help="render just one fighter")
    return parser.parse_args(argv)


def find_model(folder, fighter):
    for ext in MODEL_EXTENSIONS:
        path = os.path.join(folder, fighter + ext)
        if os.path.isfile(path):
            return path
    return None


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_model(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".glb", ".gltf"):
        bpy.ops.import_scene.gltf(filepath=path)
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=path)
    elif ext == ".obj":
        # Blender 4.x importer; older versions used import_scene.obj
        if hasattr(bpy.ops.wm, "obj_import"):
            bpy.ops.wm.obj_import(filepath=path)
        else:
            bpy.ops.import_scene.obj(filepath=path)
    else:
        raise ValueError("Unsupported model type: " + path)
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]


def bounds(meshes):
    """World-space bounding box of all meshes: (min Vector, max Vector)."""
    lo = Vector((math.inf, math.inf, math.inf))
    hi = Vector((-math.inf, -math.inf, -math.inf))
    for obj in meshes:
        for corner in obj.bound_box:
            p = obj.matrix_world @ Vector(corner)
            lo = Vector((min(lo.x, p.x), min(lo.y, p.y), min(lo.z, p.z)))
            hi = Vector((max(hi.x, p.x), max(hi.y, p.y), max(hi.z, p.z)))
    return lo, hi


def tint_materials(meshes, rgb):
    """Multiply every material's base color by rgb (keeps textures)."""
    seen = set()
    for obj in meshes:
        for slot in obj.material_slots:
            mat = slot.material
            if mat is None or mat.name in seen:
                continue
            seen.add(mat.name)
            mat.use_nodes = True
            nodes, links = mat.node_tree.nodes, mat.node_tree.links
            bsdf = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)
            if bsdf is None:
                continue
            base = bsdf.inputs["Base Color"]
            if base.is_linked:
                # Texture -> Multiply(texture, tint) -> Base Color
                source = base.links[0].from_socket
                mix = nodes.new("ShaderNodeMix")
                mix.data_type = "RGBA"
                mix.blend_type = "MULTIPLY"
                mix.inputs["Factor"].default_value = 1.0
                a = next(s for s in mix.inputs if s.name == "A" and s.type == "RGBA")
                b = next(s for s in mix.inputs if s.name == "B" and s.type == "RGBA")
                out = next(s for s in mix.outputs if s.name == "Result" and s.type == "RGBA")
                links.new(source, a)
                b.default_value = (rgb[0], rgb[1], rgb[2], 1.0)
                links.new(out, base)
            else:
                r, g, bl, alpha = base.default_value
                base.default_value = (r * rgb[0], g * rgb[1], bl * rgb[2], alpha)


def setup_camera_and_lights(meshes, size):
    scene = bpy.context.scene
    lo, hi = bounds(meshes)
    center = (lo + hi) / 2
    dims = hi - lo
    tallest = max(dims.x, dims.z, 0.001)

    # Orthographic camera looking at the model's front (-Y side toward +Y).
    cam_data = bpy.data.cameras.new("SpriteCamera")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = tallest * 1.25
    cam = bpy.data.objects.new("SpriteCamera", cam_data)
    scene.collection.objects.link(cam)
    cam.location = (center.x, lo.y - tallest * 3, center.z)
    cam.rotation_euler = (math.radians(90), 0, 0)
    scene.camera = cam

    # Key light plus soft world light.
    sun_data = bpy.data.lights.new("Key", type="SUN")
    sun_data.energy = 3.0
    sun = bpy.data.objects.new("Key", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(50), math.radians(10), math.radians(-30))

    world = bpy.data.worlds.new("SpriteWorld")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.8, 0.8, 0.85, 1.0)
        bg.inputs["Strength"].default_value = 0.6
    scene.world = world

    # Transparent PNG output.
    for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
        try:
            scene.render.engine = engine
            break
        except TypeError:
            continue
    scene.render.film_transparent = True
    scene.render.resolution_x = size
    scene.render.resolution_y = size
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"


def render_variant(model_path, fighter, gear_id, tint, out_dir, size):
    reset_scene()
    meshes = import_model(model_path)
    if not meshes:
        raise RuntimeError("No meshes found in " + model_path)
    if tint is not None:
        tint_materials(meshes, tint)
    setup_camera_and_lights(meshes, size)
    out_path = os.path.join(out_dir, "%s-%s.png" % (fighter, gear_id))
    bpy.context.scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    return out_path


def main():
    args = parse_args()
    models = os.path.abspath(args.models)
    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    fighters = [args.only] if args.only else sorted(GEAR)
    missing, written = [], []
    for fighter in fighters:
        path = find_model(models, fighter)
        if path is None:
            missing.append(fighter)
            continue
        for gear_id, tint in GEAR[fighter].items():
            written.append(render_variant(path, fighter, gear_id, tint, out_dir, args.size))
            print("Rendered", written[-1])

    print("\nDone: %d image(s) in %s" % (len(written), out_dir))
    if missing:
        print("Missing models for: %s (expected e.g. %s/%s.glb)" % (", ".join(missing), models, missing[0]))
        sys.exit(1)


if __name__ == "__main__":
    main()
