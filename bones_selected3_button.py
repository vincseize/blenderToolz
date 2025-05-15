import bpy
import json
import os

# --------- OPÉRATEUR ---------
class TOOLZ_OT_ExportSelectedBones(bpy.types.Operator):
    bl_idname = "toolz.export_selected_bones"
    bl_label = "Export json Bones selected"
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

        if bpy.data.filepath:
            path = os.path.join(os.path.dirname(bpy.data.filepath), "selected_bones.json")
        else:
            path = os.path.join(os.path.expanduser("~"), "selected_bones.json")

        try:
            with open(path, 'w') as f:
                json.dump(selected_bones, f, indent=4)
        except Exception as e:
            self.report({'ERROR'}, f"Erreur écriture JSON: {e}")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode=mode)
        self.report({'INFO'}, f"Exporté vers {path}")
        return {'FINISHED'}

# --------- MENU TOOLZ ---------
class TOOLZ_MT_Menu(bpy.types.Menu):
    bl_label = "TOOLZ"
    bl_idname = "TOOLZ_MT_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator(TOOLZ_OT_ExportSelectedBones.bl_idname, icon='EXPORT')

# --------- AJOUT AU HEADER ---------
def draw_toolz_header(self, context):
    layout = self.layout
    layout.menu(TOOLZ_MT_Menu.bl_idname)

# --------- ENREGISTREMENT ---------
classes = [TOOLZ_OT_ExportSelectedBones, TOOLZ_MT_Menu]
_draw_handler_added = False  # Flag global

def register():
    global _draw_handler_added
    for cls in classes:
        bpy.utils.register_class(cls)

    if not _draw_handler_added:
        bpy.types.TOPBAR_MT_editor_menus.append(draw_toolz_header)
        _draw_handler_added = True

def unregister_toolz_button_only():
    global _draw_handler_added
    if _draw_handler_added:
        bpy.types.TOPBAR_MT_editor_menus.remove(draw_toolz_header)
        _draw_handler_added = False
        print("Bouton TOOLZ retiré.")
    else:
        print("Aucun bouton TOOLZ à retirer.")

def unregister():
    unregister_toolz_button_only()
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

# Pour appel direct depuis le script
if __name__ == "__main__":
    register()
