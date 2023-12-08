import importlib

if "bpy" in locals():
    importlib.reload(minecraftOperators),
    importlib.reload(AnimeOperators),
    importlib.reload(minecraftUI),
    importlib.reload(animeUI),
    importlib.reload(icons),
    importlib.reload(assetsDraw),
    importlib.reload(assetsUI),
    importlib.reload(assetsOperators),
    importlib.reload(assetsNodePreset),
    importlib.reload(addonPreferences),
    importlib.reload(camera_shakify),
    importlib.reload(uv_drag),
    importlib.reload(vertex_groups),

else:
    from . import (
        addonPreferences,
        icons,
        assetsUI,
        minecraftUI,
        animeUI,

        
    )
    from .Minecraft import(
        minecraftOperators,
    )
    from .Anime import(
        AnimeOperators,
    )
    from .AssetsUI import(
        assetsDraw,
        assetsOperators,
        assetsNodePreset,
    )
    from .Operations import(
        save_cams,
        camera_shakify,
        uv_drag,
        vertex_groups,
    )

module_list = (
    save_cams,
    addonPreferences,
    minecraftUI,
    animeUI,
    minecraftOperators,
    AnimeOperators,
    assetsDraw,
    assetsUI,
    assetsOperators,
    assetsNodePreset,
    camera_shakify,
    uv_drag,
    vertex_groups,
)

def register(bl_info):
    for mod in module_list:
        mod.register()
        

def unregister(bl_info):
    for mod in reversed(module_list):
        mod.unregister()