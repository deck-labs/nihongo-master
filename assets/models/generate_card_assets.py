"""
generate_card_assets.py
Procedural 3D model generator for Hiragana Card Game using Blender 5.2.
Builds playing_card.glb and felt_table.glb with tactile beveled geometry and PBR materials.
"""

import os
import math
import bpy

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def create_playing_card():
    clear_scene()
    
    # 1. Base Dimensions (1.0 wide, 1.4 tall, 0.02 thick)
    width = 1.0
    height = 1.4
    thickness = 0.02

    # Create base cube lying flat on table (Z is thickness/up in Blender)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    card = bpy.context.active_object
    card.name = "PlayingCard"
    card.scale = (width, height, thickness)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # 2. Add Bevel Modifier for rounded corners and smooth tactile edges
    bevel = card.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.05
    bevel.segments = 4
    bpy.ops.object.modifier_apply(modifier="Bevel")
    bpy.ops.object.shade_smooth()

    # 3. Materials
    mat_face = bpy.data.materials.new(name="CardFace")
    mat_face.use_nodes = True
    bsdf_f = mat_face.node_tree.nodes.get("Principled BSDF")
    if bsdf_f:
        bsdf_f.inputs["Base Color"].default_value = (0.97, 0.95, 0.91, 1.0)
        bsdf_f.inputs["Roughness"].default_value = 0.32

    mat_back = bpy.data.materials.new(name="CardBack")
    mat_back.use_nodes = True
    bsdf_b = mat_back.node_tree.nodes.get("Principled BSDF")
    if bsdf_b:
        bsdf_b.inputs["Base Color"].default_value = (0.15, 0.28, 0.45, 1.0)
        bsdf_b.inputs["Roughness"].default_value = 0.38

    mat_edge = bpy.data.materials.new(name="CardEdge")
    mat_edge.use_nodes = True
    bsdf_e = mat_edge.node_tree.nodes.get("Principled BSDF")
    if bsdf_e:
        bsdf_e.inputs["Base Color"].default_value = (0.92, 0.90, 0.86, 1.0)
        bsdf_e.inputs["Roughness"].default_value = 0.65

    card.data.materials.append(mat_face) # index 0
    card.data.materials.append(mat_back) # index 1
    card.data.materials.append(mat_edge) # index 2

    # 4. Assign Material Slots and Exact Flat UV Mapping
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(card.data)
    uv_layer = bm.loops.layers.uv.verify()

    for face in bm.faces:
        if face.normal.z > 0.6:
            face.material_index = 0
            for loop in face.loops:
                u = (loop.vert.co.x + width / 2.0) / width
                v = (loop.vert.co.y + height / 2.0) / height
                loop[uv_layer].uv = (u, v)
        elif face.normal.z < -0.6:
            face.material_index = 1
            for loop in face.loops:
                u = (loop.vert.co.x + width / 2.0) / width
                v = (loop.vert.co.y + height / 2.0) / height
                loop[uv_layer].uv = (u, v)
        else:
            face.material_index = 2
            for loop in face.loops:
                loop[uv_layer].uv = (0.5, 0.5)

    bm.to_mesh(card.data)
    bm.free()

    # Export GLB
    out_path = os.path.join(OUTPUT_DIR, "playing_card.glb")
    bpy.ops.export_scene.gltf(
        filepath=out_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True
    )
    print(f"Generated: {out_path} ({os.path.getsize(out_path)} bytes)")

def create_felt_table():
    clear_scene()

    # 1. Table Felt (Curved Stadium/Oval shape)
    bpy.ops.mesh.primitive_cylinder_add(radius=3.8, depth=0.1, vertices=64, location=(0, -0.05, 0))
    table = bpy.context.active_object
    table.name = "FeltTable"
    table.scale = (1.4, 0.85, 1.0) # Oval
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Felt Material
    mat_felt = bpy.data.materials.new(name="TableFelt")
    mat_felt.use_nodes = True
    bsdf = mat_felt.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.05, 0.16, 0.11, 1.0) # Deep emerald felt
        bsdf.inputs["Roughness"].default_value = 0.85
    table.data.materials.append(mat_felt)

    # 2. Wooden Cushion Rim
    bpy.ops.mesh.primitive_torus_add(
        align='WORLD',
        location=(0, 0.02, 0),
        rotation=(0, 0, 0),
        major_radius=3.8,
        minor_radius=0.18,
        major_segments=64,
        minor_segments=16
    )
    rim = bpy.context.active_object
    rim.name = "WoodRim"
    rim.scale = (1.4, 0.85, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    mat_wood = bpy.data.materials.new(name="TableWood")
    mat_wood.use_nodes = True
    bsdf_w = mat_wood.node_tree.nodes.get("Principled BSDF")
    if bsdf_w:
        bsdf_w.inputs["Base Color"].default_value = (0.16, 0.08, 0.04, 1.0) # Polished dark mahogany
        bsdf_w.inputs["Roughness"].default_value = 0.25
        bsdf_w.inputs["Metallic"].default_value = 0.1
    rim.data.materials.append(mat_wood)

    # Join into single table asset
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()
    bpy.context.active_object.name = "CasinoTable"

    # UV Unwrap
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

    out_path = os.path.join(OUTPUT_DIR, "felt_table.glb")
    bpy.ops.export_scene.gltf(
        filepath=out_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True
    )
    print(f"Generated: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    create_playing_card()
    create_felt_table()
    print("Blender 3D asset generation completed successfully!")
