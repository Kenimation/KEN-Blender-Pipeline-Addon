import bpy
import os
from ..AssetsUI import assetsDefs

from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty

def copytransform(self, xyz):
    if bpy.context.object.mode == 'OBJECT':
        actobj = bpy.context.view_layer.objects.active
        if self == "loc":
            for obj in bpy.context.selected_objects:
                if xyz == "x":
                    obj.matrix_world.translation[0] = actobj.matrix_world.translation[0]
                if xyz == "y":
                    obj.matrix_world.translation[1] = actobj.matrix_world.translation[1]
                if xyz == "z":
                    obj.matrix_world.translation[2] = actobj.matrix_world.translation[2]
        if self == "rota":
            for obj in bpy.context.selected_objects:
                if xyz == "x":
                    obj.rotation_euler[0] = actobj.rotation_euler[0]
                if xyz == "y":
                    obj.rotation_euler[1] = actobj.rotation_euler[1]
                if xyz == "z":
                    obj.rotation_euler[2] = actobj.rotation_euler[2]
        if self == "size":
            for obj in bpy.context.selected_objects:
                if xyz == "x":
                    obj.scale[0] = actobj.scale[0]
                if xyz == "y":
                    obj.scale[1] = actobj.scale[1]
                if xyz == "z":
                    obj.scale[2] = actobj.scale[2]
    elif bpy.context.object.mode == 'POSE':
        actbones = bpy.context.active_pose_bone
        if self == "loc":
            for bones in bpy.context.selected_pose_bones:
                if xyz == "x":
                    bones.location[0] = actbones.location[0]
                if xyz == "y":
                    bones.location[1] = actbones.location[1]
                if xyz == "z":
                    bones.location[2] = actbones.location[2]
        if self == "rota":
            for bones in bpy.context.selected_pose_bones:
                if xyz == "x":
                    bones.rotation_euler[0] = actbones.rotation_euler[0]
                if xyz == "y":
                    bones.rotation_euler[1] = actbones.rotation_euler[1]
                if xyz == "z":
                    bones.rotation_euler[2] = actbones.rotation_euler[2]
        if self == "size":
            for bones in bpy.context.selected_pose_bones:
                if xyz == "x":
                    bones.scale[0] = actbones.scale[0]
                if xyz == "y":
                    bones.scale[1] = actbones.scale[1]
                if xyz == "z":
                    bones.scale[2] = actbones.scale[2]

class Copyloc(bpy.types.Operator):
    bl_idname = "copy.loc"
    bl_label = "Copy Location"
    bl_options = {'REGISTER', 'UNDO'}
    
    x: BoolProperty(
        name="X",
        description="Copy X.",
        default=True,
    )
    y: BoolProperty(
        name="Y",
        description="Copy Y",
        default=True,
    )
    z: BoolProperty(
        name="Z",
        description="Copy Z.",
        default=True,
    )

    def execute(self, context):
        try:
            if self.x == True:
                copytransform("loc", "x")
            if self.y == True:
                copytransform("loc", "y")
            if self.z == True:
                copytransform("loc", "z")
        except:
            self.report({"ERROR"}, "Cannot copy location!!!")
        return {'FINISHED'}
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(self, "x", toggle = True)
        row.prop(self, "y", toggle = True)
        row.prop(self, "z", toggle = True)
     
class Copyrota(bpy.types.Operator):
    bl_idname = "copy.rota"
    bl_label = "Copy Rotation"
    bl_options = {'REGISTER', 'UNDO'}
    
    x: BoolProperty(
        name="X",
        description="Copy X.",
        default=True,
    )
    y: BoolProperty(
        name="Y",
        description="Copy Y",
        default=True,
    )
    z: BoolProperty(
        name="Z",
        description="Copy Z.",
        default=True,
    )

    def execute(self, context):
        try:
            if self.x == True:
                copytransform("rota", "x")
            if self.y == True:
                copytransform("rota", "y")
            if self.z == True:
                copytransform("rota", "z")
        except:
            self.report({"ERROR"}, "Cannot copy rotation!!!")
        return {'FINISHED'}
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(self, "x", toggle = True)
        row.prop(self, "y", toggle = True)
        row.prop(self, "z", toggle = True)
    
class Copysize(bpy.types.Operator):
    bl_idname = "copy.size"
    bl_label = "Copy Size"
    bl_options = {'REGISTER', 'UNDO'}
    
    x: BoolProperty(
        name="X",
        description="Copy X.",
        default=True,
    )
    y: BoolProperty(
        name="Y",
        description="Copy Y",
        default=True,
    )
    z: BoolProperty(
        name="Z",
        description="Copy Z.",
        default=True,
    )

    def execute(self, context):
        try:
            if self.x == True:
                copytransform("size", "x")
            if self.y == True:
                copytransform("size", "y")
            if self.z == True:
                copytransform("size", "z")
        except:
            self.report({"ERROR"}, "Cannot copy size!!!")
        return {'FINISHED'}
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(self, "x", toggle = True)
        row.prop(self, "y", toggle = True)
        row.prop(self, "z", toggle = True)

class Copytransform(bpy.types.Operator):
    bl_idname = "copy.trans"
    bl_label = "Copy Transform"
    bl_options = {'REGISTER', 'UNDO'}
    
    copyloc: BoolProperty(
        name="Location",
        description="Copy Location.",
        default=True,
    )
    copyrota: BoolProperty(
        name="Rotation",
        description="Copy Rotation",
        default=True,
    )
    copysize: BoolProperty(
        name="Size",
        description="Copy Size.",
        default=True,
    )
    x: BoolProperty(
        name="X",
        description="Copy X.",
        default=True,
    )
    y: BoolProperty(
        name="Y",
        description="Copy Y",
        default=True,
    )
    z: BoolProperty(
        name="Z",
        description="Copy Z.",
        default=True,
    )

    def execute(self, context):
        try:
            if self.copyloc == True:
                if self.x == True:
                    copytransform("loc", "x")
                if self.y == True:
                    copytransform("loc", "y")
                if self.z == True:
                    copytransform("loc", "z")
            if self.copyrota == True:
                if self.x == True:
                    copytransform("rota", "x")
                if self.y == True:
                    copytransform("rota", "y")
                if self.z == True:
                    copytransform("rota", "z")
            if self.copysize == True:  
                if self.x == True:
                    copytransform("size", "x")
                if self.y == True:
                    copytransform("size", "y")
                if self.z == True:
                    copytransform("size", "z")
        except:
            self.report({"ERROR"}, "Cannot copy transform!!!")
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row(align=True)
        row.prop(self, "copyloc", toggle = True)
        row.prop(self, "copyrota", toggle = True)
        row.prop(self, "copysize", toggle = True)
        row = box.row(align=True)
        row.prop(self, "x", toggle = True)
        row.prop(self, "y", toggle = True)
        row.prop(self, "z", toggle = True)

classes = (
            Copyloc,
            Copyrota,
            Copysize,
            Copytransform,
          )        

register, unregister = bpy.utils.register_classes_factory(classes)