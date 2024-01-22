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
            bpy.context.scene.cursor.location[0] = 0
            bpy.context.scene.cursor.location[1] = 0
            bpy.context.scene.cursor.location[2] = 0
        except:
            self.report({"ERROR"}, "Cannot Rest Cursor!!!")
        return {'FINISHED'}
  
class Open_Image(bpy.types.Operator, ImportHelper):
    bl_idname = "open.image"
    bl_label = "Open Image"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = '.png'

    filter_glob: StringProperty(
        default='*.png',
        options={'HIDDEN'},
    )

    directory: StringProperty(
            subtype='DIR_PATH',
    )

    img: bpy.props.StringProperty(options={'HIDDEN'})

    mat: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        (path, file) = os.path.split(self.filepath)
        image = bpy.data.images.load(filepath=self.filepath, check_existing=True)
        script_file = os.path.realpath(__file__)
        script_directory = os.path.dirname(script_file)
        script_directory = os.path.normpath(script_directory)
        mat = bpy.data.materials[self.mat]
        mat.node_tree.nodes[self.img].image = image
        image.reload()
        return {"FINISHED"}

class Operators(bpy.types.Operator):
    bl_idname = "bpy.ops"
    bl_label = "Bpy Operators"

    id: bpy.props.StringProperty(options={'HIDDEN'})
    object: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        scene = context.scene
        if self.id == "emptyselect":
            bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects

            for obj in bpy.context.scene.objects:
                if obj.type == scene.Object_Type:
                    obj.select_set(True)    

        if self.id == "add_paticles_start_frame":
            if context.active_object.particle_systems:
                try:
                    particles_list = []
                    for particles in context.active_object.particle_systems:
                        particles_list.append(particles)
                    particles_system = particles_list[scene.particles_index]
                    particles_data = particles_system.settings
                except:
                    pass
                particles_data.frame_start = context.scene.frame_current

        if self.id == "add_paticles_end_frame":
            if context.active_object.particle_systems:
                try:
                    particles_list = []
                    for particles in context.active_object.particle_systems:
                        particles_list.append(particles)
                    particles_system = particles_list[scene.particles_index]
                    particles_data = particles_system.settings
                except:
                    pass
                particles_data.frame_end = context.scene.frame_current 

        if self.id == "jump_frame":
            frame_number = self.object
            bpy.context.scene.frame_set(round(float(frame_number)))
            
        if self.id == "new_coll":
            collection = bpy.data.collections.new(self.object)
            bpy.context.scene.collection.children.link(collection)
        try:
            light = bpy.data.lights[self.object]
            if self.id == "light+1":
                power = light.energy
                light.energy = power*2
            if self.id == "light+0.5":
                power = light.energy
                light.energy = power*1.41421
            if self.id == "light-1":
                power = light.energy
                light.energy = power*0.5
            if self.id == "light-0.5":
                power = light.energy
                light.energy = power/1.41421
        except:
            pass
        if self.id == "new marker":
            if self.object == "":
                name = "None"
            else:
                name = self.object
            scene.timeline_markers.new(name, frame=scene.frame_current)
        if self.id == "del marker":
            m = scene.timeline_markers[self.object]
            scene.timeline_markers.remove(m)
        if self.id == "select":
            for item in context.scene.objects:
                item.select_set(False)
            bpy.context.view_layer.objects.active = bpy.data.objects[self.object]
            bpy.data.objects[self.object].select_set(state = True)
        if self.id == "select light":
            for ob in bpy.context.scene.objects:
                ob.select_set(ob.type == "LIGHT")
        if self.id == "select cam":
            for ob in bpy.context.scene.objects:
                ob.select_set(ob.type == "CAMERA")
        if self.id == "duplicate":
            obj = bpy.context.active_object


            new_obj = bpy.data.objects[self.object].copy()
            new_obj.data = bpy.data.objects[self.object].data.copy()
            try:
                if bpy.data.objects[self.object].animation_data is not None:
                    new_obj.animation_data_clear()
                    new_obj.animation_data_create()
                    new_obj.animation_data.action = bpy.data.objects[self.object].animation_data.action.copy()
            except:
                pass

            bpy.context.scene.collection.objects.link(new_obj)
            # Select the new object and make it the active object
            if obj:
                obj.select_set(False)
            bpy.context.view_layer.objects.active = new_obj
            new_obj.select_set(True)
        return {"FINISHED"}

class Solo_Light(bpy.types.Operator):
    bl_idname = "solo.light"
    bl_label = "Solo Light"
    bl_options = {'REGISTER', 'UNDO'}

    light: bpy.props.StringProperty(options={'HIDDEN'})
    solo: bpy.props.BoolProperty(options={'HIDDEN'})

    def execute(self, context):
        light = self.light
        list = []

        list.append(light)

        obj = bpy.data.objects[light]
        if obj.hide_viewport == True:
            obj.hide_viewport = False
        else:
            for light_data in bpy.data.objects:
                obj = bpy.data.objects[light_data.name]
                if obj.type == 'LIGHT':
                    if obj.name not in list:
                        obj.hide_viewport = True
                    else:
                        obj.hide_viewport = False

        return {"FINISHED"}

class Data_Blend(bpy.types.Operator):
    bl_idname = "data.blend"
    bl_label = "Data blend"
    bl_options = {'REGISTER', 'UNDO'}

    blend: bpy.props.StringProperty(options={'HIDDEN'})
    type: bpy.props.StringProperty(options={'HIDDEN'})
    subtype: bpy.props.StringProperty(options={'HIDDEN'})
    toggle: bpy.props.BoolProperty(options={'HIDDEN'})

    def execute(self, context):
        if self.type == "img":
            try:
                img_data = bpy.data.images[self.blend]
            except:
                pass
            if self.subtype == "reload":
                img_data.reload
            if self.subtype == "pack":
                if img_data.packed_files:
                    img_data.unpack(method='USE_ORIGINAL')
                else:
                    img_data.pack()
            if self.subtype == "remove":
                bpy.data.images.remove(img_data)

        if self.type == "mat":
            try:
                obj = context.view_layer.objects.active
                mat_data = bpy.data.materials[self.blend]
            except:
                pass
            if self.subtype == "replace":
                # Assign it to object
                for obj in context.selected_objects:
                    try:
                        context.view_layer.objects.active = obj
                        if obj.data.materials:
                            # assign to 1st material slot
                            slot = context.object.active_material_index
                            obj.data.materials[slot] = mat_data
                        else:
                            # no slots
                            obj.data.materials.append(mat_data)
                    except:
                        continue
            if self.subtype == "append":
                for obj in context.selected_objects:
                    try:
                        context.view_layer.objects.active = obj
                        obj.data.materials.append(mat_data)
                    except:
                        continue
            if self.subtype == "del":
                selected_objects = context.selected_objects
                for obj in selected_objects:
                    # Set the object as the active object in the current view layer
                    context.view_layer.objects.active = obj

                    # Remove all material slots from the object
                    for i in reversed(range(len(obj.material_slots))):
                        bpy.ops.object.material_slot_remove()

            if self.subtype == "remove":
                bpy.data.materials.remove(mat_data)
            if self.subtype == "single":
                slot = obj.active_material_index

                new_mat = mat_data.copy()

                obj.data.materials[slot] = new_mat

            if self.subtype == "duplicate":
                new_mat = mat_data.copy()

                obj.data.materials.append(new_mat)

            if self.subtype == "select":   
                obj = bpy.data.objects
                for ob in obj:
                    if ob.type == 'MESH':
                        try:
                            for m in ob.material_slots:
                                if m.material == mat_data:
                                    ob.select_set(True)
                        except:
                            continue

        if self.type == "light":
            if self.subtype == "remove":
                light_data = bpy.data.lights[self.blend]
                bpy.data.lights.remove(light_data)
            if self.subtype == "removeall":
                for light in bpy.data.lights:
                    bpy.data.lights.remove(light)

        if self.type == "cam":
            try:
                cam_data = bpy.data.cameras[self.blend]
            except:
                pass
            if self.subtype == "remove":
                bpy.data.cameras.remove(cam_data)
            if self.subtype == "view":
                context.scene.camera = bpy.data.objects[self.blend]
        
        if self.type == "coll":
            try:
                coll = bpy.data.collections[self.blend]
            except:
                pass
            if self.subtype == "remove":
                bpy.data.collections.remove(coll)
            if self.subtype == "removeall":
                for coll in bpy.data.collections:
                    bpy.data.collections.remove(coll)
            if self.subtype == "clean":
                for obj in coll.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)

        return {"FINISHED"}

class Open_ImageFile(bpy.types.Operator, ImportHelper):
    bl_idname = "open.imagefile"
    bl_label = "Open Image File"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = '.png'

    filter_glob: StringProperty(
        default='*.png',
        options={'HIDDEN'},
    )

    directory: StringProperty(
            subtype='DIR_PATH',
    )

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        (path, file) = os.path.split(self.filepath)
        try:
            bpy.data.images.load(filepath=self.filepath, check_existing=True)
            script_file = os.path.realpath(__file__)
            script_directory = os.path.dirname(script_file)
            script_directory = os.path.normpath(script_directory)
        except:
             pass
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
            Open_Image,
            RestCursor,
            Operators,
            Data_Blend,
            Solo_Light,
            Open_ImageFile,
            Crease,
            IMAGEPACK,
            IMAGERELOAD,
            ParentObjectsToRig,
            SelectBoneGroup,
          )        

register, unregister = bpy.utils.register_classes_factory(classes)
