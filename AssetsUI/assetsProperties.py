import bpy
from . import assetsFunctions
from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatProperty, IntProperty, CollectionProperty

bpy.types.Scene.myProps = bpy.props.EnumProperty(default = "one",
                        items = [('one', 'Items', ''),
                                ('two', 'Libraries', ''),
                                ('three', 'Render', ''),
                                ])
bpy.types.Scene.mytools = bpy.props.EnumProperty(default = "one",
                        items = [('one', 'Materials', ''),
                                ('two', 'Lights', ''),
                                ('three', 'Cameras', ''),
                                ('four', 'Images', ''),
                                ])
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

bpy.types.Scene.mat_surface = bpy.props.BoolProperty(
    name="Toggle Materials Surface",
    description="Toggle Materials Surface",
)

bpy.types.Scene.mat_fake_use = bpy.props.BoolProperty(
    name="Toggle Materials Fake_User",
    description="Toggle Materials Fake_User",
    update = assetsFunctions.update_mat_fake_use
)
bpy.types.Scene.img_fake_use = bpy.props.BoolProperty(
    name="Toggle Images Fake_User",
    description="Toggle Images Fake_User",
    update = assetsFunctions.update_img_fake_use
)

bpy.types.Scene.cam_save = bpy.props.BoolProperty(
    name="Enable Camera Save List",
    description="Enable Camera Save List",
    default= True
)
bpy.types.Scene.cam_shake = bpy.props.BoolProperty(
    name="Enable Camera Shakify",
    description="Enable Camera Shakify",
    default= True
)
bpy.types.Scene.cam_quick = bpy.props.BoolProperty(
    name="Enable Quick Camera",
    description="Enable Quick Camera",
    default= True
)
bpy.types.Scene.bsdf = bpy.props.BoolProperty(
    name="Enable Principled BSDF",
    description="Enable Principled BSDF",
    default= True
)
bpy.types.Scene.img_tex = bpy.props.BoolProperty(
    name="Enable Image Texture",
    description="Enable Image Texture",
    default= True
)
bpy.types.Scene.tools = bpy.props.BoolProperty(
    name="Enable Tools",
    description="Enable Tools",
)
bpy.types.Scene.scene_mat = bpy.props.BoolProperty(
    name="Switch Materials",
    description="Switch Scene Material",
)
bpy.types.Scene.new_coll_name = bpy.props.StringProperty(
    name="New Collection Name",
    description="New Collection Name",
)
bpy.types.Scene.select_coll= bpy.props.BoolProperty(
    name="Select All Collection",
    description="Select All Collection",
    update = assetsFunctions.update_select_coll
)
bpy.types.Scene.hide_coll= bpy.props.BoolProperty(
    name="Hide All Collection",
    description="Hide All Collection",
    update = assetsFunctions.update_hide_coll
)
bpy.types.Scene.marker_name = bpy.props.StringProperty(
    name="Marker Name",
    description="Marker Name",
)

bpy.types.Scene.marker = bpy.props.BoolProperty(
    name="Enable Marker",
    description="Enable Marker",
)
bpy.types.Scene.mark_index = bpy.props.IntProperty(
    name="marker_index",
    description="marker_index",
)
bpy.types.Scene.coll_index = bpy.props.IntProperty(
    name="collection_index",
    description="collection_index",
)
bpy.types.Scene.cam_index = bpy.props.IntProperty(
    name="camera_index",
    description="camera_index",
)
bpy.types.Scene.light_index = bpy.props.IntProperty(
    name="light_index",
    description="light_index",
)
bpy.types.Scene.mat_index = bpy.props.IntProperty(
    name="mat_index",
    description="mat_index",
)
bpy.types.Scene.particles_index = bpy.props.IntProperty(
    name="Particles_index",
    description="particles_index",
)
bpy.types.Scene.image_index = bpy.props.IntProperty(
    name="Image_index",
    description="image_index",
)
bpy.types.Scene.myrig_ui_setting = bpy.props.BoolProperty(
    name="Rig UI Setting",
    description="Rig UI Setting",
    default=False,
)
bpy.types.Scene.ken_rig = bpy.props.BoolProperty(
    name="KEN Remastered v1.0_Rig",
    description="KEN Remastered v1.0 Properties",
    default=False,
)
bpy.types.Scene.ray_visility = bpy.props.BoolProperty(
    name="Ray Visility",
    description="Ray Visility",
    default=False,
)
bpy.types.Scene.editmodifier = bpy.props.BoolProperty(
    name="Show All Edit Modifier",
    default=False,
    update = assetsFunctions.update_editmodifier
)
bpy.types.Scene.cagemodifier = bpy.props.BoolProperty(
    name="Show All Cage Modifier",
    default=False,
    update = assetsFunctions.update_cagemodifier
)
bpy.types.Scene.rendermodifier = bpy.props.BoolProperty(
    name="Render All Modifier",
    default=False,
    update = assetsFunctions.update_rendermodifier
)
bpy.types.Scene.hideconstraints = bpy.props.BoolProperty(
    name="Hide All Constraints",
    default=False,
    update = assetsFunctions.update_hideconstraints
)
bpy.types.Scene.hideoverlay = bpy.props.BoolProperty(
    name="Hide Overlay",
    default=True,
    update = assetsFunctions.update_hideoverlay
)
bpy.types.Scene.imagepreview = bpy.props.BoolProperty(
    name="Show Image Preview",
    default=True,
)
bpy.types.Scene.expandlight = bpy.props.BoolProperty(
    name="Expand All Lights",
    default=False,
)

bpy.types.Scene.showconstraints = bpy.props.BoolProperty(
    name="Show Constraints",
    default=True,
)
bpy.types.Scene.showmodifier = bpy.props.BoolProperty(
    name="Show Modifier",
    default=True,
)
bpy.types.Scene.hidemodifier = bpy.props.BoolProperty(
    name="Hide All Modifier",
    default=False,
    update = assetsFunctions.update_hidemodifier
)
bpy.types.Scene.hide = bpy.props.BoolProperty(
    name="Hide",
    default=False,
    update = assetsFunctions.update_hide
)
bpy.types.Scene.cam = bpy.props.BoolProperty(
    name="Cam Focus",
    default=False,
    update = assetsFunctions.update_cam_focus
)
bpy.types.Scene.camlist = bpy.props.BoolProperty(
    name="Cam Focus List",
    default=False,
    update = assetsFunctions.update_cam_focus_list
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
bpy.types.Scene.light_type = bpy.props.BoolProperty(
    name="Light Data Type",
    description="Light Data Type",
    default=False,
)
bpy.types.Scene.mat = bpy.props.BoolProperty(
    name="Material",
    description="Material",
    default=False,
)
bpy.types.Scene.view = bpy.props.BoolProperty(
    name="View",
    description="View",
    default=True,
)
bpy.types.Scene.object_properties = bpy.props.BoolProperty(
    name="Object Propertie",
    description="Object Propertie",
    default=False,
)
bpy.types.Scene.particles_properties = bpy.props.BoolProperty(
    name="Particles Propertie",
    description="Particles Propertie",
    default=False,
)
bpy.types.Scene.advanced_option = bpy.props.BoolProperty(
    name="Advanced Option",
    description="Advanced Option",
    default=True,
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

bpy.types.Scene.BoneTool = bpy.props.BoolProperty(
    name="Bone Tool",
    description="Enable Bone Tool",
    default= False
)

bpy.types.Scene.Track_Prefix = bpy.props.StringProperty(
    name="Track Prefix",
    description="Track Prefix",
    default= "Track_",
)

bpy.types.Scene.Rig_Prop = bpy.props.StringProperty(
    name="Rig Properties",
    description="Rig Properties",
    default= "Prop",
)

bpy.types.Scene.VertexGroupMenu = EnumProperty(
    default='one',
    items=[('one', 'Custom', ''),
           ('two', 'Body', ''),
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

bpy.types.Scene.Constraints_Type = EnumProperty(
    default='Damped Track',
    items=[('Damped Track', 'Damped Track', ''),
           ('Child Of', 'Child Of', ''),
           ('Copy Rotation', 'Copy Rotation', ''),
            ])