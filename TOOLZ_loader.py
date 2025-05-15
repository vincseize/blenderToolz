bl_info = {
    "name": "TOOLZ Menu",
    "author": "TonNom",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Barre du haut",
    "description": "Ajoute un menu TOOLZ dans la barre principale",
    "category": "3D View",
}

import bpy
import os
import importlib.util
import json

SCRIPTS_DIR = r"C:\SCRIPTS_ARKEYDIA\TOOLZ"

# --------- OPÉRATEURS ---------
class TOOLZ_OT_ExportSelectedBones(bpy.types.Operator):
    bl_idname = "toolz.export_selected_bones"
    bl_label = "Exporter les Bones sélectionnés"
    bl_description = "Sauvegarde les noms des bones sélectionnés dans un fichier JSON"

    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "Aucune armature sélectionnée")
            return {'CANCELLED'}

        mode = obj.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        selected_bones = [b.name for b in obj.data.bones if b.select]

        if not selected_bones:
            self.report({'INFO'}, "Aucun bone sélectionné")
            bpy.ops.object.mode_set(mode=mode)
            return {'CANCELLED'}

        path = os.path.join(
            os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.path.expanduser("~"),
            "selected_bones.json"
        )

        try:
            with open(path, 'w') as f:
                json.dump(selected_bones, f, indent=4)
        except Exception as e:
            self.report({'ERROR'}, f"Erreur écriture JSON: {e}")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode=mode)
        self.report({'INFO'}, f"Exporté vers {path}")
        return {'FINISHED'}

# --------- CHARGEMENT DYNAMIQUE ---------
def find_scripts():
    if not os.path.exists(SCRIPTS_DIR):
        return []
    return [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".py")]

def run_script(script_name):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    spec = importlib.util.spec_from_file_location("external_script", script_path)
    if spec is None:
        print(f"Impossible de charger {script_name}")
        return
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        if hasattr(module, "main"):
            module.main()
        else:
            print(f"Aucune fonction 'main()' dans {script_name}")
    except Exception as e:
        print(f"Erreur lors de l'exécution de {script_name} : {e}")

class TOOLZ_OT_RunScript(bpy.types.Operator):
    bl_idname = "toolz.run_script"
    bl_label = "Exécuter un script externe"
    bl_description = "Exécute un script Python externe depuis TOOLZ"

    script_name: bpy.props.StringProperty()

    def execute(self, context):
        run_script(self.script_name)
        return {'FINISHED'}

# --------- MENU TOOLZ ---------
class TOOLZ_MT_Menu(bpy.types.Menu):
    bl_label = "TOOLZ"
    bl_idname = "TOOLZ_MT_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("toolz.export_selected_bones", icon='EXPORT')
        layout.separator()
        layout.label(text="Scripts externes :")
        for script in find_scripts():
            op = layout.operator("toolz.run_script", text=script.replace(".py", ""))
            op.script_name = script

# --------- AJOUT AU HEADER ---------
_draw_toolz_func = None  # Référence persistante

def draw_toolz_menu(self, context):
    self.layout.menu(TOOLZ_MT_Menu.bl_idname)

# --------- REGISTER / UNREGISTER ---------
classes = [
    TOOLZ_OT_ExportSelectedBones,
    TOOLZ_OT_RunScript,
    TOOLZ_MT_Menu,
]

def register():
    global _draw_toolz_func
    for cls in classes:
        bpy.utils.register_class(cls)

    # Supprimer le précédent si déjà là
    if _draw_toolz_func:
        try:
            bpy.types.TOPBAR_MT_editor_menus.remove(_draw_toolz_func)
        except:
            pass

    _draw_toolz_func = draw_toolz_menu
    bpy.types.TOPBAR_MT_editor_menus.append(_draw_toolz_func)

def unregister():
    global _draw_toolz_func
    try:
        bpy.types.TOPBAR_MT_editor_menus.remove(_draw_toolz_func)
    except:
        pass
    _draw_toolz_func = None

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
