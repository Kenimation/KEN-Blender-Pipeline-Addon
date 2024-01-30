import bpy
from bpy.types import Operator

class DampedTrackLoop(Operator):
    bl_idname = "add.dampedtrackloop"
    bl_label = "Add Damped Track Loop"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
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
        return {'FINISHED'}

class DampedTrackChild(Operator):
    bl_idname = "add.dampedtrackchild"
    bl_label = "Add Damped Track Child"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        # Check if an armature object is selected
        if obj.type == 'ARMATURE':
            
            for bone in obj.pose.bones:
                if bone.bone.select:
                    if bone.children:
                        # Create a Damped Track constraint
                        constraint = bone.constraints.new(type='DAMPED_TRACK')

                        # Set the target bone as the child bone
                        constraint.target = obj
                        
                        constraint.subtarget = bone.children[0].name

                        # Set the up axis
                        constraint.track_axis = 'TRACK_Y'
                        
        return {'FINISHED'}

class Copy_Rotation_Parent(Operator):
    bl_idname = "add.copyrotationparent"
    bl_label = "Add Copy Rotation Parent"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        # Check if an armature object is selected
        if obj.type == 'ARMATURE':
            
            for bone in obj.pose.bones:
                if bone.bone.select:
                    if bone.parent:
                        # Create a Damped Track constraint
                        constraint = bone.constraints.new(type='COPY_ROTATION')

                        # Set the target bone as the child bone
                        constraint.target = obj
                        constraint.subtarget = bone.parent.name
                        constraint.mix_mode = 'AFTER'
                        constraint.target_space = 'LOCAL'
                        constraint.owner_space = 'LOCAL'

                        
        return {'FINISHED'}

class ConstraintsDriver(Operator):
    bl_idname = "add.constraintsdriver"
    bl_label = "Add Constraints Driver"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        rig = context.active_object

        if rig.mode == 'POSE':                
            selected_bones = context.selected_pose_bones     
            for bone in selected_bones:
                constraint = bone.constraints.get(scene.Constraints_Type)
                if constraint is not None:
                    constraint = constraint.driver_add("influence")
                    constraint.driver.type="AVERAGE"
                    constraint.driver.variables.new()
                    constraint.driver.variables[0].targets[0].id = rig
                    constraint.driver.variables[0].targets[0].data_path = scene.Rig_Prop
        return {'FINISHED'}

class ConstraintsDriverRemove(Operator):
    bl_idname = "remove.constraintsdriver"
    bl_label = "Remove Constraints Driver"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        rig = context.active_object

        if rig.mode == 'POSE':                
            selected_bones = context.selected_pose_bones     
            for bone in selected_bones:
                constraint = bone.constraints.get(scene.Constraints_Type)
                if constraint is not None:
                    constraint = constraint.driver_remove("influence")   
        return {'FINISHED'}
     
def update_Damped_Track_Influence(self, context):
    obj = context.active_object
    # Check if an armature object is selected
    if obj.type == 'ARMATURE':
        for bone in obj.pose.bones:
            if bone.bone.select:
                # Create a Damped Track constraint
                for constraint in bone.constraints:
                    if constraint.type == 'DAMPED_TRACK':
                        constraint.influence = self.Damped_Track_Influence

def update_Copy_Rotation_Influence(self, context):
    obj = context.active_object
    # Check if an armature object is selected
    if obj.type == 'ARMATURE':
        for bone in obj.pose.bones:
            if bone.bone.select:
                # Create a Damped Track constraint
                for constraint in bone.constraints:
                    if constraint.type == 'COPY_ROTATION':
                        constraint.influence = self.Copy_Rotation_Influence

bpy.types.Scene.BoneTool = bpy.props.BoolProperty(
    name="Bone Tool",
    description="Enable Bone Tool",
    default= False
)

bpy.types.Scene.Damped_Track_Influence = bpy.props.FloatProperty(
    name="Influence",
    description="Damped Track Influence",
    max = 1,
    min = 0,
    default= 1,
    update = update_Damped_Track_Influence,
)

bpy.types.Scene.Copy_Rotation_Influence = bpy.props.FloatProperty(
    name="Influence",
    description="Copy Rotation Influence",
    max = 1,
    min = 0,
    default= 1,
    update = update_Copy_Rotation_Influence,
)

bpy.types.Scene.Track_Prefix = bpy.props.StringProperty(
    name="Track Prefix",
    description="Track Prefix",
    default= "Track_",
)

bpy.types.Scene.Rig_Prop = bpy.props.StringProperty(
    name="Rig Properties",
    description="Rig Properties",
    default= "Prop",
)

bpy.types.Scene.Constraints_Type = bpy.props.EnumProperty(
    default='Damped Track',
    items=[('Damped Track', 'Damped Track', ''),
           ('Child Of', 'Child Of', ''),
           ('Copy Rotation', 'Copy Rotation', ''),
            ])

classes = (
    DampedTrackLoop,
    DampedTrackChild,
    Copy_Rotation_Parent,
    ConstraintsDriver,
    ConstraintsDriverRemove
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
 
if __name__ == "__main__":
    register()