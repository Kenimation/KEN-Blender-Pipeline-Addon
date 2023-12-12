import bpy
import os
from ..AssetsUI import assetsDefs
from .. import addonPreferences

def update_Sub_ID(self, context):
    rig = context.active_object

    text = rig.children[0]
    text.data.body = rig.Sub_ID

    if rig.Sub_ID != "Character - Default":
        rig.name = rig.Sub_ID + " Anime Rig"
    else:
        rig.name = "KEN Anime Female Rig"

    for collection in bpy.data.collections:
            if rig.name in collection.objects:
                parent_collection = collection
                break
    if parent_collection is not None:
        if rig.Sub_ID != "Character - Default":
            parent_collection.name = rig.Sub_ID + " Anime Rig"
        else:
            parent_collection.name = "KEN Anime Female Rig"

def update_MeshSelect(self, context):
    rig = context.active_object
    for collection in bpy.data.collections:
            if rig.name in collection.objects:
                parent_collection = collection
                break

    if parent_collection is not None:
        for child_collection in parent_collection.children:
            if child_collection.name.split(".", 1)[0] == "Mesh":
                if self.MeshSelect == True:
                    child_collection.hide_select = False
                if self.MeshSelect == False:
                    child_collection.hide_select = True
                break

def update_LineArt(self, context):
    rig = context.active_object
    for collection in bpy.data.collections:
            if rig.name in collection.objects:
                parent_collection = collection
                break

    if parent_collection is not None:
        for child_collection in parent_collection.children:
            if child_collection.name.split(".", 1)[0] == "LineArt":
                if self.LineArt == False:
                    child_collection.hide_viewport = True
                    child_collection.hide_render = True
                if self.LineArt == True:
                    rig.LineArtMesh = True
                    child_collection.hide_viewport = False
                    child_collection.hide_render = False
                break

def update_LineArtMesh(self, context):
    rig = context.active_object
    for collection in bpy.data.collections:
            if rig.name in collection.objects:
                parent_collection = collection
                break

    if parent_collection is not None:
        for child_collection in parent_collection.children:
            if child_collection.name.split(".", 1)[0] == "LineArt_Mesh":
                if self.LineArtMesh == False:
                    child_collection.hide_viewport = True
                    child_collection.hide_render = True
                if self.LineArtMesh == True:
                    child_collection.hide_viewport = False
                    child_collection.hide_render = False
                break

def update_DetailLine(self, context):
    rig = context.active_object
    for collection in bpy.data.collections:
            if rig.name in collection.objects:
                parent_collection = collection
                break

    if parent_collection is not None:
        for child_collection in parent_collection.children:
            if child_collection.name.split(".", 1)[0] == "LineArt_Mesh":
                for mesh_collection in child_collection.children:
                    if mesh_collection.name.split(".", 1)[0] == "Detail_Line":
                        if self.DetailLine == False:
                            mesh_collection.hide_viewport = True
                            mesh_collection.hide_render = True
                        if self.DetailLine == True:
                            mesh_collection.hide_viewport = False
                            mesh_collection.hide_render = False
                        break

def update_MixHue(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('MixHue')
    inputs = 'Mix'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[4].material.node_tree.nodes['Eyes Shader'].inputs[inputs].default_value = value

def update_TintColor(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('TintColor')
    inputs = 'Tint Color'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[4].material.node_tree.nodes['Eyes Shader'].inputs[inputs].default_value = value

def update_Saturation(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('Saturation')
    inputs = 'Saturation'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[4].material.node_tree.nodes['Eyes Shader'].inputs[inputs].default_value = value

def update_Lightness(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('Lightness')
    inputs = 'Lightness'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_Rimlight(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('Rimlight')
    inputs = 'Rim Light'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_RimlightColor(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('RimlightColor')
    inputs = 'Rim Light Color'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_RimlightShadow(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('RimlightShadow')
    inputs = 'Rim Light Shadow'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_RimlightThickness(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('RimlightThickness')
    inputs = 'Thickness'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_RimlightRadius(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('RimlightRadius')
    inputs = 'Sample Radius'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_ShadowPosition(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('ShadowPosition')
    inputs = 'Shadow Position'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_CastShadow(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('CastShadow')
    inputs = 'Cast Shadow'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_SmoothShadow(self, context):
    rig = context.active_object
    material_obj = rig.children[0]
    value = rig.get('SmoothShadow')
    inputs = 'Smooth Shadow'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_rig_scale(self,context):
    rig = context.active_object
    value = rig.get('RigScale')
    value = float(value)
    scale = [value, value, value]
    rig.pose.bones["Rig.Scale"].scale = scale
    rig.pose.bones["Root"].custom_shape_scale_xyz = scale

def write_rig_scale(self, context):
    addon_prefs = addonPreferences.getAddonPreferences(context)
    text_file = assetsDefs.getPath("preferencesSettings.cfg")
    with open(text_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        data[15] = str(addon_prefs.rig_scale) + "\n"

    # and write everything back
    with open(text_file, 'w') as file:
        file.writelines(data)