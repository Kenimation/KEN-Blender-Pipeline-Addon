import bpy
import os
from . import AnimeDefs
from ..Minecraft import minecraftDefs
from bpy.props import (StringProperty,
                        IntProperty)

def riggetpreference(type):
    # select the rig
    rig = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = rig
        # props from user preferencesSettings.cfg
            #   arm ik
            #   flip bone
    flip_bone = minecraftDefs.readTextPrefs(4)
    if flip_bone == "False":
        rig.flipBone = 0
    else:
        rig.flipBone = 1
            #   arm ik
    arm_ik = minecraftDefs.readTextPrefs(7)
    if arm_ik == "IK":
        arm_ik = 1
    else:
        arm_ik = 0
    rig.Arm_IK_Left = arm_ik
    rig.Arm_IK_Right = arm_ik
        # leg ik
    leg_ik = minecraftDefs.readTextPrefs(10)
    if leg_ik == "IK":
        leg_ik = 1
    else:
        leg_ik = 0
    rig.Leg_IK_Left = leg_ik
    rig.Leg_IK_Right = leg_ik

    finger = minecraftDefs.readTextPrefs(13)
    if finger == "On":
        rig.Finger = 1
    else:
        rig.Finger = 0

    if type == "default":
        pass

class Append_TheAnimeRigKENFemale(bpy.types.Operator):
    bl_idname = "append.kenanimefemale"
    bl_label = "KEN Anime Rig [Female]"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        script_file = os.path.realpath(os.path.dirname(__file__))

        script_directory = os.path.dirname(script_file)
        script_directory = os.path.join(script_directory, "Rigs", "Anime")
        script_directory = os.path.normpath(script_directory)

        blendfile = os.path.join(script_directory, "KEN Minecraft Rig Remastered v1.0.blend")
        section = "Collection"
        obj = "Append KEN Anime Rig"
        filepath  = os.path.join(blendfile,section,obj)
        directory = os.path.join(blendfile,section)
        filename  = obj
        bpy.ops.wm.append(filepath=filepath,filename=filename,directory=directory,link=False,active_collection=False)

        type = "female"
        riggetpreference(type)

        bpy.ops.object.select_all(action='DESELECT')

        print("KEN Anime Rig has been appended!")
        return {'FINISHED'}

classes = (Append_TheAnimeRigKENFemale,
          )

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()