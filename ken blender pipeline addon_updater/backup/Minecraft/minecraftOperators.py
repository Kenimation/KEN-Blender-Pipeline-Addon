import bpy
import os

from ..AssetsUI import assetsDefs


from bpy.props import (StringProperty,
                        IntProperty)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                      operators
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def riggetpreference(type):
    # select the rig
    rig = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = rig
        # props from user preferencesSettings.cfg
            #   arm ik
            #   flip bone
    flip_bone = assetsDefs.readTextPrefs(4)
    if flip_bone == "False":
        rig.flipBone = 0
    else:
        rig.flipBone = 1
            #   arm ik
    arm_ik = assetsDefs.readTextPrefs(7)
    if arm_ik == "IK":
        arm_ik = 1
    else:
        arm_ik = 0
    rig.Arm_IK_Left = arm_ik
    rig.Arm_IK_Right = arm_ik
        # leg ik
    leg_ik = assetsDefs.readTextPrefs(10)
    if leg_ik == "IK":
        leg_ik = 1
    else:
        leg_ik = 0
    rig.Leg_IK_Left = leg_ik
    rig.Leg_IK_Right = leg_ik

    finger = assetsDefs.readTextPrefs(13)
    if finger == "On":
        rig.Finger = 1
    else:
        rig.Finger = 0

    if type == "default":
        pass
    elif type == "female":
        rig.SlimArms = True
        rig.FemaleMode = True
        rig.EyePosition = 0
        rig.EyeBrowPosition = 1
        bpy.data.materials["Skin (DO NoT REMOVE)"].node_tree.nodes["Skin Mat"].inputs[8].default_value = 1
        bpy.data.materials["Skin (DO NoT REMOVE)"].node_tree.nodes["Skin Mat"].inputs[5].default_value = (0.822786, 0.679543, 0.514918, 1)
        bpy.data.materials["Eyes"].node_tree.nodes["Eyes"].inputs[0].default_value = (0, 1, 0, 1)
        bpy.data.materials["Eyes"].node_tree.nodes["Eyes"].inputs[2].default_value = (0, 1, 0, 1)

        skin_path = bpy.data.images["skin"].filepath
        skin = skin_path.replace("Steve", "Alex")
        bpy.data.images["skin"].unpack()
        bpy.data.images["skin"].filepath = skin
        bpy.data.images["skin"].pack()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Append_TheRigKENLayout(bpy.types.Operator):
    bl_idname = "append.thomasrigkenlayout"
    bl_label = "KEN ThomasRig[Layout]"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        script_file = os.path.realpath(os.path.dirname(__file__))
        script_directory = os.path.dirname(script_file)
        script_directory = os.path.join(script_directory,"Assets" , "Rigs", "Minecraft")
        script_directory = os.path.normpath(script_directory)

        blendfile = os.path.join(script_directory, "KEN Minecraft Rig Layout v1.0.blend")
        section = "Collection"
        obj = "Append KEN Layout Rig"
        filepath  = os.path.join(blendfile,section,obj)
        directory = os.path.join(blendfile,section)
        filename  = obj
        bpy.ops.wm.append(filepath=filepath,filename=filename,directory=directory,link=False,active_collection=False)

        # select the rig
        type = "default"
        riggetpreference(type)

        bpy.ops.object.select_all(action='DESELECT')

        self.report({'INFO'}, "KEN Layout Rig has been appended!")
        return {'FINISHED'}

class Append_TheRigKENEditDefault(bpy.types.Operator):
    bl_idname = "append.thomasrigkenremastereddefault"
    bl_label = "KEN ThomasRig Remastered[Default]"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        script_file = os.path.realpath(os.path.dirname(__file__))

        script_directory = os.path.dirname(script_file)
        script_directory = os.path.join(script_directory,"Assets" , "Rigs", "Minecraft")
        script_directory = os.path.normpath(script_directory)

        blendfile = os.path.join(script_directory, "KEN Minecraft Rig Remastered v1.0.blend")
        section = "Collection"
        obj = "Append KEN Remastered Rig"
        filepath  = os.path.join(blendfile,section,obj)
        directory = os.path.join(blendfile,section)
        filename  = obj
        bpy.ops.wm.append(filepath=filepath,filename=filename,directory=directory,link=False,active_collection=False)

        # select the rig
        type = "default"
        riggetpreference(type)

        bpy.ops.object.select_all(action='DESELECT')

        self.report({'INFO'}, "KEN ThomasRig Remastered has been appended!")
        return {'FINISHED'}

class Append_TheRigKENEditFemale(bpy.types.Operator):
    bl_idname = "append.thomasrigkenremasteredfemale"
    bl_label = "KEN ThomasRig Remastered[Female]"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        script_file = os.path.realpath(os.path.dirname(__file__))

        script_directory = os.path.dirname(script_file)
        script_directory = os.path.join(script_directory,"Assets" , "Rigs", "Minecraft")
        script_directory = os.path.normpath(script_directory)

        blendfile = os.path.join(script_directory, "KEN Minecraft Rig Remastered v1.0.blend")
        section = "Collection"
        obj = "Append KEN Remastered Rig"
        filepath  = os.path.join(blendfile,section,obj)
        directory = os.path.join(blendfile,section)
        filename  = obj
        bpy.ops.wm.append(filepath=filepath,filename=filename,directory=directory,link=False,active_collection=False)

        type = "female"
        riggetpreference(type)

        bpy.ops.object.select_all(action='DESELECT')

        self.report({'INFO'}, "KEN ThomasRig Remastered has been appended!")
        return {'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


classes = (
            Append_TheRigKENLayout,
            Append_TheRigKENEditDefault,
            Append_TheRigKENEditFemale,
          )

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()