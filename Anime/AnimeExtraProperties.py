import bpy
from bpy.props import (BoolProperty,
                       FloatProperty,
                       EnumProperty,
                       StringProperty,
                       IntProperty,
                       FloatVectorProperty,
                       )
import os
from . import AnimeDefs

Mesh = ["Mesh", "Mesh.001", "Mesh.002", "Mesh.003", "Mesh.004", "Mesh.005"]
Asset = ["Asset", "Asset.001", "Asset.002", "Asset.003", "Asset.004", "Asset.005"]
Cloth = ["Cloth", "Cloth.001", "Cloth.002", "Cloth.003", "Cloth.004", "Cloth.005"]
Facials = ["Facials", "Facials.001", "Facials.002", "Facials.003", "Facials.004", "Facials.005"]
LineArt = ["LineArt", "LineArt.001", "LineArt.002", "LineArt.003", "LineArt.004", "LineArt.005"]
LineArtMesh = ["LineArt.Mesh", "LineArt.Mesh.001", "LineArt.Mesh.002", "LineArt.Mesh.003", "LineArt.Mesh.004", "LineArt.Mesh.005"]
FacialsLine = ["Facials.Line", "Facials.Line.001", "Facials.Line.002", "Facials.Line.003", "Facials.Line.004", "Facials.Line.005"]
DetailLine = ["Detail.Line", "Detail.Line.001", "Detail.Line.002", "Detail.Line.003", "Detail.Line.004", "Detail.Line.005"]
AdditionList = ['Rossweisse', 'Warrior']


def update_Simulation(self, context):
    rig = bpy.context.active_object
    for collection in bpy.data.collections:
            if rig.name in collection.objects:
                parent_collection = collection
                break

    if parent_collection is not None:
        for child_collection in parent_collection.children:
            if child_collection.name in Mesh:
                for mesh_collection in child_collection.children:
                    if mesh_collection.name in Asset:
                        for detail_collection in mesh_collection.children:
                            if detail_collection.name in Cloth:
                                for obj in detail_collection.objects:
                                    if self.ShowSimulation == True:
                                        obj.modifiers["Cloth"].show_viewport = True
                                        obj.modifiers["Cloth"].show_render = True
                                    elif self.ShowSimulation == False:
                                        obj.modifiers["Cloth"].show_viewport = False
                                        obj.modifiers["Cloth"].show_render = False
                                    if self.SimulationCollision == True:
                                        obj.modifiers["Cloth"].collision_settings.use_collision = True
                                    elif self.SimulationCollision == False:
                                        obj.modifiers["Cloth"].collision_settings.use_collision = False
                                    if self.SimulationSelfCollision == True:
                                        obj.modifiers["Cloth"].collision_settings.use_self_collision = True
                                    elif self.SimulationSelfCollision == False:
                                        obj.modifiers["Cloth"].collision_settings.use_self_collision = False
                                    obj.modifiers["Cloth"].point_cache.frame_start = self.SimulationStart
                                    obj.modifiers["Cloth"].point_cache.frame_end = self.SimulationEnd
                                    obj.modifiers["Cloth"].settings.quality = self.SimulationQuality
                                    obj.modifiers["Cloth"].settings.time_scale = self.SimulationSpeed
                                    obj.modifiers["Cloth"].collision_settings.collision_quality = self.SimulationCollisionQuality
                                    obj.modifiers["Cloth"].collision_settings.distance_min = self.SimulationCollisionDistance
                                break

bpy.types.Object.Armor = BoolProperty(
    default=True, name = "Armor")

bpy.types.Object.ShowSimulation = BoolProperty(
    default=False, name = "Simulation", update = update_Simulation)

bpy.types.Object.SimulationStart = IntProperty(
    default=1, name = "Start", update = update_Simulation)

bpy.types.Object.SimulationEnd = IntProperty(
    default=250, name = "End", update = update_Simulation)

bpy.types.Object.SimulationQuality = IntProperty(
    min = 1, max = 80, default=5, name = "Quality", update = update_Simulation)

bpy.types.Object.SimulationSpeed = FloatProperty(
    min = 0, max = 10, default=1.0, name = "Speed Mutiplier", update = update_Simulation)

bpy.types.Object.SimulationCollision = BoolProperty(
    default=False, name = "Object Collision", update = update_Simulation)

bpy.types.Object.SimulationSelfCollision = BoolProperty(
    default=False, name = "Self Collision", update = update_Simulation)

bpy.types.Object.SimulationCollisionQuality = IntProperty(
    min = 1, max = 20, default=2, name = "Quality", update = update_Simulation)

bpy.types.Object.SimulationCollisionDistance = FloatProperty(
    min = 0.001, max = 1, default= 0.015, name = "Distance", unit='LENGTH', update = update_Simulation)

bpy.types.Object.DynamicCloth = FloatProperty(
    min=0, max=1, default=0.25, name = "Cloth")

bpy.types.Object.DynamicHairFront = FloatProperty(
    min=0, max=1, default=0.5, name = "Front")

bpy.types.Object.DynamicHairRight = FloatProperty(
    min=0, max=1, default=0.025, name = "Right")

bpy.types.Object.DynamicHairLeft = FloatProperty(
    min=0, max=1, default=0.025, name = "Left")

bpy.types.Object.DynamicHairBack = FloatProperty(
    min=0, max=1, default=0.5, name = "Back")

bpy.types.Object.DynamicHairTail = FloatProperty(
    min=0, max=1, default=0.5, name = "Tail")

bpy.types.Object.RotateHairFront = FloatProperty(
    min=0, max=1, default=0.25, name = "Front")

bpy.types.Object.RotateHairRight = FloatProperty(
    min=0, max=1, default=0.25, name = "Right")

bpy.types.Object.RotateHairLeft = FloatProperty(
    min=0, max=1, default=0.25, name = "Left")

bpy.types.Object.RotateHairBack = FloatProperty(
    min=0, max=1, default=0.25, name = "Back")

bpy.types.Object.RotateHairTail = FloatProperty(
    min=0, max=1, default=0.25, name = "Tail")

def drawrigAddition(self, context):
    layout = self.layout
    scene = context.scene
    box = layout.box()
    rig = context.active_object
    if rig.Sub_ID == 'Rossweisse':
        row = box.row()
        row.label(text = "Asset:")
        row = box.row()
        row.prop(rig, "Armor", toggle = True)
        row = box.row()
        row.label(text = "Hair Sync Rotation:")
        row = box.row()
        row.prop(rig, "RotateHairFront", slider = True)
        row = box.row()
        row.prop(rig, "RotateHairRight", slider = True)
        row.prop(rig, "RotateHairLeft", slider = True)
        row = box.row()
        row.prop(rig, "RotateHairBack", slider = True)
        row = box.row()
        row.prop(rig, "RotateHairTail", slider = True)

        row = box.row()
        row.label(text = "Hair Dynamic:")
        row = box.row()
        row.prop(rig, "DynamicHairFront", slider = True)
        row = box.row()
        row.prop(rig, "DynamicHairRight", slider = True)
        row.prop(rig, "DynamicHairLeft", slider = True)
        row = box.row()
        row.prop(rig, "DynamicHairBack", slider = True)
        row = box.row()
        row.prop(rig, "DynamicHairTail", slider = True)

        row = box.row()
        row.label(text = "Dynamic Bone:")
        row = box.row()
        row.prop(rig, "DynamicCloth", slider = True)
        row = box.row()
        row.label(text = "Simulation:")
        row = box.row()
        row.prop(rig, "ShowSimulation", icon = "MOD_CLOTH", toggle = True)
        if rig.ShowSimulation == True:
            row = box.row()
            row.prop(rig, "SimulationQuality")
            row.prop(rig, "SimulationSpeed")
            row = box.row()
            row.prop(rig, "SimulationStart")
            row.prop(rig, "SimulationEnd")
            row = box.row()
            row.label(text = "Collision:")
            row = box.row()
            row.prop(rig, "SimulationCollision", toggle = True)
            row.prop(rig, "SimulationSelfCollision", toggle = True)
            if rig.SimulationCollision == True:
                row = box.row()
                row.prop(rig, "SimulationCollisionQuality")
                row.prop(rig, "SimulationCollisionDistance")
            row = box.row()
            row.label(text = "Bake:")
            row = box.row()
            row.operator("ptcache.bake_all", text = "Bake All Dynamics").bake=True
            row.operator("ptcache.free_bake_all", text = "Delete All Bakes")

