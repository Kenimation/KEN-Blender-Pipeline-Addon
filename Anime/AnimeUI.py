import bpy
import os

from . import AnimeProperties, AnimeExtraProperties
from ..AssetsUI import assetsDraw, assetsDefs
from .. import addonPreferences, icons


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def draw_ken_animerig(self, context, obj):
    addon_prefs = addonPreferences.getAddonPreferences(context)
    scene = context.scene
    rig = context.active_object
    if obj.RIG_ID == AnimeProperties.kenriglist[2]:
        if obj.mode == 'OBJECT':
            if obj.type == 'ARMATURE':
                if rig.Sub_ID in AnimeExtraProperties.AdditionList:
                    rig_class = "myanimerigAddition"
                    rig_get_class = scene.myanimerigAddition
                else:
                    rig_class = "myanimerig"
                    rig_get_class = scene.myanimerig

        elif obj.mode == 'POSE':
            if rig.Sub_ID in AnimeExtraProperties.AdditionList:
                rig_class = "myanimerigposeAddition"
                rig_get_class = scene.myanimerigposeAddition
            else:
                rig_class = "myanimerigpose"
                rig_get_class = scene.myanimerigpose

        if scene.ken_rig == True:
            layout = self.layout
            box = layout.box()
            row = box.row()
            row.label(text = "KEN Anime Rig v1.0 (Female)", icon = "OUTLINER_OB_ARMATURE")
            row.prop(scene, "object_properties", icon = "ARMATURE_DATA", text = "")
            for item in addon_prefs.registered_name:
                if  item.registered_name == AnimeProperties.registered_name[1]:
                    if rig.mode == 'EDIT':
                        assetsDraw.drawbone_properties(box, context, obj)
                    else:
                        row = box.row()
                        row.prop(rig, "AntiLag", text = "Subdivision", icon = 'MOD_SUBSURF')
                        row.prop(rig, "SmoothShade", text = "Smooth Shade", icon = 'MESH_DATA')
                        if rig.MeshSelect == True:
                            icon = "RESTRICT_SELECT_OFF"
                        else:
                            icon = "RESTRICT_SELECT_ON"
                        row.prop(rig, "MeshSelect", text = "", icon = icon, emboss = False)
                        row = box.row()
                        row.prop(rig, "LineArt", icon = 'MOD_LINEART')
                        row.prop(rig, "LineArtMesh", text = "", icon = "HIDE_OFF")
                        if rig.LineArt == True:
                            row = box.row()
                            row.label(text = "Bake LineArt")
                            row = box.row()
                            row.operator("object.lineart_bake_strokes_all", text="Bake All Lineart")
                            row.operator("object.lineart_clear_all", text="Clear All Lineart")
                        row = box.row()
                        row.prop(scene, rig_class, expand = True)
                        if rig_get_class == "one":
                            drawrigdesign(self, context)
                        if rig_get_class == "two":
                            drawrigmaterial(self, context)
                        if rig_get_class == "three":
                            if rig_class != "myanimerigAddition":
                                drawrigposing(self, context)
                            else:
                                AnimeExtraProperties.drawrigAddition(self, context)
                        if rig_get_class == "four":
                            AnimeExtraProperties.drawrigAddition(self, context)
                else:
                    layout = self.layout
                    box = layout.box()
                    row = box.row()
                    row.label(text = "Registered name is not available to edit the rig.")
    
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def drawrimlight(list, node):
    row = list.row()
    row.label(text = "Rim Light:")
    row = list.row()
    row.prop(node['Rim Light'], "default_value", text = "Strength", slider = True)
    row = list.row()
    row.prop(node['Rim Light Color'], "default_value", text = "")
    row = list.row()
    row.prop(node['Rim Light Shadow'], "default_value", text = "Rim Light Shadow", slider = True)
    row = list.row()
    row.prop(node['Thickness'], "default_value", text = "Thickness")
    row.prop(node['Sample Radius'], "default_value", text = "Radius")

def drawshadow(list, node):
    row = list.row()
    row.label(text = "Shadow:")
    row = list.row()
    row.prop(node['Shadow Position'], "default_value", text = "Shadow Position", slider = True)
    row = list.row()
    row.prop(node['Cast Shadow'], "default_value", text = "Cast Shadow", slider = True)
    row = list.row()
    try:
        row.prop(node['Cast Shadow Sub'], "default_value", text = "Cast Shadow Sub", slider = True)
        row = list.row()
    except:
        pass
    row.prop(node['Smooth Shadow'], "default_value", text = "Smooth Shadow", slider = True)

def drwatexture_path(list, mat, img, text):
    texture = mat.node_tree.nodes[img].image
    row = list.row(align = True)  
    row.label(text = text)
    if texture:
        col = row.column()
        col.operator("pack.img" , text="", icon="UGLYPACKAGE" if assetsDefs.is_packed(texture) else "PACKAGE").id_name = texture.name 
        col = row.column()
        if assetsDefs.is_packed(texture) == False:
            col.enabled = False
        col.prop(texture, "filepath", text="")
        col = row.column()
        if assetsDefs.is_packed(texture) == False:
            col.enabled = False
        col.operator("reload.img", text = "", icon = "FILE_REFRESH").id_name = texture.name 

        # skin library
        row = list.row(align = True)
        if assetsDefs.is_packed(texture) == False:
            row.enabled = False
        else:
            row.operator("useskin.lib", text = "library")
            row.operator("openskin.lib", text = "", icon = "FILE_FOLDER")
    else:
        openimage = row.operator("open.image", icon = "FILE_FOLDER", text = "Open Image")
        openimage.img = img
        openimage.mat = mat.name

def drwatexture(list, material_obj, slot):
    mat = material_obj.material_slots[slot].material
    drwatexture_path(list, mat, 'Base Color', text = "Base:")
    drwatexture_path(list, mat, 'Shadow Color', text = "Shadow:")
    drwatexture_path(list, mat, 'Base lim', text = "lim:")

def drawrigdesign(self, context):
    layout = self.layout
    scene = context.scene
    rig = context.active_object
    DesignClasses = "DesignClasses"

    box = layout.box()
    row = box.row()
    row.label(text = "Character Height:" + str(round(rig.dimensions[2]*100/rig.RigScale, 2))+"cm x "+ str(round(rig.RigScale, 2)))
    row = box.row()
    row.prop(rig, "RigScale", slider = True)
    row = box.row()
    row.label(text = "Sub_ID(Required)")
    row = box.row()
    col = row.column()
    if rig.Sub_ID_Lock == True:
        icon = "LOCKED"
        col.enabled = False
    else:
        icon = "UNLOCKED"
        col.enabled = True
    col.prop(rig, "Sub_ID", text = "")
    row.prop(rig, "Sub_ID_Lock", text = "", icon = icon, emboss = False)
    row = box.row()
    row.label(text = "Character Design:")
    row = box.row()
    row.prop(rig, DesignClasses, expand = True)
    if rig.get(DesignClasses) == 0:
        row = box.row()
        row.label(text = "Mesh Scale:")
        if rig.FacialDesign == True:
                icon = "DOWNARROW_HLT"
        else:
            icon = "RIGHTARROW"
        menu = box.row()
        menu.prop(rig, "FacialDesign", text = "Facial", icon = icon, emboss=False)
        if rig.FacialDesign == True:
            faciallist = box.box()
            row = faciallist.row()
            row.label(text = "Facial:")
            row = faciallist.row()
            row.prop(rig, "Facial", expand = True)
            if rig.Facial == 'two':
                material_obj = rig.children[0]
                Blush = material_obj.material_slots[5].material.node_tree.nodes['Blush'].inputs
                faciallist = box.box()
                row = faciallist.row()
                row.prop(rig, "Blush", toggle = True)
                row.prop(Blush['Color'], "default_value", text = "")
                row = faciallist.row()
                row.label(text = "Eyebrows:")
                row = faciallist.row()
                row.prop(rig, "EyebrowsThickness", slider = True)
                row = faciallist.row()
                row.prop(rig, "EyebrowsWidth", slider = True)
                row = faciallist.row()
                row.prop(rig, "EyebrowsPos", slider = True)
                row = faciallist.row()
                row.label(text = "Eyelash Type")
                row = faciallist.row()
                row.prop(rig, "EyelashType")
                row = faciallist.row()
                row.label(text = "Nose Type")
                row = faciallist.row()
                row.prop(rig, "NoseType")
                row = faciallist.row()
                row.label(text = "Teeth")
                row = faciallist.row()
                row.prop(rig, "Teeth", expand = True)
        if rig.MeshDesign == True:
                icon = "DOWNARROW_HLT"
        else:
            icon = "RIGHTARROW"
        menu = box.row()
        menu.prop(rig, "MeshDesign", text = "Body", icon = icon, emboss=False)
        if rig.MeshDesign == True:
            bodylist = box.box()
            row = bodylist.row()
            row.label(text = "Head:")
            row = bodylist.row()
            row.prop(rig, "HeadSize", slider = True)
            row = bodylist.row()
            row.label(text = "Body:")
            row = bodylist.row()
            row.prop(rig, "BodySize", slider = True)
            row = bodylist.row()
            row.prop(rig, "BodyWidth3", slider = True)
            row = bodylist.row()
            row.prop(rig, "BodyWidth2", slider = True)
            row = bodylist.row()
            row.prop(rig, "BodyWidth1", slider = True)
            row = bodylist.row()
            row.prop(rig, "BreastSize", slider = True)
            row = bodylist.row()
            row.prop(rig, "ButtSize", slider = True)
            row = bodylist.row()
            row.label(text = "Arm:")
            row = bodylist.row()
            row.prop(rig, "ArmSize", slider = True)
            row = bodylist.row()
            row.prop(rig, "ShoulderWidth", slider = True)
            row = bodylist.row()
            row.label(text = "Leg:")
            row = bodylist.row()
            row.prop(rig, "LegSize", slider = True)
            row = bodylist.row()
            row.prop(rig, "LegWidth", slider = True)
            row = bodylist.row()
            row.prop(rig, "FootSize", slider = True)
            row = bodylist.row()
            row.label(text = "Muscle:")
            row = bodylist.row()
            row.prop(rig, "BodyMuscle", slider = True)
            row = bodylist.row()
            row.prop(rig, "ArmMuscle", slider = True)
            row = bodylist.row()
            row.prop(rig, "LegMuscle", slider = True)
            row = bodylist.row()
            row.label(text = "Finger:")
            row = bodylist.row()
            row.prop(rig, "NailLength", slider = True)
            row = bodylist.row()
            row.prop(rig, "NailSharp", slider = True)
    if rig.get(DesignClasses) == 1:

        mainline = bpy.data.materials['MainLine'].grease_pencil
        pinkline = bpy.data.materials['PinkLine'].grease_pencil
        skinline = bpy.data.materials['SkinLine'].grease_pencil
        row = box.row()
        row.label(text = "LineArt:")
        row = box.row()
        row.prop(mainline, "color", text = "Main Line")
        row.prop(rig, "MainLineArt")
        row = box.row()
        row.prop(pinkline, "color", text = "Pink Line")
        row.prop(rig, "PinkLineArt")
        row = box.row()
        row.prop(skinline, "color", text = "Skin Line")
        row = box.row()
        row.label(text = "Mesh LineArt:")
        row = box.row()
        row.prop(rig, "DetailLine", toggle = True)
        if rig.DetailLine == True:
            row = box.row()
            row.prop(rig, "FingerLine", toggle = True)
            row = box.row()
            row.prop(rig, "HairLine", toggle = True)
            if rig.Sub_ID in AnimeExtraProperties.ArmorList:
                row = box.row()
                row.prop(rig, "ClothLine", toggle = True)
                row = box.row()
                row.prop(rig, "ArmorLine", toggle = True)
        if rig.Facial == 'two':
            row = box.row()
            row.label(text = "Facial LineArt:")
            row = box.row()
            row.prop(rig, "FaceLine", toggle = True)
            row.prop(rig, "FaceLineType")
            row = box.row()
            row.prop(rig, "NoseLine", toggle = True)
            row = box.row()
            row.prop(rig, "EyebrowLine", toggle = True)
            row = box.row()
            row.prop(rig, "LipLine", toggle = True)
            row = box.row()
            row.prop(rig, "MadLine", toggle = True)
            row = box.row()
            row.prop(rig, "DirtLine", toggle = True)
    if rig.get(DesignClasses) == 2:
        row = box.row()
        row.label(text = "Cast Shadow(Turn Off before bake LineArt):")
        row = box.row()
        row.prop(rig, "SubShadow", expand = True)
        if rig.SubShadow == 'two':
            row = box.row()
            row.label(text = "Mesh:")
            row = box.row()
            row.prop(rig, "BodyShadow", toggle = True)
            row = box.row()
            row.prop(rig, "FingerShadow", toggle = True)
            row = box.row()
            row.label(text = "Facial:")
            row = box.row()
            row.label(text = "Nose:")
            row = box.row()
            row.prop(rig, "NoseShadow", expand = True)
            row = box.row()
            row.label(text = "Eye:")
            row = box.row()
            row.prop(rig, "EyeBottomShadow", toggle = True)
            row = box.row()
            row.prop(rig, "EyelidsShadow")
            row = box.row()
            row.prop(rig, "EyelidsHardShadow")
            row = box.row()
            row.prop(rig, "MadShadow")

def drawrigmaterial(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    skin = material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs
    base = material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs
    metal = material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs
    hair = material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs
    eyes = material_obj.material_slots[4].material.node_tree.nodes['Eyes Shader'].inputs

    layout = self.layout
    box = layout.box()
    row = box.row()
    row.label(text = "Shader:")
    row.prop(rig, "HueColorize", text = "", icon = "COLOR")
    row.prop(rig, "AllRimlight", text = "", icon = "LIGHT_AREA")
    row.prop(rig, "AllShadow", text = "", icon = "MOD_MASK")
    if rig.HueColorize == True:
        row = box.row()
        row.label(text = "Colorize:", icon = "COLOR")
        row = box.row()
        row.prop(rig, "MixHue", slider = True)
        row = box.row()
        row.prop(rig, "TintColor", text = "")
        row = box.row()
        row.prop(rig, "Saturation", slider = True)
        row = box.row()
        row.prop(rig, "Lightness", slider = True)
    if rig.AllRimlight == True:
        row = box.row()
        row.label(text = "Rim Light:", icon = "LIGHT_AREA")
        row = box.row()
        row.prop(rig, "Rimlight", slider = True)
        row = box.row()
        row.prop(rig, "RimlightColor", text = "")
        row = box.row()
        row.prop(rig, "RimlightShadow", slider = True)
        row = box.row()
        row.prop(rig, "RimlightThickness")
        row.prop(rig, "RimlightRadius")
    if rig.AllShadow == True:
        row = box.row()
        row.label(text = "Shadow:", icon = "MOD_MASK")
        row = box.row()
        row.prop(rig, "ShadowPosition", slider = True)
        row = box.row()
        row.prop(rig, "CastShadow", slider = True)
        row = box.row()
        row.prop(rig, "SmoothShadow", slider = True)
    menu = box.row()
    if rig.SkinMaterial == True:
        icon = "DOWNARROW_HLT"
    else:
        icon = "RIGHTARROW"
    menu.prop(rig, "SkinMaterial", text = "Skin Shader", icon = icon, emboss=False)
    if rig.SkinMaterial == True:
        skinlist = box.box()
        row = skinlist.row()
        list = skinlist
        node = skin
        row.label(text = "Skin:")
        row = skinlist.row()
        row.prop(skin['Base Skin'], "default_value", text = "")
        row.prop(skin['Skin Shadow'], "default_value", text = "")
        row.prop(skin['Skin Sub Shadow'], "default_value", text = "")
        row = skinlist.row()
        row.label(text = "Highlight:")
        row = skinlist.row()
        row.prop(skin[3], "default_value", text = "Highlight", slider = True)
        row = skinlist.row()
        row.prop(skin['Skin Highlight'], "default_value", text = "")
        row.prop(skin['Skin Deep Highlight'], "default_value", text = "")
        row = skinlist.row()
        row.label(text = "Eyeballs:")
        row = skinlist.row()
        row.prop(skin['Eyeball Color'], "default_value", text = "")
        row.prop(skin['Eyeball Shadow'], "default_value", text = "")
        row.prop(skin['Eyeball Sub Shadow'], "default_value", text = "")
        row = skinlist.row()
        row.label(text = "Lip:")
        row = skinlist.row()
        row.prop(skin['Top Lip'], "default_value", text = "Top", slider = True)
        row = skinlist.row()
        row.prop(skin['Bottom Lip'], "default_value", text = "Bottom", slider = True)
        row = skinlist.row()
        row.prop(skin['Lip Color'], "default_value", text = "")
        row.prop(skin['Lip  Shadow'], "default_value", text = "")
        row.prop(skin['Lip Sub Shadow'], "default_value", text = "")
        row = skinlist.row()
        row.label(text = "Tooth:")
        row = skinlist.row()
        row.prop(skin['Tooth Color'], "default_value", text = "")
        row.prop(skin['Tooth Shadow'], "default_value", text = "")
        row = skinlist.row()
        row.label(text = "Tongue:")
        row = skinlist.row()
        row.prop(skin['Tongue Color'], "default_value", text = "")
        row.prop(skin['Tongue Shadow'], "default_value", text = "")
        row = skinlist.row()
        row.label(text = "Blood:")
        row = skinlist.row()
        row.prop(skin['Blood Color'], "default_value", text = "")
        row.prop(skin['Blood Shadow'], "default_value", text = "")
        row = skinlist.row()
        row.label(text = "Pink:")
        row = skinlist.row()
        row.prop(skin['Pink Color'], "default_value", text = "")
        row.prop(skin['Pink Shadow'], "default_value", text = "")
        row = skinlist.row()
        row.label(text = "Nail:")
        row = skinlist.row()
        row.prop(skin['Nail'], "default_value", text = "Nail", slider = True)
        drawrimlight(list, node)
        drawshadow(list, node)

    menu = box.row()
    if rig.BaseMaterial == True:
        icon = "DOWNARROW_HLT"
    else:
        icon = "RIGHTARROW"
    menu.prop(rig, "BaseMaterial", text = "Base Shader", icon = icon, emboss=False)
    if rig.BaseMaterial == True:
        baselist = box.box()
        row = baselist.row()
        list = baselist
        node = base
        row.label(text = "Base Color:")
        slot = 1
        drwatexture(list, material_obj, slot)
        row = baselist.row()
        row.prop(base['Sub Shadow'], "default_value", text = "Sub Shadow", slider = True)
        drawrimlight(list, node)
        drawshadow(list, node)
    menu = box.row()
    if rig.MetalMaterial == True:
        icon = "DOWNARROW_HLT"
    else:
        icon = "RIGHTARROW"
    menu.prop(rig, "MetalMaterial", text = "Metal Shader", icon = icon, emboss=False)
    if rig.MetalMaterial == True:
        metallist = box.box()
        row = metallist.row()
        list = metallist
        node = metal
        slot = 2
        row.label(text = "Base Color:")
        drwatexture(list, material_obj, slot)
        row = metallist.row()
        row.label(text = "Highlight:")
        row = metallist.row()
        row.prop(metal['Highlight Color'], "default_value", text = "")
        row.prop(metal['Highlight Shadow'], "default_value", text = "")
        row = metallist.row()
        row.prop(metal[6], "default_value", text = "Highlight Shadow", slider = True)
        row = metallist.row()
        row.label(text = "Material:")
        row = metallist.row()
        row.prop(metal['Specular'], "default_value", text = "Specular", slider = True)
        row = metallist.row()
        row.prop(metal['Roughness'], "default_value", text = "Roughness", slider = True)
        row = metallist.row()
        row.prop(metal['Texture'], "default_value", text = "Texture", slider = True)
        drawrimlight(list, node)
        drawshadow(list, node)
    menu = box.row()
    if rig.HairMaterial == True:
        icon = "DOWNARROW_HLT"
    else:
        icon = "RIGHTARROW"
    menu.prop(rig, "HairMaterial", text = "Hair Shader", icon = icon, emboss=False)
    if rig.HairMaterial == True:
        hairlist = box.box()
        row = hairlist.row()
        list = hairlist
        node = hair
        row.label(text = "Hair:")
        mat = material_obj.material_slots[3].material
        drwatexture_path(list, mat, 'Hair lim', text = "Hair lim:")
        row = hairlist.row()
        row.label(text = "Hair Color:")
        row = hairlist.row()
        row.prop(hair['Hair Color'], "default_value", text = "")
        row.prop(hair['Hair Shadow'], "default_value", text = "")
        row.prop(hair['Hair Sub Shadow'], "default_value", text = "")
        row = hairlist.row()
        row.label(text = "Highlight:")
        row = hairlist.row()
        row.prop(hair['Highlight Color'], "default_value", text = "")
        row.prop(hair['Highlight Deep'], "default_value", text = "")
        row = hairlist.row()
        row.prop(hair['Highlight'], "default_value", text = "Highlight", slider = True)
        row = hairlist.row()
        row.prop(hair['Highlight Position'], "default_value", text = "Highlight Position", slider = True)
        drawrimlight(list, node)
        drawshadow(list, node)
    menu = box.row()
    if rig.EyesMaterial == True:
        icon = "DOWNARROW_HLT"
    else:
        icon = "RIGHTARROW"
    menu.prop(rig, "EyesMaterial", text = "Eye Shader", icon = icon, emboss=False)
    if rig.EyesMaterial == True:
        eyelist = box.box()
        row = eyelist.row()
        row.label(text = "Eyes:")
        row = eyelist.row()
        row.prop(eyes['Base Color'], "default_value", text = "")
        row.prop(eyes['Highlight Color'], "default_value", text = "")
        row.prop(eyes['Deep Color'], "default_value", text = "")
        row = eyelist.row()
        row.prop(eyes['Outline Color'], "default_value", text = "Outline")
        row = eyelist.row()
        row.prop(eyes['Lens Color'], "default_value", text = "Lens")
        row = eyelist.row()
        row.prop(eyes['Pupils Size'], "default_value", text = "Pupil Size", slider = True)
        row = eyelist.row()
        row.label(text = "Sparkle:")
        row = eyelist.row()
        row.prop(eyes['Sparkle'], "default_value", text = "Sparkle", slider = True)
        row = eyelist.row()
        row.prop(eyes['Sparkle Color'], "default_value", text = "")
        row = eyelist.row()
        row.prop(eyes['Sparkle Emission Strength'], "default_value", text = "Emission")
        row = eyelist.row()
        row.prop(eyes['Sparkle Mirror X'], "default_value", text = "Mirror X", slider = True)
        row = eyelist.row()
        row.prop(eyes['Sparkle Wave'], "default_value", text = "Wave", slider = True)
        row = eyelist.row()
        row.prop(eyes['Wave Seed'], "default_value", text = "Wave Seed")
        row = eyelist.row()
        row.label(text = "Texture Type:")
        row = eyelist.row()
        row.prop(rig, "AnimeEyeType", expand = True)
        if rig.AnimeEyeType != "one":
            row = eyelist.row()
            row.label(text = "Texture:")
            row = eyelist.row()
            row.prop(eyes['Texture Strength'], "default_value", text = "Texture Strength", slider = True)
            row = eyelist.row()
            row.prop(eyes['Texture Color'], "default_value", text = "")
            row = eyelist.row()
            row.prop(eyes['Seed'], "default_value", text = "Seed")
        row = eyelist.row()
        row.label(text = "Shadow:")
        row = eyelist.row()
        row.prop(eyes['Shadow'], "default_value", text = "Shadow", slider = True)

def drawrigposing(self, context):
    layout = self.layout
    rig = context.active_object
    box = layout.box().column()
    scene =  context.scene
    box.prop(rig, "show_in_front", icon = "HIDE_OFF", text = "Show bones in front")
    box.prop(rig, "flipBone", text = "Flip Bone", toggle = True)
    row = box.row()
    row.prop(rig, "MainBone", text = "Main Bone", toggle = True)
    row.prop(rig, "HeadBone", text = "Head Bone", toggle = True)


    box = layout.box()
    row = box.row()
    row.label(text = "Arms IK:")
    row = box.row()
    row.prop(rig, "Arm_IK_Right", text = "Right", slider = True)
    row.prop(rig, "Arm_IK_Left", text = "Left", slider = True)
    row = box.row()
    row.prop(rig, "Arm_Stretch", slider = True)

    row = box.row()
    row.label(text = "Legs IK:")
    row = box.row()
    row.prop(rig, "Leg_IK_Right", text = "Right", slider = True)
    row.prop(rig, "Leg_IK_Left", text = "Left", slider = True)
    row = box.row()
    row.prop(rig, "Leg_Stretch", slider = True)

    row = box.row()
    row.label(text = "Bone World:")
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
    row.label(text = "Head:")
    row = box.row()
    row.prop(rig, "HeadFFD", toggle = True)
    row = box.row()
    row.label(text = "Facial:")
    row = box.row()
    row.prop(rig, "Full_Rigged_Face", toggle = True)
    row = box.row()
    row.prop(rig, "SmartEye", toggle = True)
    row = box.row()
    row.label(text = "Hair:")
    row = box.row()
    row.prop(rig, "HairControl", toggle = True)
    row = box.row()
    row.label(text = "Quick Parent:")
    col = row.column()
    cl = col.row()
    cl.prop(scene, "boneName", icon = "BONE_DATA", text = "")
    cl.prop(rig, "ParentBones", text = "")
    row = box.row()
    row.operator("parent.rig", text = "Parent object to rig")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                      classes 
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def menu_func_anime(self, context):
    pcoll = preview_collections["main"]
    ken_icon = pcoll["Dual"]
    addon_prefs = addonPreferences.getAddonPreferences(context)
    if addon_prefs.registered_name:
        if all(item.registered_name in AnimeProperties.registered_name for item in addon_prefs.registered_name):
            self.layout.menu("Anime_RIG_Menu", text = "KEN Anime RIG Presnt", icon_value = ken_icon.icon_id)

class Anime_RIG_Menu(bpy.types.Menu):
    bl_idname = "Anime_RIG_Menu"
    bl_label = "Append KEN Anime Rig"

    def draw(self, context):
        script_file = os.path.realpath(__file__)
        script_file = os.path.dirname(script_file)

        addon_prefs = addonPreferences.getAddonPreferences(context)
        for item in addon_prefs.registered_name:
            if  item.registered_name == AnimeProperties.registered_name[1]:

                layout = self.layout

                split = layout.split()
                col = split.column()

                pcoll = preview_collections["main"]
                ken_icon = pcoll["Dual"]

                col.operator("append.kenanimefemale", icon_value = ken_icon.icon_id)

preview_collections = {}

classes = (
            Anime_RIG_Menu,
          )

def register(): 
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
 
    icon = icons.icons("icons")
    pcoll = icon.getColl()
    icon.load(pcoll)
    preview_collections["main"] = pcoll

    bpy.types.VIEW3D_MT_add.append(menu_func_anime)
  
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.PoseBone.extra_prop
    bpy.types.VIEW3D_MT_add.remove(menu_func_anime)