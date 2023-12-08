import bpy
import os


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#             packed image && reload
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#              UI Property Implementation
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def bool_property(ly, rig, boolProp):
    if rig.get(boolProp) == 0:
        return ly.prop(rig, boolProp, icon = "LAYER_USED")
    else:
        return ly.prop(rig, boolProp, icon = "LAYER_ACTIVE")

def getAddonPreferences(context):
    preferences = context.preferences
    addon_prefs = preferences.addons[__package__].preferences
    return addon_prefs

def getPath(file):
    script_file = os.path.realpath(__file__)
    script_directory = os.path.dirname(script_file)
    file = os.path.join(os.path.dirname(script_directory), file)
    file = os.path.normpath(file)
    return file

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   update property
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def update_Blush(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('Blush')
    material_obj.material_slots[3].material.node_tree.nodes['Mix Shader'].inputs['Fac'].default_value = value

def update_PupilsThreshold(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('PupilsThreshold')
    material_obj.material_slots[1].material.node_tree.nodes['Eyes'].inputs['Pupils Threshold'].default_value = value

def update_SparkleEmission(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('SparkleEmission')
    material_obj.material_slots[1].material.node_tree.nodes['Eyes'].inputs['Sparkle Emission'].default_value = value

def update_PupilsEmission(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('PupilsEmission')
    material_obj.material_slots[1].material.node_tree.nodes['Eyes'].inputs['Pupils Emission'].default_value = value

def update_EyeType(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('EyeType')
    material_obj.material_slots[1].material.node_tree.nodes['Eyes'].inputs['Type'].default_value = value

def update_Pupil_Dot(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('Pupil_Dot')
    material_obj.material_slots[1].material.node_tree.nodes['Eyes'].inputs['Pupil Dot'].default_value = value

def update_Pupil_Dot_Size(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('Pupil_Dot_Size')
    material_obj.material_slots[1].material.node_tree.nodes['Eyes'].inputs['Pupil Dot Size'].default_value = value

def update_Pupil_Dot_Fallout(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('Pupil_Dot_Fallout')
    material_obj.material_slots[1].material.node_tree.nodes['Eyes'].inputs['Pupil Dot Fallout'].default_value = value

def update_EyeTextureType(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('EyeTextureType')
    material_obj.material_slots[1].material.node_tree.nodes['Eyes'].inputs['TextureType'].default_value = value

def update_EyesTwo(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('EyesTwo')
    material_obj.material_slots[1].material.node_tree.nodes['Eyes'].inputs['TwoDifferentEyes'].default_value = value
    material_obj.material_slots[2].material.node_tree.nodes['Eyeball'].inputs['Two'].default_value = value

def update_SparkleTextureType(self, context):
    rig = bpy.context.active_object
    material_obj = rig.children[0]
    value = rig.get('SparkleTextureType')
    material_obj.material_slots[1].material.node_tree.nodes['Eyes'].inputs['Sparkle Type'].default_value = value

def update_AntiLag(self, context):
    rig = bpy.context.active_object   
    value = rig.get('AntiLag')
    rig.pose.bones["Head_Properties"]["AntiLag"] = value

def update_HeadWorld(self, context):
    rig = bpy.context.active_object   
    value = rig.get('HeadWorld')
    rig.pose.bones["Head_Properties"]["Head world"] = value

def update_EyesTracker(self, context):
    rig = bpy.context.active_object   
    value = rig.get('EyesTracker')
    rig.pose.bones["Head_Properties"]["Eyes tracker"] = value

def update_FemaleMode(self, context):
    rig = bpy.context.active_object   
    value = rig.get('FemaleMode')
    rig.pose.bones["Head_Properties"]["Male/Female"] = value

def update_SecondLayer(self, context):
    rig = bpy.context.active_object   
    value = rig.get('SecondLayer')
    rig.pose.bones["Head_Properties"]["Second layer"] = value

def update_SmoothBends(self, context):
    rig = bpy.context.active_object   
    value = rig.get('SmoothBends')
    rig.pose.bones["Head_Properties"]["Smooth bends"] = value

def update_TextureDeform(self, context):
    rig = bpy.context.active_object   
    value = rig.get('TextureDeform')
    rig.pose.bones["Head_Properties"]["Texture deform"] = value

def update_Finger(self, context):
    rig = bpy.context.active_object   
    value = rig.get('Finger')
    rig.pose.bones["R.Arm_Properties"]["R.Arm_Fingers"] = value
    rig.pose.bones["L.Arm_Properties"]["L.Arm_Fingers"] = value

def update_SlimArms(self, context):
    rig = bpy.context.active_object   
    value = rig.get('SlimArms')
    rig.pose.bones["R.Arm_Properties"]["R.Arm_Steve/Alex"] = value
    rig.pose.bones["L.Arm_Properties"]["L.Arm_ Steve/Alex"] = value

def update_EyeBrowThickness(self, context):
    rig = bpy.context.active_object   
    value = rig.get('EyeBrowThickness')
    rig.pose.bones['EyebrowsThikness'].location[2] = value/10

def update_FullRiggedFace(self, context):
    rig = bpy.context.active_object   
    value = rig.get('FullRiggedFace')
    rig.pose.bones['FaceControls'].location[1] = value/10

def update_EyesFollow(self, context):
    rig = bpy.context.active_object   
    value = rig.get('EyesFollow')
    rig.pose.bones['EyesFollow'].location[2] = value/10

def update_Chibi(self, context):
    rig = bpy.context.active_object
    value = rig.get('Chibi')
    rig.pose.bones["Head_Properties"]["Chibi"] = value

def update_lattice(self, context):
    rig = bpy.context.active_object   
    value = rig.get('Lattice')
    rig.pose.bones["Head_Properties"]["Lattice"] = value

def update_FingerPlus(self, context):
    rig = bpy.context.active_object   
    value = rig.get('FingerPlus')
    rig.pose.bones["R.Arm_Properties"]["R.Arm_Fingers+"] = value
    rig.pose.bones["L.Arm_Properties"]["L.Arm_Fingers+"] = value

def update_NoFace(self, context):
    rig = bpy.context.active_object
    state = rig.get('NoFace')
    print(rig.NoFace)
    value = state * -0.575

    bones = ['Pupils_controller', 'Eyebrow_control.001', 'Eyebrow_control', 'R.eyebrow', 'L.Eyebrow', 'R.Eyebrow_bend',
             'L.Eyebrow_bend', 'Eyes_UP_DOWN', 'Bone.028', 'Bone.029', 'Bone.032', 'Bone.031', 'Bone.030']
    facePanel = ['BracketTop', 'BracketBottom']

    rig.FullRiggedFace = False
    rig.pose.bones["BracketTop"].location[1] = value
    for bones in bones:
        rig.data.bones[bones].hide = state
    for bones in facePanel:
        rig.data.bones[bones].hide_select = state

def update_ParentBones(self, context):
    scn = context.scene
    rig = context.object
    scn.boneName = rig.ParentBones

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def readTextPrefs(line):
    text_file = getPath("preferencesSettings.cfg")
    with open(text_file, "r") as file:
        data = file.read().splitlines()
        data = data[line-1]
        return data

def write_flip_bone(self, context):
    addon_prefs = getAddonPreferences(context)
    text_file = getPath("preferencesSettings.cfg")
    with open(text_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        data[3] = str(addon_prefs.flip_bone) + "\n"
        print(addon_prefs.flip_bone)

    # and write everything back
    with open(text_file, 'w') as file:
        file.writelines(data)

def write_armIK(self, context):
    addon_prefs = getAddonPreferences(context)
    text_file = getPath("preferencesSettings.cfg")
    with open(text_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        data[6] = addon_prefs.armIK + "\n"

    # and write everything back
    with open(text_file, 'w') as file:
        file.writelines(data)

def write_legIK(self, context):
    addon_prefs = getAddonPreferences(context)
    text_file = getPath("preferencesSettings.cfg")
    with open(text_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        data[9] = addon_prefs.legIK + "\n"

    # and write everything back
    with open(text_file, 'w') as file:
        file.writelines(data)

def write_finger(self, context):
    addon_prefs = getAddonPreferences(context)
    text_file = getPath("preferencesSettings.cfg")
    with open(text_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        data[12] = addon_prefs.finger + "\n"

    # and write everything back
    with open(text_file, 'w') as file:
        file.writelines(data)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   operator defs
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

