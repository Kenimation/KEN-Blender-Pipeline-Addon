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
    importlib.reload(copytransform),
    importlib.reload(model_importer),
    importlib.reload(world_importer),
    importlib.reload(materials),
    importlib.reload(lights),
    importlib.reload(cameras),
    importlib.reload(images),
    importlib.reload(particles),
    importlib.reload(pie_menu),
    importlib.reload(modifiers_panel),
    importlib.reload(constraints_panel),
    importlib.reload(materials_panel),
    importlib.reload(pose_tools),
    importlib.reload(editing_tools),
    importlib.reload(animation_tools),
    importlib.reload(materials_tools),

else:
    from . import (
        addonPreferences,
        icons,
    )
    from .Assets import(
        assetsUI,
        assetsOperators,
        assetsNodePreset,
    )
    from .Assets.Anime import(
        AnimeUI,
        AnimeOperators,
    )
    from .Assets.Minecraft import(
        minecraftUI,
        minecraftOperators,
    )
    from .Assets.Libraries import(
        materials,
        lights,
        cameras,
        images,
        particles,
    )
    from .Operatiors import(
        save_cams,
        camera_shakify,
        uv_drag,
        vertex_groups,
        clean_resources,
        pose_tools,
        animation_tools,
        materials_tools,
        editing_tools,
        copytransform,
        model_importer,
        world_importer,
    )
    from .UI import(
        pie_menu,
        modifiers_panel,
        constraints_panel,
        materials_panel,
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
    copytransform,
    vertex_groups,
    clean_resources,
    materials,
    lights,
    cameras,
    images,
    particles,
    model_importer,
    world_importer,
    editing_tools,
    animation_tools,
    pose_tools,
    materials_tools,
    modifiers_panel,
    constraints_panel,
    materials_panel,
    pie_menu,
)

def register(bl_info):
    for mod in module_list:
        mod.register()

def unregister(bl_info):
    for mod in reversed(module_list):
        mod.unregister()