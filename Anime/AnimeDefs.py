import bpy
import os
import re
Mesh = ["Mesh", "Mesh.001", "Mesh.002", "Mesh.003", "Mesh.004", "Mesh.005"]
Facials = ["Facials", "Facials.001", "Facials.002", "Facials.003", "Facials.004", "Facials.005"]
LineArt = ["LineArt", "LineArt.001", "LineArt.002", "LineArt.003", "LineArt.004", "LineArt.005"]
LineArtMesh = ["LineArt.Mesh", "LineArt.Mesh.001", "LineArt.Mesh.002", "LineArt.Mesh.003", "LineArt.Mesh.004", "LineArt.Mesh.005"]
FacialsLine = ["Facials.Line", "Facials.Line.001", "Facials.Line.002", "Facials.Line.003", "Facials.Line.004", "Facials.Line.005"]
DetailLine = ["Detail.Line", "Detail.Line.001", "Detail.Line.002", "Detail.Line.003", "Detail.Line.004", "Detail.Line.005"]

def update_Sub_ID(self, context):
    rig = bpy.context.active_object

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

def update_Facial(self, context):
    rig = bpy.context.active_object
    for collection in bpy.data.collections:
            if rig.name in collection.objects:
                parent_collection = collection
                break

    if parent_collection is not None:
        for child_collection in parent_collection.children:
            if child_collection.name in Mesh:
                for face_collection in child_collection.children:
                    if face_collection.name in Facials:
                        if self.Facial == 'one':
                            face_collection.hide_viewport = True
                            face_collection.hide_render = True
                        if self.Facial == 'two':
                            face_collection.hide_viewport = False
                            face_collection.hide_render = False
                        break

    if parent_collection is not None:
        for child_collection in parent_collection.children:
            if child_collection.name in LineArtMesh:
                for mesh_collection in child_collection.children:
                    if mesh_collection.name in FacialsLine:
                        if self.Facial == 'one':
                            mesh_collection.hide_viewport = True
                            mesh_collection.hide_render = True
                        if self.Facial == 'two':
                            mesh_collection.hide_viewport = False
                            mesh_collection.hide_render = False
                        break

def update_LineArt(self, context):
    rig = bpy.context.active_object
    for collection in bpy.data.collections:
            if rig.name in collection.objects:
                parent_collection = collection
                break

    if parent_collection is not None:
        for child_collection in parent_collection.children:
            if child_collection.name in LineArt:
                if self.LineArt == False:
                    child_collection.hide_viewport = True
                    child_collection.hide_render = True
                if self.LineArt == True:
                    rig.LineArtMesh = True
                    child_collection.hide_viewport = False
                    child_collection.hide_render = False
                break

def update_LineArtMesh(self, context):
    rig = bpy.context.active_object
    for collection in bpy.data.collections:
            if rig.name in collection.objects:
                parent_collection = collection
                break

    if parent_collection is not None:
        for child_collection in parent_collection.children:
            if child_collection.name in LineArtMesh:
                if self.LineArtMesh == False:
                    child_collection.hide_viewport = True
                    child_collection.hide_render = True
                if self.LineArtMesh == True:
                    child_collection.hide_viewport = False
                    child_collection.hide_render = False
                break

def update_DetailLine(self, context):
    rig = bpy.context.active_object
    for collection in bpy.data.collections:
            if rig.name in collection.objects:
                parent_collection = collection
                break

    if parent_collection is not None:
        for child_collection in parent_collection.children:
            if child_collection.name in LineArtMesh:
                for mesh_collection in child_collection.children:
                    if mesh_collection.name in DetailLine:
                        if mesh_collection.name in DetailLine:
                            if self.DetailLine == False:
                                mesh_collection.hide_viewport = True
                                mesh_collection.hide_render = True
                            if self.DetailLine == True:
                                mesh_collection.hide_viewport = False
                                mesh_collection.hide_render = False
                            break

def update_MixHue(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('MixHue')
    inputs = 'Mix'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[4].material.node_tree.nodes['Eyes Shader'].inputs[inputs].default_value = value

def update_TintColor(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('TintColor')
    inputs = 'Tint Color'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[4].material.node_tree.nodes['Eyes Shader'].inputs[inputs].default_value = value

def update_Saturation(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('Saturation')
    inputs = 'Saturation'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[4].material.node_tree.nodes['Eyes Shader'].inputs[inputs].default_value = value

def update_Lightness(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('Lightness')
    inputs = 'Lightness'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_Rimlight(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('Rimlight')
    inputs = 'Rim Light'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_RimlightColor(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('RimlightColor')
    inputs = 'Rim Light Color'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_RimlightShadow(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('RimlightShadow')
    inputs = 'Rim Light Shadow'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_RimlightThickness(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('RimlightThickness')
    inputs = 'Thickness'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_RimlightRadius(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('RimlightRadius')
    inputs = 'Sample Radius'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_ShadowPosition(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('ShadowPosition')
    inputs = 'Shadow Position'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_CastShadow(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('CastShadow')
    inputs = 'Cast Shadow'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_SmoothShadow(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('SmoothShadow')
    inputs = 'Smooth Shadow'
    material_obj.material_slots[0].material.node_tree.nodes['Skin Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[1].material.node_tree.nodes['Base Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Metal Shader'].inputs[inputs].default_value = value
    material_obj.material_slots[3].material.node_tree.nodes['Hair Shader'].inputs[inputs].default_value = value

def update_ParentBones(self, context):
    scn = context.scene
    rig = context.object
    scn.boneName = rig.ParentBones