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
                assetsDefs.copytransform("loc", "x")
            if self.y == True:
                assetsDefs.copytransform("loc", "y")
            if self.z == True:
                assetsDefs.copytransform("loc", "z")
        except:
            self.report({"ERROR"}, "Cannot copy location!!!")
        return {'FINISHED'}
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.column_flow(columns = 3)
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
                assetsDefs.copytransform("rota", "x")
            if self.y == True:
                assetsDefs.copytransform("rota", "y")
            if self.z == True:
                assetsDefs.copytransform("rota", "z")
        except:
            self.report({"ERROR"}, "Cannot copy rotation!!!")
        return {'FINISHED'}
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.column_flow(columns = 3)
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
                assetsDefs.copytransform("size", "x")
            if self.y == True:
                assetsDefs.copytransform("size", "y")
            if self.z == True:
                assetsDefs.copytransform("size", "z")
        except:
            self.report({"ERROR"}, "Cannot copy size!!!")
        return {'FINISHED'}
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.column_flow(columns = 3)
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
                    assetsDefs.copytransform("loc", "x")
                if self.y == True:
                    assetsDefs.copytransform("loc", "y")
                if self.z == True:
                    assetsDefs.copytransform("loc", "z")
            if self.copyrota == True:
                if self.x == True:
                    assetsDefs.copytransform("rota", "x")
                if self.y == True:
                    assetsDefs.copytransform("rota", "y")
                if self.z == True:
                    assetsDefs.copytransform("rota", "z")
            if self.copysize == True:  
                if self.x == True:
                    assetsDefs.copytransform("size", "x")
                if self.y == True:
                    assetsDefs.copytransform("size", "y")
                if self.z == True:
                    assetsDefs.copytransform("size", "z")
        except:
            self.report({"ERROR"}, "Cannot copy transform!!!")
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.column_flow(columns = 3)
        row = box.row()
        row.prop(self, "copyloc", toggle = True)
        row.prop(self, "copyrota", toggle = True)
        row.prop(self, "copysize", toggle = True)
        row = box.row()
        row.prop(self, "x", toggle = True)
        row.prop(self, "y", toggle = True)
        row.prop(self, "z", toggle = True)

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

class Addconstraints(bpy.types.Operator):
    bl_idname = "add.constraints"
    bl_label = "Add Constraints"
    bl_options = {'REGISTER', 'UNDO'}

    type: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        try:
            if self.type == 'CHILD_OF':
                if bpy.context.object.mode == 'OBJECT':
                    bpy.ops.object.constraint_add(type='CHILD_OF')
                elif bpy.context.object.mode == 'POSE':
                    bpy.ops.pose.constraint_add(type='CHILD_OF')
            if self.type == 'DAMPED_TRACK':
                if bpy.context.object.mode == 'OBJECT':
                    bpy.ops.object.constraint_add(type='DAMPED_TRACK')
                elif bpy.context.object.mode == 'POSE':
                    bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
            if self.type == 'FOLLOW_PATH':
                if bpy.context.object.mode == 'OBJECT':
                    bpy.ops.object.constraint_add(type='FOLLOW_PATH')
                elif bpy.context.object.mode == 'POSE':
                    bpy.ops.pose.constraint_add(type='FOLLOW_PATH')
        except:
            self.report({"ERROR"}, "Cannot add Child Of!!!")
        return {"FINISHED"}
    
class Set_inverse(bpy.types.Operator):
    bl_idname = "set.inverse"
    bl_label = "Set Inverse"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            bpy.ops.constraint.childof_set_inverse(constraint=self.id, owner='OBJECT')
        elif bpy.context.object.mode == 'POSE':
            bpy.ops.constraint.childof_set_inverse(constraint=self.id, owner='BONE')
        return {"FINISHED"}
 
class Clear_inverse(bpy.types.Operator):
    bl_idname = "clear.inverse"
    bl_label = "Clear Inverse"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            bpy.ops.constraint.childof_clear_inverse(constraint=self.id, owner='OBJECT')    
        elif bpy.context.object.mode == 'POSE':
            bpy.ops.constraint.childof_clear_inverse(constraint=self.id, owner='BONE')
        return {"FINISHED"}

class All_constraint(bpy.types.Operator):
    bl_idname = "all.constraint"
    bl_label = "All Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    type: bpy.props.IntProperty(options={'HIDDEN'})

    def execute(self, context):
        if self.type == 0:
            obj = context.view_layer.objects.active
            for id in obj.modifiers[:]:
                bpy.ops.object.modifier_remove(modifier=id.name)
        if self.type == 1:
            obj = context.object
            bones = context.active_pose_bone
            if obj.mode != 'POSE':
                con = obj.constraints
                for id in con[:]:
                    bpy.ops.constraint.delete(constraint=id.name)
            elif obj.mode == 'POSE':
                con = bones.constraints
                for id in con[:]:
                    bpy.ops.constraint.delete(constraint=id.name)
        if self.type == 2:
            obj = context.view_layer.objects.active
            for id in obj.modifiers[:]:
                bpy.ops.object.modifier_apply(modifier=id.name)
        if self.type == 3:
            obj = context.object
            bones = context.active_pose_bone
            if obj.mode != 'POSE':
                con = obj.constraints
                for id in con[:]:
                    bpy.ops.constraint.apply(constraint=id.name)
            elif obj.mode == 'POSE':
                con = bones.constraints
                for id in con[:]:
                    bpy.ops.constraint.apply(constraint=id.name)
        return {"FINISHED"}

class Delete_constraint(bpy.types.Operator):
    bl_idname = "delete.constraint"
    bl_label = "Delete Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            bpy.ops.constraint.delete(constraint=self.id, owner='OBJECT')
            bpy.ops.object.modifier_remove(modifier=self.id)
        elif bpy.context.object.mode == 'POSE':
            bpy.ops.constraint.delete(constraint=self.id, owner='BONE')
        return {"FINISHED"}

class Apply_constraint(bpy.types.Operator):
    bl_idname = "apply.constraint"
    bl_label = "Apply Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            bpy.ops.constraint.apply(constraint=self.id, owner='OBJECT')
            bpy.ops.object.modifier_apply(modifier=self.id)
        elif bpy.context.object.mode == 'POSE':
            bpy.ops.constraint.apply(constraint=self.id, owner='BONE')
        return {"FINISHED"}

class Copy_constraint(bpy.types.Operator):
    bl_idname = "copy.constraint"
    bl_label = "Copy Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            bpy.ops.constraint.copy(constraint=self.id, owner='OBJECT')
            bpy.ops.object.modifier_copy(modifier=self.id)
        elif bpy.context.object.mode == 'POSE':
            bpy.ops.constraint.copy(constraint=self.id, owner='BONE')
        return {"FINISHED"}

class Disable_constraint(bpy.types.Operator):
    bl_idname = "disable.constraint"
    bl_label = "Disable Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            ob = bpy.context.object
            constraint = ob.constraints.get(self.id)
            if constraint:
                mw = ob.matrix_world.copy()
                constraint.influence = 0
                ob.matrix_world = mw
        elif bpy.context.object.mode == 'POSE':
            bone = bpy.context.active_pose_bone
            constraint = bone.constraints.get(self.id)
            if constraint:
                mw = bone.matrix.copy()
                constraint.influence = 0
                bone.matrix = mw
        return {"FINISHED"}

class New_Material(bpy.types.Operator):
    bl_idname = "new.material"
    bl_label = "New Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            ob = bpy.context.active_object
            # Get material
            mat = bpy.data.materials.new(name="Material")
            mat.use_nodes = True

            # Assign it to object
            if ob.data.materials:
                # assign to 1st material slot
                slot = bpy.context.object.active_material_index
                ob.data.materials[slot] = mat
            else:
                # no slots
                ob.data.materials.append(mat)
            assetsDefs.fixmaterial()
        except:
             pass
        return {"FINISHED"}

class Add_Image(bpy.types.Operator):
    bl_idname = "add.image"
    bl_label = "Add Image"
    bl_options = {'REGISTER', 'UNDO'}

    mat: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        mat = bpy.data.materials[self.mat]
        node_tree = mat.node_tree
        tex_node = node_tree.nodes.new('ShaderNodeTexImage')
        tex_node.interpolation = 'Closest'
        tex_node.location = assetsDefs.tex_node_loc
        for node in mat.node_tree.nodes:
            if node.name == "Principled BSDF":
                bsdf = node
                node_tree.links.new(bsdf.inputs['Base Color'], tex_node.outputs['Color'])
                node_tree.links.new(bsdf.inputs['Subsurface Color'], tex_node.outputs['Color'])

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

        if self.id == "DampedTrackLoop":
            rig = context.active_object
            obj = context.selected_objects
            prefix = scene.Track_Prefix
            if rig.mode == 'POSE':
                selected_bones = context.selected_pose_bones
                for bone in selected_bones:
                    constraint = bone.constraints.new(type = 'DAMPED_TRACK')
                    for obj in context.selected_objects:
                        if obj != rig:
                            constraint.target = obj
                            constraint.subtarget = prefix + bone.name

        if self.id == "ConstraintsDriver":
            rig = bpy.context.active_object
            obj = bpy.context.selected_objects

            if rig.mode == 'POSE':                
                selected_bones = bpy.context.selected_pose_bones     
                for bone in selected_bones:
                    constraint = bone.constraints.get(scene.Constraints_Type)
                    if constraint is not None:
                        constraint = constraint.driver_add("influence")
                        constraint.driver.type="AVERAGE"
                        constraint.driver.variables.new()
                        constraint.driver.variables[0].targets[0].id = rig
                        constraint.driver.variables[0].targets[0].data_path = scene.Rig_Prop

        if self.id == "ConstraintsDriverRemove":
            rig = bpy.context.active_object
            obj = bpy.context.selected_objects

            if rig.mode == 'POSE':                
                selected_bones = bpy.context.selected_pose_bones     
                for bone in selected_bones:
                    constraint = bone.constraints.get(scene.Constraints_Type)
                    if constraint is not None:
                        constraint = constraint.driver_remove("influence")           
        
        if self.id == "VertexGroupAdd":

            if scene.VertexGroupMenu == 'one':
                if scene.FixNameType == 'one':
                    Name = scene.FixName + "_" + scene.VertexGroupName
                if scene.FixNameType == 'two':
                    Name = scene.VertexGroupName + "_" + scene.FixName
            if scene.VertexGroupMenu == 'two':
                Part = ['Head', 'Body']
                if scene.VertexGroupPart in Part:
                    Name = str(scene.VertexGroupPart)
                else:
                    if scene.VertexGroupLR == 'one':
                        if scene.FixNameType == 'one':
                            Name = scene.FixName + "_" + 'L.'+str(scene.VertexGroupPart)
                        if scene.FixNameType == 'two':
                            Name = 'L.'+str(scene.VertexGroupPart) + "_" + scene.FixName
                    elif scene.VertexGroupLR == 'two':
                        if scene.FixNameType == 'one':
                            Name = scene.FixName + "_" + 'R.'+str(scene.VertexGroupPart)
                        if scene.FixNameType == 'two':
                            Name = 'R.'+str(scene.VertexGroupPart) + "_" + scene.FixName

            new_vertex_group = context.active_object.vertex_groups.new(name=Name)
            mesh = context.active_object.data
            vertices = mesh.vertices
            vertex_indices = [v.index for v in vertices]
            for index in vertex_indices:
                new_vertex_group.add([index], 1.0, 'ADD')


        if self.id == "VertexGroupLoop":
            Count = scene.VertexGroupCount
            Name = scene.VertexGroupName
            if scene.VertexGroupMiiror == True:
                for num in range(Count*2, 0, 2):
                    pair = [num, num + 1]
                    new_vertex_group = bpy.context.active_object.vertex_groups.new(name=Name)
                    vertex_group_data = pair
                    new_vertex_group.add(vertex_group_data, 1.0, 'ADD')
            else:
                for num in range(0, Count*2, 2):
                    pair = [num, num + 1]
                    new_vertex_group = bpy.context.active_object.vertex_groups.new(name=Name)
                    vertex_group_data = pair
                    new_vertex_group.add(vertex_group_data, 1.0, 'ADD')
             
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
            if self.subtype == "clean":
                img_list = []

                for img in bpy.data.images:
                    if img.use_fake_user == False:
                        img_name = img.name.removesuffix(".png" or ".jpg")
                        if img_name.split(".")[0] is not None:
                            img.name = img_name.split(".")[0]
                            img_list.append(img.name)
                        if img_name == img_name.split(".")[0]:
                            img_list.append(img.name)
                        
                for material in bpy.data.materials:
                    node_tree = material.node_tree
                    if node_tree:
                        for node in node_tree.nodes:
                            if node.type == "TEX_IMAGE" and node.image.name not in img_list:
                                node.image = bpy.data.images[node.image.name.split(".")[0]]

                for node_groups in bpy.data.node_groups:
                    for node in node_groups.nodes:
                        if node.type == "IMAGE_TEXTURE" and node.inputs[0].default_value.name not in img_list:
                            node.inputs[0].default_value = bpy.data.images[node.inputs[0].default_value.name.split(".")[0]]

                for img in bpy.data.images:
                    if img.use_fake_user == False:
                        if img.name not in img_list:
                            if img.name != img.name.split(".")[0]:
                                bpy.data.images.remove(img)

                img_list.clear()

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
                                
            if self.subtype == "clean":
                mat_list = []

                for mat in bpy.data.materials:
                    if mat.use_fake_user == False:
                        if mat.name == mat.name.split(".")[0]:
                            mat_list.append(mat.name)

                for obj in bpy.data.objects:
                    if obj.type == "MESH" and obj.data.materials:
                        try:
                            for mat_slot in obj.material_slots:
                                if mat_slot.material.name not in mat_list and mat_slot.material.use_fake_user == False:
                                    try:
                                        mat_slot.material = bpy.data.materials[mat_slot.material.name.split(".")[0]]
                                    except:
                                        mat_slot.material.name = mat_slot.material.name.split(".")[0]
                        except:
                            pass

                for node_groups in bpy.data.node_groups:
                    for node in node_groups.nodes:
                        if node.type == "SET_MATERIAL" and node.inputs[2].default_value not in mat_list:
                            try:
                                node.inputs[2].default_value = bpy.data.materials[node.inputs[2].default_value.name.split(".")[0]]
                            except:
                                node.inputs[2].default_value.name = node.inputs[2].default_value.name.split(".")[0]
                            
                for mat in bpy.data.materials:
                    if mat.use_fake_user == False:
                        if mat.name not in mat_list:
                            if mat.name != mat.name.split(".")[0]:
                                bpy.data.materials.remove(mat)
                mat_list.clear()

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


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

classes = (
            Copyloc,
            Copyrota,
            Copysize,
            Copytransform,
            Open_Image,
            RestCursor,
            Addconstraints,
            Copy_constraint,
            All_constraint,
            Set_inverse,
            Clear_inverse,
            Delete_constraint,
            Apply_constraint,
            Disable_constraint,
            New_Material,
            Add_Image,
            Operators,
            Data_Blend,
            Solo_Light,
            Open_ImageFile,
            Crease,
            IMAGEPACK,
            IMAGERELOAD,
            ParentObjectsToRig,
          )        

register, unregister = bpy.utils.register_classes_factory(classes)
