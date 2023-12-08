import bpy
import os

from . import minecraftDefs


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

class OPEN_ADDON_PREFS_OF_ADDON(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "open.addonprefsofaddon"
    bl_label = ""
    bl_description = "opens the user preferences for this addon"

    id_name: bpy.props.StringProperty()

    def execute(self, context):
        bpy.ops.screen.userpref_show()
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers['WinMan']['addon_search'] = "KEN Pipeline"
        bpy.ops.preferences.addon_show(module = "KEN Blender Pipeline")
        bpy.ops.preferences.addon_expand(module = "KEN Blender Pipeline")
        
        return {'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class IMAGEPACK(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "packimg.thomasminecraftrig"
    bl_label = ""
    bl_description = "Pack/Unpack the skin texture"

    id_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        img = bpy.data.images[self.id_name]
        if minecraftDefs.is_packed(img):
            img.pack()
        else:
            minecraftDefs.safe_unpack(img)
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)
        return {'FINISHED'}

class IMAGERELOAD(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "reloadimg.thomasminecraftrig"
    bl_label = ""
    bl_description = "reload the skin texture"

    id_name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        img = bpy.data.images[self.id_name]
        img.reload()
        print("image reloaded")
        return {'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Append_TheRigKENLayout(bpy.types.Operator):
    bl_idname = "append.thomasrigkenlayout"
    bl_label = "KEN ThomasRig[Layout]"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        script_file = os.path.realpath(os.path.dirname(__file__))
        script_directory = os.path.dirname(script_file)
        script_directory = os.path.join(script_directory, "Rigs", "Minecraft")
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

        print("KEN Layout Rig has been appended!")
        return {'FINISHED'}

class Append_TheRigKENEditDefault(bpy.types.Operator):
    bl_idname = "append.thomasrigkenremastereddefault"
    bl_label = "KEN ThomasRig Remastered[Default]"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        script_file = os.path.realpath(os.path.dirname(__file__))

        script_directory = os.path.dirname(script_file)
        script_directory = os.path.join(script_directory, "Rigs", "Minecraft")
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

        print("KEN ThomasRig Remastered has been appended!")
        return {'FINISHED'}

class Append_TheRigKENEditFemale(bpy.types.Operator):
    bl_idname = "append.thomasrigkenremasteredfemale"
    bl_label = "KEN ThomasRig Remastered[Female]"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        script_file = os.path.realpath(os.path.dirname(__file__))

        script_directory = os.path.dirname(script_file)
        script_directory = os.path.join(script_directory, "Rigs", "Minecraft")
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

        print("KEN ThomasRig Remastered has been appended!")
        return {'FINISHED'}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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
            selected_objects = bpy.context.selected_objects
            rig = bpy.context.active_object

            for object in selected_objects:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = object

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

class SyncAddonPrefs(bpy.types.Operator):
    bl_idname = "addonprefs.sync"
    bl_label = "sync. addon prefs"
    bl_options = {'REGISTER', 'UNDO'}

    

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        if minecraftDefs.readTextPrefs(4) == "True":
            addon_prefs.flip_bone = True
        else:
            addon_prefs.flip_bone = False
        addon_prefs.armIK = minecraftDefs.readTextPrefs(7)
        addon_prefs.legIK = minecraftDefs.readTextPrefs(10)
        addon_prefs.finger = minecraftDefs.readTextPrefs(13)
        
        return {'FINISHED'}


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


classes = (OPEN_ADDON_PREFS_OF_ADDON,
            IMAGEPACK,
            Append_TheRigKENLayout,
            Append_TheRigKENEditDefault,
            Append_TheRigKENEditFemale,
            IMAGERELOAD,
            ParentObjectsToRig,
            SyncAddonPrefs,
          )

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()