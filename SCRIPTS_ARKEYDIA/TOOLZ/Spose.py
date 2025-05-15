import bpy
import math

# Récupérer l'armature dans la scène
def get_armature():
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            return obj
    return None

# Activer l'objet spécifié
def activate_object(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

# Passer en mode POSE
def enter_pose_mode(obj):
    bpy.ops.object.mode_set(mode='POSE')

# Désélectionner tous les bones dans l'armature
def deselect_all_bones(obj):
    for pb in obj.pose.bones:
        pb.bone.select = False

# Sélectionner un bone spécifique
def select_bone(obj, bone_name):
    bone = obj.pose.bones.get(bone_name)
    if bone:
        bone.bone.select = True
        obj.data.bones.active = bone.bone
        return bone
    else:
        print(f"Bone '{bone_name}' non trouvé.")
        return None

# Sélectionner plusieurs bones à la fin
def select_bones(obj, bone_names):
    for bone_name in bone_names:
        bone = obj.pose.bones.get(bone_name)
        if bone:
            bone.bone.select = True

# Appliquer une rotation selon l'axe donné
def apply_rotation_axis(bone, axis, value):
    if bone:
        bone.rotation_mode = 'XYZ'
        if axis == 'X':
            bone.rotation_euler[0] = value
        elif axis == 'Y':
            bone.rotation_euler[1] = value
        elif axis == 'Z':
            bone.rotation_euler[2] = value
        print(f"Rotation {axis} = {value} appliquée à {bone.name}")

# Appliquer une rotation sur un axe donné à une liste de bones
def run_rotation_on_bones(bone_names, rotation_value, axis='Y'):
    armature = get_armature()
    if not armature:
        print("Aucune armature trouvée.")
        return

    activate_object(armature)
    enter_pose_mode(armature)

    for bone_name in bone_names:
        bone = select_bone(armature, bone_name)
        apply_rotation_axis(bone, axis, rotation_value)

# Liste des bones à modifier (rotation Y)
bone_list1 = [
    "VRimb_Naked:upperarm_l",
    "VRimb_Naked:upperarm_r"
]

# Liste des bones à modifier (rotation Z)
bone_list2 = [
    "VRimb_Naked:lowerarm_l",
    "VRimb_Naked:lowerarm_r"
]

# Combinaison des deux listes pour la sélection finale
all_bones = bone_list1 + bone_list2

# Appliquer la rotation Y = 0°
deselect_all_bones(get_armature())
run_rotation_on_bones(bone_list1, -math.radians(0), axis='Y')

# Appliquer la rotation Z = 0°
run_rotation_on_bones(bone_list2, math.radians(0), axis='Z')

# Sélection finale des deux listes
select_bones(get_armature(), all_bones)
