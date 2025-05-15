import bpy
import json
import os

def deselect_all_bones_and_objects_then_return_to_edit():
    # Passer en mode OBJECT si nécessaire
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Désélectionner tous les objets
    bpy.ops.object.select_all(action='DESELECT')

    # Trouver la première armature dans la scène
    armature = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            armature = obj
            break

    if armature:
        # Sélectionner l'armature
        bpy.context.view_layer.objects.active = armature
        armature.select_set(True)

        # Passer en mode EDIT
        bpy.ops.object.mode_set(mode='EDIT')
        print("Tout a été désélectionné. Armature réactivée en mode EDIT.")
    else:
        print("Aucune armature trouvée.")

def show_selected_bones_names_and_save():
    obj = bpy.context.object
    if not obj or obj.type != 'ARMATURE':
        print("Sélectionne une armature.")
        return

    # Sauver le mode actuel pour pouvoir revenir plus tard
    current_mode = obj.mode

    # Si on est en mode EDIT, on peut récupérer les bones sélectionnés dans ce mode
    if current_mode == 'EDIT':
        selected_bones = [b.name for b in obj.data.edit_bones if b.select]
    else:
        selected_bones = []

    # Créer le message à afficher
    if selected_bones:
        message = "\n".join(selected_bones)
        print(message)
    else:
        message = "Aucun bone sélectionné."
        print(message)

    # Sauvegarder dans un fichier JSON
    save_selected_bones_to_json(selected_bones)

    def draw(self, context):
        for line in message.split('\n'):
            self.layout.label(text=line)

    bpy.context.window_manager.popup_menu(draw, title="Bones sélectionnés", icon='BONE_DATA')

    # Revenir au mode initial
    bpy.ops.object.mode_set(mode=current_mode)

def save_selected_bones_to_json(selected_bones):
    # Définir le chemin du fichier JSON au même niveau que le fichier .blend
    blend_file_path = bpy.data.filepath
    if blend_file_path:
        folder_path = os.path.dirname(blend_file_path)
        file_path = os.path.join(folder_path, "selected_bones.json")
    else:
        file_path = os.path.join(os.getcwd(), "selected_bones.json")

    # Écrire les bones sélectionnés dans le fichier JSON
    try:
        with open(file_path, 'w') as json_file:
            json.dump({"selected_bones": selected_bones}, json_file, indent=4)
        print(f"Les bones sélectionnés ont été enregistrés dans : {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du fichier JSON : {e}")

# Exemple d’appel
deselect_all_bones_and_objects_then_return_to_edit()
show_selected_bones_names_and_save()
