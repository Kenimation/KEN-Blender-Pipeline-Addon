import bpy
import os
from . import AnimeDefs
from ..AssetsUI import assetsDefs
from bpy.props import (StringProperty,
                        IntProperty)

def anime_rig_get_preference(type):
    # select the rig
    rig = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = rig
        # props from user preferencesSettings.cfg
            #   arm ik
            #   flip bone
    flip_bone = assetsDefs.readTextPrefs(16)
    if flip_bone == "False":
        rig.flipBone = 0
    else:
        rig.flipBone = 1
            #   arm ik
    arm_ik = assetsDefs.readTextPrefs(19)
    if arm_ik == "IK":
        arm_ik = 1
    else:
        arm_ik = 0
    rig.Arm_IK_Left = arm_ik
    rig.Arm_IK_Right = arm_ik
        # leg ik
    leg_ik = assetsDefs.readTextPrefs(22)
    if leg_ik == "IK":
        leg_ik = 1
    else:
        leg_ik = 0
    rig.Leg_IK_Left = leg_ik
    rig.Leg_IK_Right = leg_ik

    rig_scale = assetsDefs.readTextPrefs(13)
    rig.RigScale = float(rig_scale)

class Append_TheAnimeRigKENFemale(bpy.types.Operator):
    bl_idname = "append.kenanimefemale"
    bl_label = "KEN Anime Rig [Female]"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        script_file = os.path.realpath(os.path.dirname(__file__))

        script_directory = os.path.dirname(script_file)
        script_directory = os.path.join(script_directory,"Assets" , "Rigs", "Anime")
        script_directory = os.path.normpath(script_directory)

        blendfile = os.path.join(script_directory, "KEN Anime Female Rig.blend")
        section = "Collection"
        obj = "KEN Anime Female Rig"
        filepath  = os.path.join(blendfile,section,obj)
        directory = os.path.join(blendfile,section)
        filename  = obj
        bpy.ops.wm.append(filepath=filepath,filename=filename,directory=directory,link=False,active_collection=False)

        type = "female"
        anime_rig_get_preference(type)

        bpy.ops.object.select_all(action='DESELECT')

        context.scene.view_settings.view_transform = 'Standard'
        self.report({'INFO'}, "KEN Anime Rig has been appended! | Scene Color Space set to Standard")
        return {'FINISHED'}


classes = (
            Append_TheAnimeRigKENFemale,
          )
          

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()