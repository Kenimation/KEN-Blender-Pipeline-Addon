import bpy
from bpy.types import WindowManager, Operator, Panel, Menu, UIList, PropertyGroup
from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatProperty, IntProperty, CollectionProperty
import os
import bmesh
from . import assetsDefs, assetsDraw
from .Minecraft import minecraftUI
from .Anime import AnimeProperties, AnimeUI, AnimeRig
from .Libraries import materials, lights, cameras, images
from .. import addonPreferences, addon_updater_ops, icons

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                      classes
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Assets_UI(bpy.types.Panel):
    bl_label = "KEN Pipeline"
    bl_idname = "OBJECT_PT_KEN_Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KEN Pipeline"
    
    def draw(self, context):
        addon_prefs = addonPreferences.getAddonPreferences(context)
        pcoll = preview_collections["main"]
        layout = self.layout
        scene = context.scene
        obj = context.object

        layout.label(text = "UI for Quick Tools Pipeline")
        box = layout.box()
        row = box.row()
        row.label(text = "Create by KEN", icon = 'RIGHTARROW')
        assetsDraw.drawheader(context, addon_prefs, row, obj)
        row.operator("open.addonprefsofaddon", icon = "SETTINGS", text = "")
        addon_updater_ops.check_for_update_background(context)
        addon_updater_ops.update_notice_box_ui(self, context, box)
        box = layout.box()
        row = box.row()
        row.prop(scene, "myProps", expand = True)
        row.scale_y = 1.25
        if scene.myProps == 'one':
            if addon_prefs.view == True and scene.view == True:
                row = box.row()
                assetsDraw.draw_view(addon_prefs, context, box, row, obj)
                box = layout.box()

            if obj:
                row = box.row()
                assetsDraw.draw_properties(addon_prefs, context, row, obj, pcoll)

                if obj.mode != 'EDIT':
                    assetsDraw.draw_transform(addon_prefs, context, box, obj)
                else:
                    assetsDraw.drawedit_transform(addon_prefs, context, box, obj)
                    
                if obj.RIG_ID not in AnimeProperties.kenriglist and scene.object_properties == True:
                    assetsDraw.drawobj_properties(self,context, obj)
                    
                assetsDraw.draw_edit(scene, box)

            if addon_prefs.tools == True and scene.tools == True:
                assetsDraw.draw_tools(self, scene, obj)

            if obj:
                if obj.type == 'MESH' and scene.mat == True:
                    materials.drawmaterial_properties(self, context, obj)

                if addon_prefs.advanced_option == True and scene.advanced_option == True:
                    assetsDraw.draw_data(self, context, obj)

                if addon_prefs.registered_name:
                    if any(item.registered_name in AnimeProperties.registered_name for item in addon_prefs.registered_name):
                        minecraftUI.draw_ken_mcrig(self, context, obj)
                        AnimeUI.draw_ken_animerig(self, context, obj)
                        AnimeRig.draw_horse_animerig(self, context, obj)

                if obj.RIG_ID in AnimeProperties.kenriglist and scene.object_properties == True:
                    assetsDraw.drawobj_properties(self,context, obj)

            else:
                box.alert = True
                box.label(text = "No Active Object.", icon = "OBJECT_DATAMODE")

        if scene.myProps == 'two':
            row = box.row()
            row.prop(scene, "libraries", expand = True)

            if scene.libraries == 'one':
                materials.draw_materials(self, context, box)

            if scene.libraries == 'two':
                lights.draw_lights(self, context, box)

            if scene.libraries == 'three':
                cameras.draw_cams(self, context, box)
            
            if scene.libraries == 'four':
                images.draw_images(self, context, box)

        if scene.myProps == 'three':
            row = box.row()
            row.label(icon = "SCENE_DATA")
            row.prop(scene, "name", text = "")
            box.label(text = "Output:", icon = "OUTPUT")
            box.label(text = "Resolution")
            row = box.row()
            row.prop(scene.render, "resolution_x", text = "X")
            row.prop(scene.render, "resolution_y", text = "Y")
            box.prop(scene.render, "fps", text = "FPS")
            box.prop(scene.render, "film_transparent", text = "Transparent")
            box.label(text = "Frame Range")
            row = box.row()
            row.prop(scene, "frame_start", text = "Start")
            row.prop(scene, "frame_end", text = "End")
            box.prop(scene, "frame_step", text = "Step")
            box.label(text = "File:")
            box.prop(scene.render, "filepath", text = "")
            row = box.row()
            row.prop(scene.render, "use_file_extension", toggle = True)
            row.prop(scene.render, "use_render_cache", toggle = True)
            box.template_image_settings(scene.render.image_settings, color_management=False)
            box.label(text = "Color Management:")
            row = box.row()
            row.prop(scene.render.image_settings, "color_management", expand = True)
            box.prop(scene.sequencer_colorspace_settings, "name", text = "Color Space")
            layout = self.layout
            box = layout.box()
            box.label(text = "Render:", icon = "SCENE")
            row = box.row()
            row.prop(scene, "finalrender", text = "", icon = "RESTRICT_RENDER_OFF")
            if scene.finalrender == True:
                row.operator("render.render", text = "Render Image", icon = "RENDER_STILL")
                row.operator("render.render", text = "Render Animation", icon = "RENDER_ANIMATION").animation = True
            else:
                row.operator("render.opengl", text = "Viewport Render", icon = "RENDER_STILL")
                row.operator("render.opengl", text = "Viewport Animation", icon = "RENDER_ANIMATION").animation = True
            for item in addon_prefs.registered_name:
                if item.registered_name == AnimeProperties.registered_name[2]:
                    ken_icon = pcoll["Dual"]
                    row.operator("render.anime_snap", text = "", icon_value = ken_icon.icon_id).mode = "Final"
            if scene.cycles.denoiser == 'OPTIX':
                box.operator("cycles.denoise_animation", text = "Optix Denoising Animation")
            box.label(text = "Render Settings")
            box.prop(scene.render, "engine", text = "Render Engine")
            if context.scene.render.engine in ["CYCLES"]:
                assetsDraw.draw_cycles(scene, box)
            if context.scene.render.engine in ["BLENDER_EEVEE"]:
                assetsDraw.draw_eevee(scene, box)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def update_category():
    bpy.utils.unregister_class(Assets_UI)
    addon_prefs = addonPreferences.getAddonPreferences(bpy.context)
    Assets_UI.bl_category = addon_prefs.category_name
    bpy.utils.register_class(Assets_UI)

preview_collections = {}

classes = (
            Assets_UI,
          )
def register():
    bpy.utils.register_class(Assets_UI)
    update_category()
    icon = icons.icons("Icons")
    pcoll = icon.getColl()
    icon.load(pcoll)
    preview_collections["main"] = pcoll

def unregister():
    from bpy.utils import unregister_class
    unregister_class(Assets_UI)

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()