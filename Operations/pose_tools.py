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

class ConstraintsDriver(Operator):
    bl_idname = "add.constraintsdriver"
    bl_label = "Add Constraints Driver"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        rig = context.active_object

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
        return {'FINISHED'}

class ConstraintsDriverRemove(Operator):
    bl_idname = "remove.constraintsdriver"
    bl_label = "Remove Constraints Driver"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        rig = context.active_object

        if rig.mode == 'POSE':                
            selected_bones = bpy.context.selected_pose_bones     
            for bone in selected_bones:
                constraint = bone.constraints.get(scene.Constraints_Type)
                if constraint is not None:
                    constraint = constraint.driver_remove("influence")   
        return {'FINISHED'}

classes = (
    DampedTrackLoop,
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