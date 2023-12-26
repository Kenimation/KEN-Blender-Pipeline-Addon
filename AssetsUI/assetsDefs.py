import bpy
import os

from ..Anime import AnimeProperties
from .. import addonPreferences


def users_collection(obj):
	"""Returns the collections/group of an object"""
	if hasattr(obj, "users_collection"):
		return obj.users_collection
	elif hasattr(obj, "users_group"):
		return obj.users_group

def collections():
	"""Returns group or collection object for 2.7 and 2.8"""
	if hasattr(bpy.data, "collections"):
		return bpy.data.collections
	else:
		return bpy.data.groups

def move_to_collection(obj, collection):

	"""Move out of all collections and into this specified one. 2.8 only"""
	for col in obj.users_collection:
		col.objects.unlink(obj)
	collection.objects.link(obj)
    
def update_mat_fake_use(self, context):
    if self.mat_fake_use == True:
        for mat in bpy.data.materials:
            mat.use_fake_user = True
    else:
        for mat in bpy.data.materials:
            mat.use_fake_user = False

def update_img_fake_use(self, context):
    if self.img_fake_use == True:
        for img in bpy.data.images:
            if img.has_data:
                img.use_fake_user = True
    else:
        for img in bpy.data.images:
            if img.has_data:
                img.use_fake_user = False

def update_hideoverlay(self, context):
    if self.hideoverlay == True:
        context.space_data.overlay.show_extras = True
        context.space_data.overlay.show_bones = True
    else:
        context.space_data.overlay.show_extras = False
        context.space_data.overlay.show_bones = False

def update_rendermodifier(self, context):
    obj = context.view_layer.objects.active
    modifiers = obj.modifiers
    if self.rendermodifier == True:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_render = False
    else:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_render = True

def update_editmodifier(self, context):
    obj = context.view_layer.objects.active
    modifiers = obj.modifiers
    if self.editmodifier == True:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_in_editmode = True
    else:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_in_editmode = False

def update_cagemodifier(self, context):
    obj = context.view_layer.objects.active
    modifiers = obj.modifiers
    if self.cagemodifier == True:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_on_cage = True
    else:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_on_cage = False

def update_hideconstraints(self, context):
    obj = context.object
    bones = context.active_pose_bone
    if obj.mode != 'POSE':
        con = obj.constraints
    if obj.mode == 'POSE':
        con = bones.constraints
    if self.hideconstraints == True:
        for id in con[:]:
            con[id.name].enabled = False
    else:
        for id in con[:]:
            con[id.name].enabled = True

def update_hidemodifier(self, context):
    obj = context.view_layer.objects.active
    modifiers = obj.modifiers
    if self.hidemodifier == True:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_viewport = False
    else:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_viewport = True

def update_hide(self, context):
    for ob in context.scene.objects:
        if ob.type == 'LIGHT':
            if self.hide == True:
                ob.hide_viewport = True
            else:
                ob.hide_viewport = False

def update_cam_focus_list(self, context):
    cam_list = []
    for cam in bpy.data.objects:
        cam_list.append(cam)
    cam = cam_list[context.scene.cam_index]
    if self.camlist == True:
        bpy.ops.photographer.create_focus_plane(camera=cam.name)
    else:
        bpy.ops.photographer.delete_focus_plane(camera=cam.name)
    return

def update_cam_focus(self, context):
    cam = context.view_layer.objects.active.name
    if self.cam == True:
        bpy.ops.photographer.create_focus_plane(camera=cam)
    else:
        bpy.ops.photographer.delete_focus_plane(camera=cam)
    return

def update_hide_coll(self, context):
    if self.hide_coll == True:
        for coll in bpy.data.collections:
            coll.hide_viewport = True
    else:
        for coll in bpy.data.collections:
            coll.hide_viewport = False

def update_select_coll(self, context):
    if self.select_coll == True:
        for coll in bpy.data.collections:
            coll.hide_select = True
    else:
        for coll in bpy.data.collections:
            coll.hide_select = False

def getPath(file):
    script_file = os.path.realpath(__file__)
    script_directory = os.path.dirname(script_file)
    file = os.path.join(os.path.dirname(script_directory), file)
    file = os.path.normpath(file)
    return file

def update_ParentBones(self, context):
    scn = context.scene
    rig = context.object
    scn.boneName = rig.ParentBones

def readTextPrefs(line):
    text_file = getPath("preferencesSettings.cfg")
    with open(text_file, "r") as file:
        data = file.read().splitlines()
        data = data[line-1]
        return data

def write_flip_bone(self, context):
    addon_prefs = addonPreferences.getAddonPreferences(context)
    text_file = getPath("preferencesSettings.cfg")
    with open(text_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        data[15] = str(addon_prefs.flip_bone) + "\n"
        print(addon_prefs.flip_bone)

    # and write everything back
    with open(text_file, 'w') as file:
        file.writelines(data)

def write_armIK(self, context):
    addon_prefs = addonPreferences.getAddonPreferences(context)
    text_file = getPath("preferencesSettings.cfg")
    with open(text_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        data[18] = addon_prefs.armIK + "\n"

    # and write everything back
    with open(text_file, 'w') as file:
        file.writelines(data)

def write_legIK(self, context):
    addon_prefs = addonPreferences.getAddonPreferences(context)
    text_file = getPath("preferencesSettings.cfg")
    with open(text_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        data[21] = addon_prefs.legIK + "\n"

    # and write everything back
    with open(text_file, 'w') as file:
        file.writelines(data)

def is_packed(img):
    try:
        return img.packed_files.values() == []
    except (AttributeError, KeyError, TypeError):
        return False

def safe_unpack(img): #unpacks relative to the file ONLY if the file is saved
    if img.packed_files:
        if bpy.data.is_saved:
            return img.unpack()
        else:
            return img.unpack(method='USE_ORIGINAL')

def update_Facial(self, context):
    rig = context.active_object
    if context.active_object.get("RIG_ID") in AnimeProperties.kenriglist[2]:
        for collection in bpy.data.collections:
                if rig.name in collection.objects:
                    parent_collection = collection
                    break

        if parent_collection is not None:
            for child_collection in parent_collection.children:
                if child_collection.name.split(".", 1)[0] == "Mesh":
                    for face_collection in child_collection.children:
                        if face_collection.name.split(".", 1)[0] == "Facials":
                            if self.Facial == 'one':
                                face_collection.hide_viewport = True
                                face_collection.hide_render = True
                            if self.Facial == 'two':
                                face_collection.hide_viewport = False
                                face_collection.hide_render = False
                            break

        if parent_collection is not None:
            for child_collection in parent_collection.children:
                if child_collection.name.split(".", 1)[0] == "LineArt_Mesh":
                    for mesh_collection in child_collection.children:
                        if mesh_collection.name.split(".", 1)[0] == "Facials_Line":
                            if self.Facial == 'one':
                                mesh_collection.hide_viewport = True
                                mesh_collection.hide_render = True
                            if self.Facial == 'two':
                                mesh_collection.hide_viewport = False
                                mesh_collection.hide_render = False
                            break
        if self.Facial == 'one':
            self.Facial_Bone = False
            self.Full_Facial_Bone = False
        if self.Facial == 'two':
            self.Facial_Bone = True
            self.Full_Facial_Bone = True
    elif context.active_object.get("RIG_ID") in AnimeProperties.kenriglist[0]:
        rig = context.active_object
        facePanel = ['BracketTop', 'BracketBottom']
        if rig.Facial == "one":
            value = -0.575
            rig.FullRiggedFace = False
            rig.pose.bones["BracketTop"].location[1] = value
            for bones in facePanel:
                rig.data.bones[bones].hide_select = False
        elif rig.Facial == "two":
            value = 0
            rig.pose.bones["BracketTop"].location[1] = value
            for bones in facePanel:
                rig.data.bones[bones].hide_select = True
