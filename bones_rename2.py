import bpy
import random

def delete_armature():
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE':
            bpy.data.objects.remove(obj, do_unlink=True)
    for arm in bpy.data.armatures:
        bpy.data.armatures.remove(arm)
    print("Ancienne armature supprimée.")

def create_new_armature(name="Armature"):
    arm_data = bpy.data.armatures.new(name)
    arm_object = bpy.data.objects.new(name, arm_data)
    bpy.context.collection.objects.link(arm_object)
    bpy.context.view_layer.objects.active = arm_object
    arm_object.select_set(True)
    print("Nouvelle armature créée.")
    return arm_object

def add_selected_bones(armature, selected_bone_names):
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    for i, name in enumerate(selected_bone_names):
        bone = edit_bones.new(name)
        bone.head = (0, i * 0.5, 0)
        bone.tail = (0, i * 0.5 + 0.4, 0)

    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"{len(selected_bone_names)} bones ajoutés : {selected_bone_names}")

def keep_and_rename_bones(armature, rename_dict):
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    for bone in list(edit_bones):
        if bone.name in rename_dict:
            bone.name = rename_dict[bone.name]
        else:
            edit_bones.remove(bone)

    bpy.ops.object.mode_set(mode='OBJECT')
    print("Bones filtrés et renommés selon le dictionnaire.")

# === Utilisation ===

rename_dict = {
    "Bone_001": "New_001",
    "Bone_002": "New_002",
    "Bone_004": "New_004"
}

mandatory_bone_names = list(rename_dict.keys())
all_possible_bones = [f"Bone_{i:03d}" for i in range(1, 21)]

total_count = random.randint(5, 20)
selected_bones = set(random.sample(all_possible_bones, total_count))
selected_bones.update(mandatory_bone_names)

delete_armature()
armature = create_new_armature()
add_selected_bones(armature, sorted(selected_bones))
keep_and_rename_bones(armature, rename_dict)
