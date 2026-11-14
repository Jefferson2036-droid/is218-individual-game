"""Render Arena Climb fighter sprites with Blender.

Imports one model per fighter, tints it for each gear item, and renders a
transparent PNG of every fighter + gear combination.

Two ways to run it:

1. From Terminal, at the repository root:

    /Applications/Blender.app/Contents/MacOS/Blender --background \
        --python art/blender/make_sprites.py

2. Inside Blender: Scripting workspace -> Text -> Open -> this file -> Run Script.

Defaults: models from art/models, images to art/renders (paths are found
from this script's location, so it works from any folder).

Expected model files in art/models (any one format per fighter):
    knight.(glb|gltf|fbx|obj), archer.(...), wizard.(...)
Textures may sit in art/models/textures; a material named "Ranger_Texture"
is matched to textures/Ranger_Texture.png (or any PNG ending in that name).

Output: art/renders/<fighter>-<gear>.png, e.g. knight-gold-armor.png
"""

import argparse
import glob
import math
import os
import sys

import bpy
from mathutils import Vector

# Gear tints (RGB 0-1). "starter" keeps the model's own colors.
# Keep ids in sync with docs/game-design.md and prototype/index.html (ITEMS).
GEAR = {
    "knight": {
        "starter": None,
        "gold-armor": (1.00, 0.78, 0.30),
        "dragon-shield": (0.95, 0.35, 0.32),
    },
    "archer": {
        "starter": None,
        "flame-bow": (1.00, 0.55, 0.28),
        "shadow-cloak": (0.55, 0.55, 0.75),
    },
    "wizard": {
        "starter": None,
        "storm-staff": (0.40, 0.80, 1.00),
        "arcane-purple": (0.78, 0.45, 1.00),
    },
}

MODEL_EXTENSIONS = (".glb", ".gltf", ".fbx", ".obj")
CAMERA_TURN_DEG = 25     # turn the camera a little so the fighter is seen at a 3/4 angle
CAMERA_TILT_DEG = 8      # look down slightly


# ---------- paths ----------

def script_path():
    """Path of this file, whether run with --python or from Blender's text editor."""
    candidate = globals().get("__file__")
    if candidate and os.path.isfile(candidate):
        return os.path.abspath(candidate)
    for text in bpy.data.texts:
        if text.filepath and text.filepath.endswith("make_sprites.py"):
            return os.path.abspath(bpy.path.abspath(text.filepath))
    return None


def repo_root():
    path = script_path()
    if path:
        # art/blender/make_sprites.py -> repository root
        return os.path.dirname(os.path.dirname(os.path.dirname(path)))
    return os.getcwd()


def parse_args():
    root = repo_root()
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Render Arena Climb sprites")
    parser.add_argument("--models", default=os.path.join(root, "art", "models"))
    parser.add_argument("--out", default=os.path.join(root, "art", "renders"))
    parser.add_argument("--size", type=int, default=512, help="square image size in pixels")
    parser.add_argument("--only", choices=sorted(GEAR), help="render just one fighter")
    return parser.parse_args(argv)


def find_model(folder, fighter):
    for ext in MODEL_EXTENSIONS:
        path = os.path.join(folder, fighter + ext)
        if os.path.isfile(path):
            return path
    return None


# ---------- scene ----------

def clear_scene():
    """Remove everything so each variant starts clean (safe inside the Blender window too)."""
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for collection in (bpy.data.meshes, bpy.data.materials, bpy.data.images, bpy.data.cameras,
                       bpy.data.lights, bpy.data.armatures, bpy.data.actions, bpy.data.worlds,
                       bpy.data.node_groups):
        for block in list(collection):
            if block.users == 0:
                collection.remove(block)


def import_model(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".glb", ".gltf"):
        bpy.ops.import_scene.gltf(filepath=path)
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=path)
    elif ext == ".obj":
        if hasattr(bpy.ops.wm, "obj_import"):
            bpy.ops.wm.obj_import(filepath=path)
        else:
            bpy.ops.import_scene.obj(filepath=path)
    else:
        raise ValueError("Unsupported model type: " + path)
    return [o for o in bpy.context.scene.objects if o.type == "MESH"]


def attach_textures(meshes, models_dir):
    """Give each material its texture if the import didn't link one."""
    pngs = glob.glob(os.path.join(models_dir, "textures", "*.png")) + glob.glob(os.path.join(models_dir, "*.png"))
    by_stem = {os.path.splitext(os.path.basename(p))[0].lower(): p for p in pngs}
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
            if bsdf is None or bsdf.inputs["Base Color"].is_linked:
                continue
            key = mat.name.split(".")[0].lower()           # "Ranger_Texture.001" -> "ranger_texture"
            path = by_stem.get(key) or next((p for s, p in by_stem.items() if s.endswith(key)), None)
            if not path:
                continue
            tex = nodes.new("ShaderNodeTexImage")
            tex.image = bpy.data.images.load(path, check_existing=True)
            links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])


def use_idle_pose():
    """Pose armatures with an Idle animation if the model has one."""
    idle = next((a for a in bpy.data.actions if "idle" in a.name.lower()), None)
    for obj in bpy.context.scene.objects:
        if obj.type == "ARMATURE" and idle is not None:
            if obj.animation_data is None:
                obj.animation_data_create()
            obj.animation_data.action = idle
    bpy.context.scene.frame_set(1)


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


def bounds(meshes):
    lo = Vector((math.inf, math.inf, math.inf))
    hi = Vector((-math.inf, -math.inf, -math.inf))
    for obj in meshes:
        for corner in obj.bound_box:
            p = obj.matrix_world @ Vector(corner)
            lo = Vector((min(lo.x, p.x), min(lo.y, p.y), min(lo.z, p.z)))
            hi = Vector((max(hi.x, p.x), max(hi.y, p.y), max(hi.z, p.z)))
    return lo, hi


def setup_camera_and_lights(meshes, size):
    scene = bpy.context.scene
    bpy.context.view_layer.update()
    lo, hi = bounds(meshes)
    center = (lo + hi) / 2
    dims = hi - lo
    tallest = max(dims.x, dims.y, dims.z, 0.001)
    dist = tallest * 4

    cam_data = bpy.data.cameras.new("SpriteCamera")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = tallest * 1.15
    cam_data.clip_start = tallest * 0.01
    cam_data.clip_end = tallest * 20
    cam = bpy.data.objects.new("SpriteCamera", cam_data)
    scene.collection.objects.link(cam)
    turn = math.radians(CAMERA_TURN_DEG)
    tilt = math.radians(CAMERA_TILT_DEG)
    # Camera faces +Y by default (rotation x = 90°); turn it around Z and tilt it down.
    cam.rotation_euler = (math.radians(90) - tilt, 0, turn)
    direction = Vector((-math.sin(turn), math.cos(turn), 0))
    cam.location = center - direction * dist + Vector((0, 0, dist * math.tan(tilt)))
    scene.camera = cam

    key_data = bpy.data.lights.new("Key", type="SUN")
    key_data.energy = 3.5
    key = bpy.data.objects.new("Key", key_data)
    scene.collection.objects.link(key)
    key.rotation_euler = (math.radians(45), math.radians(15), math.radians(-35))

    rim_data = bpy.data.lights.new("Rim", type="SUN")
    rim_data.energy = 1.5
    rim = bpy.data.objects.new("Rim", rim_data)
    scene.collection.objects.link(rim)
    rim.rotation_euler = (math.radians(-60), 0, math.radians(160))

    world = bpy.data.worlds.new("SpriteWorld")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.85, 0.85, 0.9, 1.0)
        bg.inputs["Strength"].default_value = 0.7
    scene.world = world

    for engine in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT", "CYCLES"):
        try:
            scene.render.engine = engine
            break
        except TypeError:
            continue
    try:
        scene.view_settings.view_transform = "Standard"   # keep texture colors as painted
    except TypeError:
        pass
    scene.render.film_transparent = True
    scene.render.resolution_x = size
    scene.render.resolution_y = size
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"


def render_variant(model_path, models_dir, fighter, gear_id, tint, out_dir, size):
    clear_scene()
    meshes = import_model(model_path)
    if not meshes:
        raise RuntimeError("No meshes found in " + model_path)
    attach_textures(meshes, models_dir)
    use_idle_pose()
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
    print("Models:", models)
    print("Output:", out_dir)

    fighters = [args.only] if args.only else sorted(GEAR)
    missing, written = [], []
    for fighter in fighters:
        path = find_model(models, fighter)
        if path is None:
            missing.append(fighter)
            continue
        for gear_id, tint in GEAR[fighter].items():
            written.append(render_variant(path, models, fighter, gear_id, tint, out_dir, args.size))
            print("Rendered", written[-1])

    print("\nDone: %d image(s) in %s" % (len(written), out_dir))
    if missing:
        print("Missing models for: %s" % ", ".join(missing))
        if bpy.app.background:
            sys.exit(1)


if __name__ == "__main__":
    main()
