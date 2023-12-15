import importlib

if "bpy" in locals():
    importlib.reload(minecraftOperators),
    importlib.reload(minecraftUI),
    importlib.reload(AnimeUI),
    importlib.reload(AnimeOperators),
    importlib.reload(icons),
    importlib.reload(assetsDraw),
    importlib.reload(assetsUI),
    importlib.reload(assetsOperators),
    importlib.reload(assetsNodePreset),
    importlib.reload(addonPreferences),
    importlib.reload(camera_shakify),
    importlib.reload(uv_drag),
    importlib.reload(vertex_groups),
    importlib.reload(fix_material),
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
        assetsDraw,
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
        fix_material,
        model_importer,
        world_importer,
        editing,
    )

module_list = (
    save_cams,
    addonPreferences,
    minecraftUI,
    AnimeUI,
    minecraftOperators,
    AnimeOperators,
    assetsUI,
    assetsDraw,
    assetsOperators,
    assetsNodePreset,
    camera_shakify,
    uv_drag,
    vertex_groups,
    fix_material,
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