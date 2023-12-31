# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                       bl_info
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

bl_info = {
    "name": "KEN Blender Pipeline",
    "author": "KEN",
    "version": (2, 1, 7),
    "blender": (4, 0, 0),
    "location": "3DView",
    "description": "KEN Blender Pipeline Addons",
    "warning": "",
    "wiki_url": "",
    "category": "KEN Pipeline"
    }

import importlib

if "load_modules" in locals():
    importlib.reload(load_modules)
else:
    from . import load_modules
    from . import addon_updater_ops


def register():
    addon_updater_ops.register(bl_info)
    load_modules.register(bl_info)

def unregister():
    addon_updater_ops.unregister(bl_info)
    load_modules.unregister(bl_info)
    
if __name__ == "__main__":
    register()
