import bpy
import os
from bpy_extras.io_utils import ImportHelper
from . import assetsDefs
import bmesh
from bpy.types import Operator, OperatorFileListElement
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                      operators
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RestCursor(bpy.types.Operator):
    bl_idname = "rest.cursor"
    bl_label = "Rest Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            context.scene.cursor.location[0] = 0
            context.scene.cursor.location[1] = 0
            context.scene.cursor.location[2] = 0
            self.report({"INFO"}, "Cursor Rest.")
        except:
            self.report({"ERROR"}, "Cannot Rest Cursor!!!")
        return {'FINISHED'}
  
class Remove_All_By_Type(bpy.types.Operator):
    bl_idname = "object.remove_all_by_type"
    bl_label = "Remove Object Type"
    bl_options = {'REGISTER', 'UNDO'}

    type: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        count = 0
        for obj in context.scene.objects:
            if obj.type == self.type:
                bpy.data.objects.remove(obj, do_unlink=True)
                count += 1

        self.report({"INFO"}, str(count) + "" + self.type + " Objects have removed.")
        return {"FINISHED"}

class Set_Select(bpy.types.Operator):
    bl_idname = "object.set_select"
    bl_label = "Object Set Select"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        for item in context.scene.objects:
            item.select_set(False)
        bpy.context.view_layer.objects.active = bpy.data.objects[self.object]
        bpy.data.objects[self.object].select_set(state = True)

        self.report({"INFO"}, self.object + " Object selected.")
        return {"FINISHED"}
    
class Duplicate_List(bpy.types.Operator):
    bl_idname = "object.duplicate_list"
    bl_label = "Duplicate Object in list"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        scene = context.scene
        obj = bpy.data.objects[self.object]
        bpy.ops.object.set_select(object=self.object)
        bpy.ops.object.duplicate()
        count = len([ob for ob in context.scene.objects if ob.type == obj.type])
        if obj.type == "LIGHT":
            scene.light_index = count + 1
        elif obj.type == "CAMERA":
            scene.cam_index = count - 1

        self.report({"INFO"}, self.object + " Object has been duplicated.")
        return {"FINISHED"}

class Jump_Frame(bpy.types.Operator):
    bl_idname = "frames.jump"
    bl_label = "Jump Frames"

    frame: bpy.props.FloatProperty(options={'HIDDEN'})

    def execute(self, context):
        context.scene.frame_set(int(self.frame))
        return {"FINISHED"}

class Crease(bpy.types.Operator):
    bl_idname = "set.crease"
    bl_label = "Set Crease"
    bl_options = {'REGISTER', 'UNDO'}

    items = [
        ('All', 'All', ''),
        ('Selected Elements', 'Selected Elements', '')
    ]

    mode: bpy.props.IntProperty(options={'HIDDEN'})
    type: bpy.props.StringProperty(options={'HIDDEN'})

    whoToInfluence: bpy.props.EnumProperty(
        description = "Influence all / selection",
        name        = "whoToInfluence",
        items       = items,
        default     = 'Selected Elements'
    )

    def execute(self, context):
        o  = bpy.context.object
        d  = o.data
        bm = bmesh.from_edit_mesh(d)

        if self.type == 'set':
            type = 1
        elif self.type == 'clear':
            type = 0

        if self.mode == 1:

            creaseLayer = bm.verts.layers.crease.verify()

            if self.whoToInfluence == 'Selected Elements':
                selectedVerts = [v for v in bm.verts if v.select]
                for v in selectedVerts: v[creaseLayer] = type
            else:
                for v in bm.verts: v[creaseLayer] = type

            bmesh.update_edit_mesh(d)

        if self.mode == 2:

            creaseLayer = bm.edges.layers.crease.verify()

            if self.whoToInfluence == 'Selected Elements':
                selectedEdges = [e for e in bm.edges if e.select]
                for e in selectedEdges: e[creaseLayer] = type
            else:
                for e in bm.edges: e[creaseLayer] = type

            bmesh.update_edit_mesh(d)

        return {"FINISHED"}

class IMAGEPACK(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "pack.img"
    bl_label = ""
    bl_description = "Pack/Unpack the texture"

    id_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        img = bpy.data.images[self.id_name]
        if assetsDefs.is_packed(img):
            img.pack()
        else:
            assetsDefs.safe_unpack(img)
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)
        return {'FINISHED'}

class IMAGERELOAD(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "reload.img"
    bl_label = ""
    bl_description = "reload the texture"

    id_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        img = bpy.data.images[self.id_name]
        img.reload()
        print("image reloaded")
        return {'FINISHED'}

class ParentObjectsToRig(bpy.types.Operator):
    bl_idname = "parent.rig"
    bl_label = "parent to rig"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = context.scene
        rig = context.object
        
        try:
            boneName = scn.boneName
            if bpy.context.active_object.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            selected_objects = context.selected_objects

            for object in selected_objects:
                bpy.ops.object.select_all(action='DESELECT')
                context.view_layer.objects.active = object

                # add armature modifier
                if object != rig:
                    object.modifiers.new(name = 'Skeleton', type = 'ARMATURE')
                    object.modifiers['Skeleton'].object = rig

                    # add vertices
                    vertices = []
                    vertices.clear()
                    for vtc in range(len(object.data.vertices)):
                        vertices.append(vtc)
                    new_vertex_group = bpy.context.active_object.vertex_groups.new(name=boneName)
                    new_vertex_group.add(vertices, 1.0, 'ADD')
            scn.boneName = ""
            return {'FINISHED'}
        except:
            self.report({"ERROR"}, "an error occured; objects might not be selected")
            return {"CANCELLED"}

class SelectBoneGroup(bpy.types.Operator):
    bl_idname = "bone.selectgroup"
    bl_label = "Select Bone Group"
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty()

    def execute(self, context):
        rig = context.active_object

            # Find the active index of the collection
        for index, collection in enumerate(rig.data.collections):
            if collection.name == self.name:
                rig.data.collections.active_index = index
                bpy.ops.armature.collection_select()
                break


        return {'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

classes = (
            RestCursor,
            Set_Select,
            Duplicate_List,
            Remove_All_By_Type,
            Jump_Frame,
            Crease,
            IMAGEPACK,
            IMAGERELOAD,
            ParentObjectsToRig,
            SelectBoneGroup,
          )        

register, unregister = bpy.utils.register_classes_factory(classes)
