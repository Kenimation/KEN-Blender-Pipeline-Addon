import bpy
from . import minecraftDefs
from bpy.props import (BoolProperty,
                       FloatProperty,
                       EnumProperty,
                       StringProperty,
                       IntProperty,
                       )
import os

class EnumFromFolder:
    def __init__(self, filepath=None, fileformats=".blend"):
        self.filenames = ""
        if filepath is not None:
            self.fileloc = os.path.join(os.path.dirname(os.path.dirname(__file__)), filepath)
        else:
            self.fileloc = os.path.dirname(os.path.dirname(__file__))
        for files in os.listdir(self.fileloc):
            formates = fileformats.split(' ')
            for formats in formates:
                if formats in files:
                    files = files.replace(formats, "")
                    if self.filenames != "":
                        self.filenames = self.filenames + "%%" + files
                    else:
                        self.filenames = files

    def createEnum(self, objectName, name=None, default=None, update=None):
        items = self.filenames.split('%%')
        Enum = "bpy.props.EnumProperty("
        if name is not None:
            Enum = Enum + f"name={name}, "
        if default is not None:
            Enum = Enum + f"default = {default},"
        Enum = Enum + "items = ["
        i = 0
        for item in items:
            if i != len(items) - 1:
                Enum = Enum + f"('{item}', '{item}', '{item}'),"
            else:
                Enum = Enum + f"('{item}', '{item}', '{item}')"
            i += 1
        Enum = Enum + "]"
        if update is not None:
            Enum = Enum + f",update={update}"
        Enum = Enum + ")"
        return Enum

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                  Bool Propertry 
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

bpy.types.Object.AntiLag = BoolProperty(
    default=True, update=minecraftDefs.update_AntiLag)

bpy.types.Object.HeadWorld = BoolProperty(
    default=False, update=minecraftDefs.update_HeadWorld)

bpy.types.Object.EyesTracker = BoolProperty(
    default=False, update=minecraftDefs.update_EyesTracker)

bpy.types.Object.SlimArms = BoolProperty(
    default=False, update=minecraftDefs.update_SlimArms)

bpy.types.Object.FemaleMode = BoolProperty(
    default=False, update=minecraftDefs.update_FemaleMode)

bpy.types.Object.SecondLayer = BoolProperty(
    default=False, update=minecraftDefs.update_SecondLayer)

bpy.types.Object.SmoothBends = BoolProperty(
    default=False, update=minecraftDefs.update_SmoothBends)

bpy.types.Object.TextureDeform = BoolProperty(
    default=False, update=minecraftDefs.update_TextureDeform)

bpy.types.Object.Finger = BoolProperty(
    default=False, update=minecraftDefs.update_Finger)

bpy.types.Object.FullRiggedFace = BoolProperty(
    default=False, update=minecraftDefs.update_FullRiggedFace)

bpy.types.Object.EyesFollow = BoolProperty(
    default=True, update=minecraftDefs.update_EyesFollow)

bpy.types.Object.Chibi = BoolProperty(
    default=False, update=minecraftDefs.update_Chibi)

bpy.types.Object.FingerPlus = BoolProperty(
    default=False, update=minecraftDefs.update_FingerPlus)

bpy.types.Object.Pupil_Dot = BoolProperty(
    default=True, update=minecraftDefs.update_Pupil_Dot)

bpy.types.Object.Jacket = BoolProperty(
    default = False)

bpy.types.Object.JacketLattice = BoolProperty(
    default = True)

bpy.types.Object.SmartMovement = BoolProperty(
    default = True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                  Float Property
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

bpy.types.Object.Blush = FloatProperty(
    min=0, max=1, default=0, update=minecraftDefs.update_Blush)

bpy.types.Object.EyePosition = FloatProperty(
    min=0, max=1, default=0.5, name = "EyePosition")

bpy.types.Object.EyeBrowPosition = FloatProperty(
    min=0, max=1, default=0.5, name = "EyeBrowPosition")

bpy.types.Object.EyeBrowThickness = FloatProperty(
    min=0, max=1, default=0.25, update=minecraftDefs.update_EyeBrowThickness)

bpy.types.Object.SmartMovement_Arm = FloatProperty(
    min = 0, max = 1, default = 0, name = "Influence On Arm")

bpy.types.Object.SmartMovement_Leg = FloatProperty(
    min = 0, max = 1, default = 0, name = "Influence On Leg")

bpy.types.Object.SmartMovement_Waist = FloatProperty(
    min = 0, max = 1, default = 0, name = "Influence On Waist")

bpy.types.Object.SmartMovement_HeadDeformations = FloatProperty(
    min = 0, max = 1, default = 0.5, name = "Influence On Head")

bpy.types.Object.SparkleEmission = FloatProperty(
    min=0, max=15, default=5, update=minecraftDefs.update_SparkleEmission)

bpy.types.Object.PupilsEmission = FloatProperty(
    min=0, max=15, default=0, update=minecraftDefs.update_PupilsEmission)

bpy.types.Object.PupilsThreshold = FloatProperty(
    min=0, max=1, default=0.1, update=minecraftDefs.update_PupilsThreshold)

bpy.types.Object.Pupil_Dot_Size = FloatProperty(
    min=0, max=1, default=0.35, update=minecraftDefs.update_Pupil_Dot_Size)

bpy.types.Object.Pupil_Dot_Fallout = FloatProperty(
    min=0, max=1, default=0.1, update=minecraftDefs.update_Pupil_Dot_Fallout)

bpy.types.Object.EyeTextureType = IntProperty(
    min=0, max=3, default=2, update=minecraftDefs.update_EyeTextureType)

bpy.types.Object.SparkleTextureType = IntProperty(
    min=0, max=10, default=2, update=minecraftDefs.update_SparkleTextureType)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                  Enum Property
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

bpy.types.Object.ken_mc_rig = bpy.props.BoolProperty(
    name="KEN Remastered v1.0_Rig",
    description="KEN Remastered v1.0 Properties",
    default=False,
)

bpy.types.Scene.myrig = bpy.props.EnumProperty(default = "one",
                        items = [('one', 'Design', ''),
                                ('two', 'Materials', ''),
                                ])
bpy.types.Scene.myrigpose = bpy.props.EnumProperty(default = "three",
                        items = [('one', 'Design', ''),
                                ('two', 'Materials', ''),
                                ('three', 'Posing', ''),
                                ('four', 'Animating', ''),
                                ])

bpy.types.Scene.riglayout = bpy.props.EnumProperty(default = "one",
                        items = [('one', 'Layout', ''),
                                ('two', 'Posing', ''),
                                ])

bpy.types.Scene.riglayoutpose = bpy.props.EnumProperty(default = "three",
                        items = [('one', 'Layout', ''),
                                ('two', 'Posing', ''),
                                ('three', 'Animating', ''),
                                ])

bpy.types.Object.CPpos = EnumProperty(
    default='two',
    items=[('one', 'Left', ''),
           ('two', 'Right', '')
           ])

bpy.types.Object.EyeType = EnumProperty(
    update=minecraftDefs.update_EyeType,
    default='two',
    items=[('one', 'None', ''),
           ('two', 'Textures', ''),
           ])

bpy.types.Object.EyesTwo = EnumProperty(
    update=minecraftDefs.update_EyesTwo,
    default='one',
    items=[('one', 'One', ''),
           ('two', 'Two', ''),
           ])

bpy.types.Object.solid = EnumProperty(
    default='0',
    items=[('0', 'Skin', ''),
           ('1', 'Solid', '')
           ]
           )

bpy.types.Object.UIParent = EnumProperty(
    default='one',
    items=[('one', 'Head', ''),
           ('two', 'Upper body', ''),
           ('three', 'Root', '')
           ])

