import bpy
from bpy.types import Operator
 
 
class OBJECT_OT_vertex_group_remove_empty(Operator):
    bl_idname = "object.vertex_group_remove_empty"
    bl_label = "Remove Empty Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}
    bl_region_type = 'UI'
 
    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH')

    def execute(self, context):

        ob = context.object
        ob.update_from_editmode()
       
        vgroup_used = {i: False for i, k in enumerate(ob.vertex_groups)}
       
        for v in ob.data.vertices:
            for g in v.groups:
                if g.weight > 0.0:
                    vgroup_used[g.group] = True
       
        for i, used in sorted(vgroup_used.items(), reverse=True):
            if not used:
                ob.vertex_groups.remove(ob.vertex_groups[i])
               
        return {'FINISHED'}
    
class OBJECT_OT_vertex_group_mirror_prefix(Operator):
    bl_idname = "object.vertex_group_mirror_prefix"
    bl_label = "Remove Unused Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}
    bl_region_type = 'UI'
 
    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH')

    def execute(self, context):

        obj = context.object
        obj.update_from_editmode()

        Lprefix = ['L', 'Left', 'LEFT']
        Rprefix = ['R', 'Right', 'RIGHT']

        for vertex_group in obj.vertex_groups:
            for i, p in enumerate(Lprefix):
                if vertex_group.name.startswith(p + "."):
                    name = vertex_group.name.replace(p + ".", "")
                    r_prefix = Rprefix[i] + "." + name

                    # Check if the corresponding "R." prefix exists
                    if r_prefix in obj.vertex_groups:
                        self.report({'INFO'}, "Prefix '{}' already has corresponding " + Rprefix[i] + ". prefix. Skipping creation.".format(vertex_group.name))
                        continue

                    # Create the new "R." prefix
                    obj.vertex_groups.new(name=r_prefix)
                    self.report({'INFO'}, "Created prefix '{}'.".format(r_prefix))
                else:
                    continue

            for i, p in enumerate(Rprefix):
                if vertex_group.name.startswith(p + "."):
                    name = vertex_group.name.replace(p + ".", "")
                    l_prefix = Lprefix[i] + "." + name

                    # Check if the corresponding "L." prefix exists
                    if l_prefix in obj.vertex_groups:
                        self.report({'INFO'}, "Prefix '{}' already has corresponding " + Lprefix[i] + ". prefix. Skipping creation.".format(vertex_group.name))
                        continue

                    # Create the new "L." prefix
                    obj.vertex_groups.new(name=l_prefix)
                    self.report({'INFO'}, "Created prefix '{}'.".format(l_prefix))
                else:
                    continue
       


               
        return {'FINISHED'}

class VertexGroupAdd(Operator):
    bl_idname = "add.vertex_group"
    bl_label = "Vertex Groups Add"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        if scene.VertexGroupMenu == 'one':
            if scene.FixName != "":
                if scene.FixNameType == 'one':
                    Name = scene.FixName + "_" + scene.VertexGroupName
                if scene.FixNameType == 'two':
                    Name = scene.VertexGroupName + "_" + scene.FixName
            else:
                Name = scene.VertexGroupName

        if scene.VertexGroupMenu == 'two':
            Part = ['Head', 'Body']
            if scene.VertexGroupPart in Part:
                Name = str(scene.VertexGroupPart)
            else:
                if scene.VertexGroupLR == 'one':
                    name = 'L.'+str(scene.VertexGroupPart)
                    if scene.FixName != "":
                        if scene.FixNameType == 'one':
                            Name = scene.FixName + "_" + name
                        if scene.FixNameType == 'two':
                            Name = name + "_" + scene.FixName
                    else:
                        Name = 'L.'+str(scene.VertexGroupPart)
                elif scene.VertexGroupLR == 'two':
                    name = 'R.'+str(scene.VertexGroupPart)
                    if scene.FixName != "":
                        if scene.FixNameType == 'one':
                            Name = scene.FixName + "_" + name
                        if scene.FixNameType == 'two':
                            Name = name + "_" + scene.FixName
                    else:
                        Name = name

        new_vertex_group = context.active_object.vertex_groups.new(name=Name)
        mesh = context.active_object.data
        vertices = mesh.vertices
        vertex_indices = [v.index for v in vertices]
        for index in vertex_indices:
            new_vertex_group.add([index], 1.0, 'ADD')

        return {'FINISHED'}

class VertexGroupAddLoop(Operator):
    bl_idname = "add.vertex_group_loop"
    bl_label = "Vertex Groups Add Loop"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
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

        return {'FINISHED'}

def draw_func(self, context):
    layout = self.layout
    layout.operator(
    OBJECT_OT_vertex_group_remove_empty.bl_idname, text = "Remove Empty Vertex Groups",
    icon='X')
    layout.operator(
    OBJECT_OT_vertex_group_mirror_prefix.bl_idname, text = "Mirror Prefix Vertex Groups",
    icon='MOD_MIRROR')
    layout.separator()


classes = (
    OBJECT_OT_vertex_group_remove_empty,
    OBJECT_OT_vertex_group_mirror_prefix,
    VertexGroupAdd,
    VertexGroupAddLoop,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.MESH_MT_vertex_group_context_menu.prepend(draw_func)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.MESH_MT_vertex_group_context_menu.remove(draw_func)
 
if __name__ == "__main__":
    register()