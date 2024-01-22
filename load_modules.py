import importlib

if "bpy" in locals():
    importlib.reload(minecraftOperators),
    importlib.reload(minecraftUI),
    importlib.reload(AnimeUI),
    importlib.reload(AnimeOperators),
    importlib.reload(icons),
    importlib.reload(assetsUI),
    importlib.reload(assetsOperators),
    importlib.reload(assetsNodePreset),
    importlib.reload(addonPreferences),
    importlib.reload(camera_shakify),
    importlib.reload(uv_drag),
    importlib.reload(vertex_groups),
    importlib.reload(clean_resources),
    importlib.reload(modifiers_ui),
    importlib.reload(constraints_ui),
    importlib.reload(pose_tools),
    importlib.reload(animation_tools),
    importlib.reload(copytransform),
    importlib.reload(material_tool),
    importlib.reload(pie_menu),
    importlib.reload(model_importer),
    importlib.reload(world_importer),
    importlib.reload(editing),

else:
    from . import (
        addonPreferences,
        icons,
    )
    from .AssetsUI import(
        assetsUI,
        assetsOperators,
        assetsNodePreset,
    )
    from .Minecraft import(
        minecraftUI,
        minecraftOperators,
    )
    from .Anime import(
        AnimeUI,
        AnimeOperators,
    )
    from .Operations import(
        save_cams,
        camera_shakify,
        uv_drag,
        vertex_groups,
        clean_resources,
        pose_tools,
        pie_menu,
        animation_tools,
        copytransform,
        material_tool,
        model_importer,
        world_importer,
        editing,
    )
    from .UI import(
        modifiers_ui,
        constraints_ui,
    )

module_list = (
    save_cams,
    addonPreferences,
    minecraftUI,
    AnimeUI,
    minecraftOperators,
    AnimeOperators,
    assetsUI,
    assetsOperators,
    assetsNodePreset,
    camera_shakify,
    uv_drag,
    pose_tools,
    modifiers_ui,
    constraints_ui,
    pie_menu,
    animation_tools,
    copytransform,
    vertex_groups,
    clean_resources,
    material_tool,
    model_importer,
    world_importer,
    editing,
)

def register(bl_info):
    for mod in module_list:
        mod.register()

def unregister(bl_info):
    for mod in reversed(module_list):
        mod.unregister()