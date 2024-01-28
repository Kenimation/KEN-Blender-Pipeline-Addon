import bpy
import os

from . import minecraftExtraProperties, minecraftDefs, minecraftProperties, minecraftOperators
from ..AssetsUI import assetsDraw, assetsDefs
from ..Anime import AnimeProperties
from .. import addonPreferences, icons

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def draw_ken_mcrig(self, context, obj):
    scene = context.scene
    if obj.get("RIG_ID") == AnimeProperties.kenriglist[0]:
        if obj.mode == 'OBJECT':
            if obj.type == 'ARMATURE':
                rig_class = "myrig"
                rig_get_class = scene.myrig
        elif obj.mode == 'POSE':
            rig_class = "myrigpose"
            rig_get_class = scene.myrigpose
        if obj.ken_mc_rig == True:
            layout = self.layout
            rig = context.active_object
            box = layout.box()
            row = box.row()
            row.label(text = "KEN Remastered v1.0_Rig", icon = "OUTLINER_OB_ARMATURE")
            row.prop(scene, "object_properties", icon = "ARMATURE_DATA", text = "")
            if rig.mode == 'EDIT':
                assetsDraw.drawbone_properties(box, context, obj)
            else:
                row.prop(scene, "myrig_ui_setting", text = "", icon = "SETTINGS")
                row = box.row()
                row.prop(rig, "AntiLag", icon = 'GRIP')
                row = box.row()
                row.prop(context.scene.render, "use_simplify", text = "Use Simplify", toggle = True)
                row.prop(context.scene.render, "simplify_subdivision", text = "Subdivision")
                row = box.row()
                row.prop(scene, rig_class, expand = True)
                if rig_get_class == "one":
                    drawrigdesign(self, context)
                if rig_get_class == "two":
                    drawrigmaterial(self, context)
                if rig_get_class == "three":
                    drawrigposing(self, context)
                if rig_get_class == "four":
                    drawriganimating(self, context)
            if scene.myrig_ui_setting == True:
                drawriguisetting(self, context)

    if obj.get("RIG_ID") == AnimeProperties.kenriglist[1]:
        if obj.mode == 'OBJECT':
            if obj.type == 'ARMATURE':
                rig_class = "riglayout"
                rig_get_class = scene.riglayout
        elif obj.mode == 'POSE':
            rig_class = "riglayoutpose"
            rig_get_class = scene.riglayoutpose
        if obj.ken_mc_rig == True:
            layout = self.layout
            rig = context.active_object
            box = layout.box()
            row = box.row()
            row.label(text = "KEN Rig Layout v1.0", icon = "OUTLINER_OB_ARMATURE")
            row = box.row()
            row.prop(rig, "AntiLag", icon = 'GRIP')
            row = box.row()
            row.prop(context.scene.render, "use_simplify", text = "Use Simplify", toggle = True)
            row.prop(context.scene.render, "simplify_subdivision", text = "Subdivision")
            row = box.row()
            row.prop(scene, rig_class, expand = True)
            if rig_get_class == "one":
                drawlayoutsetting(self, context)
            if rig_get_class == "two":
                drawlayoutposing(self, context)
            if rig_get_class == "three":
                drawriganimating(self, context)
     
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def drawlayoutsetting(self, context):
    layout = self.layout
    rig = context.active_object

    layout = self.layout
    rig = context.active_object
    material_obj = rig.children[0]
    color = material_obj.material_slots[0].material.node_tree.nodes['Diffuse BSDF'].inputs
    skin_texture = material_obj.material_slots[0].material.node_tree.nodes['Skin'].image

    ### skin
    box = layout.box()
    row = box.row()
    row.label(text = "Layout Setting:")
    
    row = box.row()
    row.prop(rig, "solid", expand = True)
    # skin normal
    if rig.solid == '0':
        row = box.row(align = True)
        row.label(text = "Skin:")
        row = box.row(align = True)  
        col = row.column()
        col.operator("pack.img" , text="", icon="UGLYPACKAGE" if assetsDefs.is_packed(skin_texture) else "PACKAGE").id_name = skin_texture.name 

        col = row.column() 
        if assetsDefs.is_packed(skin_texture) == False:
            col.enabled = False
        col.prop(skin_texture, "filepath", text="")

        col = row.column()
        if assetsDefs.is_packed(skin_texture) == False:
            col.enabled = False
        col.operator("reload.img", text = "", icon = "FILE_REFRESH").id_name = skin_texture.name 

        # skin library
        row = box.row(align = True)
        if assetsDefs.is_packed(skin_texture) == False:
            row.enabled = False
        else:
            row.operator("useskin.lib", text = "library")
            row.operator("openskin.lib", text = "", icon = "FILE_FOLDER")

    if rig.solid == '1':
        row = box.row()
        row.label(text = "Layout Color:")
        row = box.row()
        row.prop(color['Color'], "default_value", text = "", slider = True)


    row = box.row(align = True)
    row.label(text = "Design:")
    split = box.split()
    col = split.column()

    row = col.row()
    row.prop(rig, "FemaleMode", toggle = True)
    row.prop(rig, "SlimArms", toggle = True)
    col.prop(rig, "Chibi", toggle = True)

def drawlayoutposing(self, context):
    layout = self.layout
    rig = context.active_object
    box = layout.box().column()
    box.prop(rig, "show_in_front", icon = "HIDE_OFF", text = "Show bones in front")
    box.prop(rig, "flipBone", text = "Flip Bone", toggle = True)

    box = layout.box()
    row = box.row()
    row.alignment = 'CENTER'
    row.label(text = "Arms IK:")
    row.prop(rig, "Arm_IK_Right", text = "Right", slider = True)
    row.prop(rig, "Arm_IK_Left", text = "Left", slider = True)

    row = box.row()
    row.alignment = 'CENTER'
    row.label(text = "Legs IK:")
    row.prop(rig, "Leg_IK_Right", text = "Right", slider = True)
    row.prop(rig, "Leg_IK_Left", text = "Left", slider = True)

    box = layout.box()
    row = box.row()
    row.prop(rig, "HeadWorld", toggle = True)
    row = box.row()
    row.label(text="Arm World:")
    row.prop(rig, "ArmWorld_r", text = "Right", toggle = True)
    row.prop(rig, "ArmWorld_l", text = "Left" ,toggle = True)
    row = box.row()
    row.label(text="Wrist World:")
    row.prop(rig, "WristWorld_r", text = "Right", toggle = True)
    row.prop(rig, "WristWorld_l", text = "Left" ,toggle = True)
    row = box.row()
    row.prop(rig, "FingerPlus", text = "Finger Full Rigged", toggle = True)
        
    box = layout.box()
    split = box.split()
    col = split.column()
    col.label(text = "Smart Movement")
    col.prop(rig, "SmartMovement", toggle = True)
    if rig.get("SmartMovement"):
        row = box.row()
        row.prop(rig, "SmartMovement_Arm", slider = True)
        row = box.row()
        row.prop(rig, "SmartMovement_Leg", slider = True)
        row = box.row()
        row.prop(rig, "SmartMovement_Waist", slider = True)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def drawrigdesign(self, context):
    layout = self.layout
    rig = context.active_object
    material_obj = rig.children[0]
    try:
        blush = material_obj.material_slots[3].material.node_tree.nodes['Mix Shader'].inputs
    except:
        pass
    box = layout.box()
    row = box.row()
    row.label(text = "Design:")
    split = box.split()
    col = split.column()

    row = col.row()
    row.prop(rig, "FemaleMode", toggle = True)
    row.prop(rig, "SlimArms", toggle = True)
    col.prop(rig, "Chibi", toggle = True)
    col.prop(rig, "SecondLayer", toggle = True)
    col.prop(rig, "SmoothBends", toggle = True)
    col.prop(rig, "TextureDeform", toggle = True)
    row = col.row()
    row.prop(rig, "Facial", expand = True)
    col.prop(rig, "Finger", toggle = True)  
    col.prop(rig, "EyeBrowPosition", slider = True)
    col.prop(rig, "EyeBrowThickness", slider = True)
    col.prop(rig, "EyePosition", slider = True)
    try:
        col.prop(blush['Fac'],"default_value", text = "Blush", slider = True)
    except:
        pass

def drawrigmaterial(self, context):
    layout = self.layout
    rig = context.active_object
    material_obj = rig.children[0]
    sss_node = material_obj.material_slots[0].material.node_tree.nodes['Skin Mat'].inputs
    skin_texture = material_obj.material_slots[0].material.node_tree.nodes['Skin'].image
    eye_node = material_obj.material_slots[1].material.node_tree.nodes['Eyes'].inputs
    eyeball = material_obj.material_slots[2].material.node_tree.nodes['Eyeball'].inputs

    ### skin
    box = layout.box()
    row = box.row(align = True)
    row.label(text = "Skin:")

    
    # skin normal
    row = box.row(align = True)  
    col = row.column()
    col.operator("pack.img" , text="", icon="UGLYPACKAGE" if assetsDefs.is_packed(skin_texture) else "PACKAGE").id_name = skin_texture.name 

    col = row.column() 
    if assetsDefs.is_packed(skin_texture) == False:
        col.enabled = False
    col.prop(skin_texture, "filepath", text="")

    col = row.column()
    if assetsDefs.is_packed(skin_texture) == False:
        col.enabled = False
    col.operator("reload.img", text = "", icon = "FILE_REFRESH").id_name = skin_texture.name 

    # skin library
    row = box.row(align = True)
    if assetsDefs.is_packed(skin_texture) == False:
        row.enabled = False
    else:
        row.operator("useskin.lib", text = "library")
        row.operator("openskin.lib", text = "", icon = "FILE_FOLDER")

    ### SSS
    row = box.row()
    row.label(text = "Subsurface:")
    row = box.row()
    row.prop(sss_node['Subsurface Weight'], "default_value", text = "Subsurface", slider = True)
    row = box.row()
    row.prop(sss_node['Subsurface Radius'], "default_value", text = "Radius", slider = False)
    row = box.row()
    row.prop(sss_node['Auto Subsurf'], "default_value", text = "Auto Subsurf", slider = True)
    row = box.row()
    split = box.split()
    col = split.column(align = True)
    col.prop(sss_node['Skin Color'], "default_value", text = "")
    row = box.row()
    row.prop(sss_node['Sensitivity'], "default_value", text = "Sensitivity", slider = True)
    row = box.row()

    box = layout.box()
    row = box.row()
    row.label(text = "Face Type:")
    row = box.row()
    row.prop(sss_node['Lip'], "default_value", text = "Lip", slider = True)
    row = box.row()
    row.prop(sss_node['Lip Color'], "default_value", text = "")

    ### eyes
    box = layout.box()
    row = box.row()
    row.label(text = "Eye Type:")
    row = box.row()
    row.prop(rig, "EyesTwo", expand = True)
    row = box.row()
    row.prop(rig, "EyeType", expand = True)

    split = box.split()
    col = split.column(align = True)


    # solid
    if rig.get('EyeType') == 0:
        
        col.prop(eye_node['Color1'], "default_value", text = "")
        if rig.get("EyesTwo") == 1:
            col = split.column(align = True)
            col.prop(eye_node['Color2'], "default_value", text = "")
        row = box.row()
        row.prop(eye_node['Pupils Specular'], "default_value", text = "Pupils Specular", slider = True)
        row = box.row()
        row.prop(eye_node['Pupils Roughness'], "default_value", text = "Pupils Roughness", slider = True)
        row = box.row()
        row.prop(eye_node['Pupils Emission'], "default_value", text = "Pupils Emission", slider = True)
        row = box.row()
    # texture
    elif rig.get('EyeType') == 1:
        col.prop(eye_node['EyeSC'], "default_value", text = "")
        col.prop(eye_node['Color1'], "default_value", text = "")
        if rig.get("EyesTwo"):
            col = split.column(align = True)
            col.prop(eye_node['EyeSCOth'], "default_value", text = "")
            col.prop(eye_node['Color2'], "default_value", text = "")
        row = box.row()
        row.prop(rig, "EyeTextureType", expand = True)
        row = box.row()
        row.prop(eye_node['Pupils Specular'], "default_value", text = "Pupils Specular", slider = True)
        row = box.row()
        row.prop(eye_node['Pupils Roughness'], "default_value", text = "Pupils Roughness", slider = True)
        row = box.row()
        row.prop(eye_node['Pupils Emission'], "default_value", text = "Pupils Emission", slider = True)
        row = box.row()
        row.prop(eye_node['Pupils Threshold'], "default_value", text = "Pupils Threshold", slider = True)
        row = box.row()
        row.label(text = "Sparkle Type:")
        row = box.row()
        row.prop(eye_node['Sparkle Color'], "default_value", text = "")
        row = box.row()
        row.prop(rig, "SparkleTextureType", expand = True)
        row = box.row()
        row.prop(eye_node['Sparkle Emission'], "default_value", text = "Sparkle Emission", slider = True)
        row = box.row()
        row.label(text = "Pupils Dot:")
        row = box.row()
        row.prop(eye_node['Pupil Dot'], "default_value", text = "Pupil Dot", slider = True)
        row = box.row()
        row.prop(eye_node['Pupil Dot Deep'], "default_value", text = "Deep Dot", slider = True)
        row = box.row()
        row.prop(eye_node['Pupil Dot Size'], "default_value", text = "Size", slider = True)
        row = box.row()
        row.prop(eye_node['Pupil Dot Fallout'], "default_value", text = "Fallout", slider = True)
        row = box.row()
        row.label(text = "Pupils Normal Map:")
        row = box.row()
        row.prop(eye_node['Normal'], "default_value", text = "Pupils Normal Map", slider = True)
        row = box.row()
    
    row.label(text = "Eyeball:")
    split = box.split()
    col = split.column(align = True)
    if rig.get("EyesTwo") == 1:
        col.prop(eyeball['EyeballColor1'], "default_value", text = "")
        col = split.column(align = True)
        col.prop(eyeball['EyeballColor2'], "default_value", text = "")
    else:
        col.prop(eyeball['EyeballColor1'], "default_value", text = "")
    row = box.row()
    row.prop(eyeball['Specular'], "default_value", text = "Specular", slider = True)
    row = box.row()
    row.prop(eyeball['Roughness'], "default_value", text = "Roughness", slider = True)
    row = box.row()
    row.prop(eyeball['Emission'], "default_value", text = "Emission", slider = True)

def drawrigposing(self, context):
    layout = self.layout
    rig = context.active_object
    box = layout.box().column()
    box.prop(rig, "show_in_front", icon = "HIDE_OFF", text = "Show bones in front")
    box.prop(rig, "flipBone", text = "Flip Bone", toggle = True)

    box = layout.box()
    row = box.row()
    row.alignment = 'CENTER'
    row.label(text = "Arms IK:")
    row.prop(rig, "Arm_IK_Right", text = "Right", slider = True)
    row.prop(rig, "Arm_IK_Left", text = "Left", slider = True)

    row = box.row()
    row.alignment = 'CENTER'
    row.label(text = "Legs IK:")
    row.prop(rig, "Leg_IK_Right", text = "Right", slider = True)
    row.prop(rig, "Leg_IK_Left", text = "Left", slider = True)

    box = layout.box()
    row = box.row()
    row.prop(rig, "HeadWorld", toggle = True)
    row = box.row()
    row.label(text="Arm World:")
    row.prop(rig, "ArmWorld_r", text = "Right", toggle = True)
    row.prop(rig, "ArmWorld_l", text = "Left" ,toggle = True)
    row = box.row()
    row.label(text="Wrist World:")
    row.prop(rig, "WristWorld_r", text = "Right", toggle = True)
    row.prop(rig, "WristWorld_l", text = "Left" ,toggle = True)

    split = box.split()
    col = split.column()
    col.prop(rig, "FullRiggedFace", text = "Face Full Rigged" , toggle = True)
    if rig.get("Finger") == True:
        col.prop(rig, "FingerPlus", text = "Finger Full Rigged", toggle = True)

        
    box = layout.box()
    split = box.split()
    col = split.column()
    col.label(text = "Eyes")
    col.prop(rig, "EyesTracker", toggle = True)
    col.label(text = "Smart Movement")
    col.prop(rig, "SmartMovement", toggle = True)
    if rig.get("SmartMovement"):
        if rig.get("Facial") == "two":   
            split = box.split()
            col = split.column()
            row = box.row()
            col.prop(rig, "EyesFollow", text = "Smart Eyelids", toggle = True)
            row.prop(rig, "SmartMovement_HeadDeformations", slider = True)
        row = box.row()
        row.prop(rig, "SmartMovement_Arm", slider = True)
        row = box.row()
        row.prop(rig, "SmartMovement_Leg", slider = True)
        row = box.row()
        row.prop(rig, "SmartMovement_Waist", slider = True)

def drawriganimating(self, context):
    rig = context.active_object
    scn = context.scene
    layout = self.layout
    #   easy parent
    box = layout.box()
    box.label(text = "Advanced rig options:")
    box.label(text = "Quick Parent:")
    col = box.column()
    cl = col.row()
    cl.prop(scn, "boneName", icon = "BONE_DATA", text = "")
    cl.prop(rig, "ParentBones", text = "")
    cl = col.row()
    cl.scale_y = 1.25
    cl.operator("parent.rig", text = "Parent object to rig")
    
    minecraftExtraProperties.drawrigextra(self, context)

def drawriguisetting(self, context):
    layout = self.layout
    rig = context.active_object         

    box = layout.box()
    row1 = box.row()
    row2 = box.row()

    row1.label(text = "Control panel position:")
    row2.prop(rig, "CPpos", expand = True)

    box = layout.box()
    row1 = box.row()
    row2 = box.row()
    
    row1.label(text = "Control panel parent:")
    row2.prop(rig, "UIParent", expand = True)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def menu_func_mc(self, context):
    pcoll = preview_collections["main"]
    ken_icon = pcoll["Minecraft"]
    addon_prefs = addonPreferences.getAddonPreferences(context)
    if addon_prefs.registered_name:
        if any(item.registered_name in AnimeProperties.registered_name for item in addon_prefs.registered_name):
            self.layout.separator()
            self.layout.menu("MC_RIG_Menu", text = "KEN MC RIG Presnt", icon_value = ken_icon.icon_id)

class MC_RIG_Menu(bpy.types.Menu):
    bl_idname = "MC_RIG_Menu"
    bl_label = "Append ThomasRig KEN Remastered"

    def draw(self, context):
        script_file = os.path.realpath(__file__)
        script_file = os.path.dirname(script_file)
        layout = self.layout

        split = layout.split()
        col = split.column()

        pcoll = preview_collections["main"]
        ken_icon = pcoll["Minecraft"]
        ken02_icon = pcoll["Minecraft_02"]

        col.operator("append.thomasrigkenremastereddefault", icon_value = ken_icon.icon_id)
        col.operator("append.thomasrigkenremasteredfemale", icon_value = ken02_icon.icon_id)
        col.operator("append.thomasrigkenlayout", icon_value = ken02_icon.icon_id)

preview_collections = {}

classes = (
            MC_RIG_Menu,
          )

def register(): 
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
 
    icon = icons.icons("icons")
    pcoll = icon.getColl()
    icon.load(pcoll)
    preview_collections["main"] = pcoll

    bpy.types.VIEW3D_MT_add.append(menu_func_mc)
  
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.PoseBone.extra_prop
    bpy.types.VIEW3D_MT_add.remove(menu_func_mc)