import bpy

# Supprimer toutes les références à TOOLZ_MT_menu du header
def cleanup_toolz_menus():
    try:
        bpy.types.TOPBAR_MT_editor_menus.remove(draw_toolz_header)
        print("draw_toolz_header retiré du header.")
    except:
        print("draw_toolz_header n'était pas dans TOPBAR_MT_editor_menus.")

    # Supprimer toutes les classes TOOLZ_MT_menu et TOOLZ_OT_ExportSelectedBones si elles existent
    for cls_name in [
        "TOOLZ_MT_menu",
        "TOOLZ_OT_ExportSelectedBones"
    ]:
        cls = getattr(bpy.types, cls_name, None)
        if cls:
            try:
                bpy.utils.unregister_class(cls)
                print(f"Classe {cls_name} désenregistrée.")
            except RuntimeError:
                print(f"Classe {cls_name} déjà désenregistrée.")
        else:
            print(f"Classe {cls_name} non trouvée.")

# Fonction fictive, au cas où elle a été définie dans les anciens scripts
def draw_toolz_header(self, context):
    pass

# Exécution du nettoyage
cleanup_toolz_menus()
