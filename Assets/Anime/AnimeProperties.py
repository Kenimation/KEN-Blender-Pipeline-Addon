import bpy
from bpy.props import (BoolProperty,
                       FloatProperty,
                       EnumProperty,
                       StringProperty,
                       IntProperty,
                       FloatVectorProperty,
                       )
import os
from . import AnimeDefs

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                  Bool Propertry 
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                  Float Property
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

bpy.types.Object.MadShadow = IntProperty(
    min=0, max=2, default=1, name = "Mad Shadow")

bpy.types.Object.EyelidsHardShadow = IntProperty(
    min=0, max=3, default=0, name = "Eyelids Hard Shadow")

bpy.types.Object.EyelidsShadow = IntProperty(
    min=0, max=4, default=1, name = "Eyelids Shadow")

bpy.types.Object.EyeBottomShadow = BoolProperty(
    default=True, name = "Eye Bottom")

bpy.types.Object.FingerShadow = BoolProperty(
    default=False, name = "Finger")

bpy.types.Object.NeckShadow = BoolProperty(
    default=False, name = "Neck")

bpy.types.Object.Sub_ID_Lock = BoolProperty(
    default=False)

bpy.types.Object.Sub_ID = StringProperty(
    default="Character - Default", name = "Sub_ID", update=AnimeDefs.update_Sub_ID)

bpy.types.Object.MixHue = FloatProperty(
    min=0, max=1, default=0.5, name = "Mix", update=AnimeDefs.update_MixHue)

bpy.types.Object.TintColor = FloatVectorProperty(
        subtype='COLOR',
        default=(1.0, 1.0, 1.0, 1.0),
        size=4,
        min=0.0,
        max=1.0,
        name = "TintColor",
        update=AnimeDefs.update_TintColor)

bpy.types.Object.Saturation = FloatProperty(
    min=0, max=2, default=1, name = "Saturation", update=AnimeDefs.update_Saturation)

bpy.types.Object.Lightness = FloatProperty(
    min=0, max=2, default=1, name = "Lightness", update=AnimeDefs.update_Lightness)


bpy.types.Object.Rimlight = FloatProperty(
    min=0, max=1, default=0, name = "Rim light", update=AnimeDefs.update_Rimlight)

bpy.types.Object.RimlightColor = FloatVectorProperty(
        subtype='COLOR',
        default=(1.0, 1.0, 1.0, 1.0),
        size=4,
        min=0.0,
        max=1.0,
        name = "Rim light Color"
        , update=AnimeDefs.update_RimlightColor)

bpy.types.Object.RimlightShadow = FloatProperty(
    min=0, max=1, default=1, name = "Rim light Shadow", update=AnimeDefs.update_RimlightShadow)

bpy.types.Object.RimlightThickness = FloatProperty(
    min=0, max=1000, default=100, name = "Rim light Thickness", update=AnimeDefs.update_RimlightThickness)

bpy.types.Object.RimlightRadius = FloatProperty(
    min=0, max=1, default=0.1, name = "Rim light Radius", update=AnimeDefs.update_RimlightRadius)

bpy.types.Object.ShadowPosition = FloatProperty(
    min=0, max=1, default=0.5, name = "Shadow Position", update=AnimeDefs.update_ShadowPosition)

bpy.types.Object.CastShadow = FloatProperty(
    min=0, max=1, default=0, name = "Cast Shadow", update=AnimeDefs.update_CastShadow)

bpy.types.Object.SmoothShadow = FloatProperty(
    min=0.001, max=1, default=0.001, name = "Smooth Shadow", update=AnimeDefs.update_SmoothShadow)

bpy.types.Object.HueColorize = BoolProperty(
    default=False, name = "Hue Colorize")

bpy.types.Object.AllRimlight = BoolProperty(
    default=False, name = "All Rim light")

bpy.types.Object.AllShadow = BoolProperty(
    default=False, name = "All Shadow")

bpy.types.Object.Blush = BoolProperty(
    default=False, name = "Blush")

bpy.types.Object.MeshSelect = BoolProperty(
    default=True, name = "Mesh Select", update=AnimeDefs.update_MeshSelect)

bpy.types.Object.HairMaterial = BoolProperty(
    default=True, name = "Hair Shader")

bpy.types.Object.EyesMaterial = BoolProperty(
    default=True, name = "Eyes Shader")

bpy.types.Object.MetalMaterial = BoolProperty(
    default=True, name = "Metal Shader")

bpy.types.Object.BaseMaterial = BoolProperty(
    default=True, name = "Base Shader")

bpy.types.Object.SkinMaterial = BoolProperty(
    default=True, name = "Skin Shader")

bpy.types.Object.SmoothShade = BoolProperty(
    default=True, name = "Smooth Shade")

bpy.types.Object.FacialDesign = BoolProperty(
    default=True, name = "Facial Design")

bpy.types.Object.MeshDesign = BoolProperty(
    default=True, name = "Mesh Design")

bpy.types.Object.SmartEye = BoolProperty(
    default=True, name = "Smart Eye")

bpy.types.Object.DirtLine = BoolProperty(
    default=False, name = "Dirt Line")

bpy.types.Object.FingerLine = BoolProperty(
    default=False, name = "Finger Line")

bpy.types.Object.BandedLine = BoolProperty(
    default=True, name = "Banded Cloth")

bpy.types.Object.ClothLine = BoolProperty(
    default=True, name = "Cloth Line")

bpy.types.Object.ArmorLine = BoolProperty(
    default=True, name = "Armor Line")

bpy.types.Object.HairLine = BoolProperty(
    default=True, name = "Hair Line")

bpy.types.Object.DetailLine = BoolProperty(
    default=True, name = "Detail Line")

bpy.types.Object.MadLine = BoolProperty(
    default=True, name = "Mad Line")

bpy.types.Object.EyebrowLine = BoolProperty(
    default=True, name = "Eyebrows Line")

bpy.types.Object.LipLine = BoolProperty(
    default=True, name = "Lip Line")

bpy.types.Object.NoseLine = BoolProperty(
    default=True, name = "Nose Line")

bpy.types.Object.FaceLine = BoolProperty(
    default=True, name = "Face Line")

bpy.types.Object.LineArtMesh = BoolProperty(
    default=True, name = "LineArt", update=AnimeDefs.update_LineArtMesh)

bpy.types.Object.LineArt = BoolProperty(
    default=True, name = "LineArt", update=AnimeDefs.update_LineArt)

bpy.types.Object.NoseType = IntProperty(
    min=1, max=3, default=1, name = "Nose Type")

bpy.types.Object.FaceLineType = IntProperty(
    min=1, max=3, default=3, name = "Face Line Type")

bpy.types.Object.MainLineArt = IntProperty(
    min=1, max=10, default=1, name = "Thickness")

bpy.types.Object.PinkLineArt = IntProperty(
    min=1, max=10, default=1, name = "Thickness")

bpy.types.Object.EyelashType = IntProperty(
    min=1, max=4, default=1, name = "Eyelash Type")

bpy.types.Object.EyebrowsPos = FloatProperty(
    min=0.1, max=2, default=1, name = "Eyebrows Position")

bpy.types.Object.EyebrowsThickness = FloatProperty(
    min=0.1, max=2, default=0.75, name = "Eyebrows Thickness")

bpy.types.Object.EyebrowsWidth = FloatProperty(
    min=0.1, max=2, default=1, name = "Eyebrows Width")

bpy.types.Object.EyebrowsLineType= IntProperty(
    min=1, max=2, default=1, name = "Eyebrows Line Type")

bpy.types.Object.EyebrowsType= IntProperty(
    min=1, max=2, default=1, name = "Eyebrows Type")

bpy.types.Object.RigScale = FloatProperty(
    min=1, max=15, default=1, name = "Rig Scale", update = AnimeDefs.update_rig_scale)

bpy.types.Object.HeadSize = FloatProperty(
    min=0.5, max=2, default=1, name = "Head Size")

bpy.types.Object.BodySize = FloatProperty(
    min=0.1, max=2, default=1, name = "Body Length")

bpy.types.Object.BreastSize = FloatProperty(
    min=0.1, max=2, default=1, name = "Breast Size")

bpy.types.Object.ShoulderWidth = FloatProperty(
    min=0.5, max=2, default=1, name = "Shoulder Width")

bpy.types.Object.BodyWidth3 = FloatProperty(
    min=0.5, max=2, default=1, name = "Chest Width")

bpy.types.Object.BodyWidth2 = FloatProperty(
    min=0.5, max=2, default=1, name = "Body Width")

bpy.types.Object.BodyWidth1 = FloatProperty(
    min=0.5, max=2, default=1, name = "Waist Width")

bpy.types.Object.ArmSize = FloatProperty(
    min=0.1, max=2, default=1, name = "Arm Length")

bpy.types.Object.LegWidth = FloatProperty(
    min=0.5, max=2, default=1, name = "Leg Width")

bpy.types.Object.LegSize = FloatProperty(
    min=0.1, max=2, default=1, name = "Leg Length")

bpy.types.Object.ButtSize = FloatProperty(
    min=0.5, max=1.5, default=1, name = "Butt Size")

bpy.types.Object.NailLength = FloatProperty(
    min=0.1, max=2, default=1, name = "Nail Length")

bpy.types.Object.NailSharp = FloatProperty(
    min=0, max=1, default=0, name = "Nail Sharp")

bpy.types.Object.BodyMuscle = FloatProperty(
    min=0, max=1, default=1, name = "Body Muscle")

bpy.types.Object.ArmMuscle = FloatProperty(
    min=0, max=1, default=1, name = "Arm Muscle")

bpy.types.Object.LegMuscle = FloatProperty(
    min=0, max=1, default=1, name = "Leg Muscle")

bpy.types.Object.FootSize = FloatProperty(
    min=0.5, max=2, default=1, name = "Foot Length")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                  Bool Property
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
bpy.types.Object.ken_anime_rig = bpy.props.BoolProperty(
    name="KEN Anime Rig",
    description="KEN Anime Rig Properties",
    default=False,
)

bpy.types.Object.Main_Bone = BoolProperty(
    default=True, name = "Main Bone", update = AnimeDefs.update_Main_Bone)

bpy.types.Object.Facial_Bone = BoolProperty(
    default=True, name = "Facial", update = AnimeDefs.update_Facial_Bone)

bpy.types.Object.Full_Facial_Bone = BoolProperty(
    default=False, name = "Full Facial", update = AnimeDefs.update_Full_Facial_Bone)

bpy.types.Object.Hair_Bone = BoolProperty(
    default=True, name = "Hair", update = AnimeDefs.update_Hair_Bone)

bpy.types.Object.Full_Hair_Bone = BoolProperty(
    default=False, name = "Full Hair", update = AnimeDefs.update_Full_Hair_Bone)

bpy.types.Object.BonesCollection = BoolProperty(
    default=False, name = "Bones Collection")

kenriglist = ["KENRemastered", "KENLayout", "KenAnime"]
registered_name = ["KENCER USER", "Minecraft2024", "Anime2024 Project - Valkyrie"]
bone_collections = ["FFD", "Head", "Body", "R.Arm", "L.Arm", "R.Hand", "L.Hand","R.Leg","L.Leg","R.Foot","L.Foot"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                  Enum Property
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

bpy.types.Scene.myanimerig = EnumProperty(
    default='Setup',
    items=[('Setup', 'Setup', ''),
            ('Design', 'Design', ''),
            ])

bpy.types.Scene.myanimerigpose = EnumProperty(
    default='Posing',
    items=[('Setup', 'Setup', ''),
            ('Design', 'Design', ''),
            ('Posing', 'Posing', ''),
            ])

bpy.types.Scene.myanimerigAddition = EnumProperty(
    default='Setup',
    items=[('Setup', 'Setup', ''),
            ('Design', 'Design', ''),
            ('Addition', 'Addition', ''),
            ])

bpy.types.Scene.myanimerigposeAddition = EnumProperty(
    default='Posing',
    items=[('Setup', 'Setup', ''),
            ('Design', 'Design', ''),
            ('Posing', 'Posing', ''),
            ('Addition', 'Addition', ''),
            ])

bpy.types.Object.DesignClasses = EnumProperty(
    default='Mesh',
    items=[('Mesh', 'Mesh', ''),
            ('Shader', 'Shader', ''),
            ])

bpy.types.Object.SetupClasses = EnumProperty(
    default='LineArt',
    items=[('LineArt', 'LineArt', ''),
            ('Shadow', 'Shadow', ''),
            ])

bpy.types.Object.NoseLineType = EnumProperty(
    default='Straight',
    items=[('Straight', 'Straight', ''),
            ('Slash', 'Slash', ''),
            ])

bpy.types.Object.NoseShadow = EnumProperty(
    default='one',
    items=[('one', 'None', ''),
            ('two', 'Right', ''),
            ('three', 'Left', ''),
            ])

bpy.types.Object.SubShadow = EnumProperty(
    default='one',
    items=[('one', 'OFF', ''),
            ('two', 'ON', ''),
            ])

bpy.types.Object.Teeth = EnumProperty(
    default='one',
    items=[('one', 'Flat', ''),
            ('two', 'Rough', ''),
            ])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                  String Propertry 
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

