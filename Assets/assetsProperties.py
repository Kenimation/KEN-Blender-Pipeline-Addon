import bpy
from . import assetsDefs
from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatProperty, IntProperty, CollectionProperty

bpy.types.Scene.myProps = bpy.props.EnumProperty(default = "one",
                        items = [('one', 'Items', ''),
                                ('two', 'Libraries', ''),
                                ('three', 'Render', ''),
                                ])
bpy.types.Scene.libraries = bpy.props.EnumProperty(default = "one",
                        items = [('one', 'Materials', ''),
                                ('two', 'Lights', ''),
                                ('three', 'Cameras', ''),
                                ('four', 'Images', ''),
                                ])

bpy.types.Scene.new_coll_name = bpy.props.StringProperty(
    name="New Collection Name",
    description="New Collection Name",
)
bpy.types.Scene.select_coll= bpy.props.BoolProperty(
    name="Select All Collection",
    description="Select All Collection",
    update = assetsDefs.update_select_coll
)
bpy.types.Scene.hide_coll= bpy.props.BoolProperty(
    name="Hide All Collection",
    description="Hide All Collection",
    update = assetsDefs.update_hide_coll
)
bpy.types.Scene.myrig_ui_setting = bpy.props.BoolProperty(
    name="Rig UI Setting",
    description="Rig UI Setting",
    default=False,
)
bpy.types.Scene.ray_visility = bpy.props.BoolProperty(
    name="Ray Visility",
    description="Ray Visility",
    default=False,
)
bpy.types.Scene.hideconstraints = bpy.props.BoolProperty(
    name="Hide All Constraints",
    default=False,
    update = assetsDefs.update_hideconstraints
)
bpy.types.Scene.showconstraints = bpy.props.BoolProperty(
    name="Show Constraints",
    default=True,
)
bpy.types.Scene.showmodifier = bpy.props.BoolProperty(
    name="Show Modifier",
    default=True,
)
bpy.types.Scene.hide = bpy.props.BoolProperty(
    name="Hide",
    default=False,
    update = assetsDefs.update_hide
)
bpy.types.Scene.lightpath = bpy.props.BoolProperty(
    name="Light Path",
    description="Light Path",
    default=False,
)
bpy.types.Scene.finalrender = bpy.props.BoolProperty(
    name="Final Render",
    description="Final Render",
    default=False,
)
bpy.types.Scene.view = bpy.props.BoolProperty(
    name="View",
    description="View",
    default= True,
)
bpy.types.Scene.advanced_option = bpy.props.BoolProperty(
    name="Advanced Option",
    description="Advanced Option",
    default= True,
)
bpy.types.Scene.tools = bpy.props.BoolProperty(
    name="Enable Tools",
    description="Enable Tools",
    default= False,
)
bpy.types.Scene.object_properties = bpy.props.BoolProperty(
    name="Object Propertie",
    description="Object Propertie",
    default=False,
)
bpy.types.Scene.simulation = bpy.props.BoolProperty(
    name="Simulation Mode",
    description="Simulation Mode",
    default=False,
)

bpy.types.Scene.QuickImport = bpy.props.BoolProperty(
    name="Quick Import",
    description="Enable Quick Import",
    default= True
)

bpy.types.Scene.EditingTools = bpy.props.BoolProperty(
    name="Editing Tools",
    description="Enable Editing Tools",
    default= True
)

bpy.types.Scene.VertexGroupCount = bpy.props.IntProperty(
    name="Vertex Group Count",
    description="Number Vertex Group Add",
    default = 1
)

bpy.types.Scene.VertexGroupName = bpy.props.StringProperty(
    name="Vertex Group Name",
    description="Vertex Group Name",
    default= "Group"
)

bpy.types.Scene.VertexGroupTool = bpy.props.BoolProperty(
    name="Vertex Group Tool",
    description="Enable Vertex Group Tool",
    default= False
)

bpy.types.Scene.VertexGroupMiiror = bpy.props.BoolProperty(
    name="Miiror Vertex Group Loop",
    description="Enable Vertex Group Miiror",
    default= False
)

bpy.types.Scene.VertexGroupMenu = EnumProperty(
    default='one',
    items=[('one', 'Custom', ''),
           ('two', 'Body', ''),
            ])

bpy.types.Scene.FixName = bpy.props.StringProperty(
    name="Add Fix Name",
    description="Add Fix Name",
    default= ""
)

bpy.types.Scene.FixNameType = EnumProperty(
    default='one',
    items=[('one', 'Prefix', ''),
           ('two', 'Suffix', ''),
            ])


bpy.types.Scene.VertexGroupLR = EnumProperty(
    default='one',
    items=[('one', 'Left', ''),
           ('two', 'Right', ''),
            ])

bpy.types.Scene.VertexGroupPart = EnumProperty(
    default='Head',
    items=[('Head', 'Head', ''),
           ('Body', 'Body', ''),
            ('Arm', 'Arm', ''),
            ('Arm_Bend', 'Arm_Bend', ''),
            ('Hand', 'Hand', ''),
            ('Leg', 'Leg', ''),
            ('Leg_Bend', 'Leg_Bend', ''),
            ('Foot', 'Foot', ''),
            ])


bpy.types.Scene.Object_Type = EnumProperty(
    default='EMPTY',
    items=[('MESH', 'Mesh', ''),
           ('ARMATURE', 'Aemature', ''),
           ('EMPTY', 'Empty', ''),
            ('LIGHT', 'Light', ''),
            ('CAMERA', 'Camera', ''),
            ])

bpy.types.Scene.boneName = StringProperty()

bpy.types.Scene.OpenSimplify = BoolProperty(
    default = True, name = "")

bpy.types.Object.RIG_ID = bpy.props.StringProperty(
    name="RIG_ID",
    description="RIG_ID",
    default= ""
)

bpy.types.Object.RIG_Type = bpy.props.StringProperty(
    name="RIG_Type",
    description="RIG_Type",
    default= ""
)

bpy.types.Object.flipBone = BoolProperty(
    default=True)

bpy.types.Object.ArmWorld_r = BoolProperty(
    default=False)

bpy.types.Object.ArmWorld_l = BoolProperty(
    default=False)

bpy.types.Object.WristWorld_r = BoolProperty(
    default=False)

bpy.types.Object.WristWorld_l = BoolProperty(
    default=False)

bpy.types.Object.Arm_IK_Right = FloatProperty(
    min = 0, max = 1, default = 0, name = "Arm IK Right")

bpy.types.Object.Arm_IK_Left = FloatProperty(
    min = 0, max = 1, default = 0, name = "Arm IK Left")

bpy.types.Object.Leg_IK_Right = FloatProperty(
    min = 0, max = 1, default = 1, name = "Leg IK Right")

bpy.types.Object.Leg_IK_Left = FloatProperty(
    min = 0, max = 1, default = 1, name = "Leg IK Left")

bpy.types.Object.Arm_Stretch = FloatProperty(
    min = 0, max = 1, default = 0, name = "Arm Stretch")

bpy.types.Object.Leg_Stretch = FloatProperty(
    min = 0, max = 1, default = 1, name = "Leg Stretch")

bpy.types.Object.Facial = EnumProperty(
    default='two',
    items=[('one', 'No Face', ''),
            ('two', 'Face', ''),
            ],
            update=assetsDefs.update_Facial)

bpy.types.Object.ParentBones = EnumProperty(
    update = assetsDefs.update_ParentBones,
    default=None,
    items=[('R.Arm_Asset', 'R.Arm_Asset', ''),
            ('L.Arm_Asset', 'L.Arm_Asset', ''),
            ('Head', 'Head', ''),
            ('Chest', 'Chest', '')
            ])