import bpy
from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatProperty, IntProperty, CollectionProperty

type = ["Warrior_Main", "Valkyrie_Rossweisse", "Valkyrie_Mother"]

def drawrigextra(self, context):
    rig = context.active_object
    if rig.get("sub_id") in type:
        layout = self.layout
        box = layout.box()
        box.label(text = "Extra rig options:")
        if rig.get("sub_id") == type[0]:
            row = box.row()
            row.label(text = "Cape:")
            row = box.row()
            row.prop(rig, "dynamic_cape", slider = True)
        if rig.get("sub_id") == type[1]:
            row = box.row()
            row.prop(rig, "hair_controller", toggle = True)
            row = box.row()
            row.label(text = "Dynamic Hair:")
            row = box.row()
            row.prop(rig, "hair", slider = True)
            row = box.row()
            row.prop(rig, "hair_head", slider = True)
            row = box.row()
            row.prop(rig, "hair_front", slider = True)
            row = box.row()
            row.prop(rig, "hair_back", slider = True)
            row = box.row()
            row.prop(rig, "hair_braid", slider = True)
            row = box.row()
            row.label(text = "Wing:")
            row = box.row()
            row.prop(rig, "wing_controller", toggle = True)
            row = box.row()
            row.label(text = "Cloth:")
            row = box.row()
            row.prop(rig, "dynamic_cloth", slider = True)
        if rig.get("sub_id") == type[2]:
            row = box.row()
            row.prop(rig, "hair_controller", toggle = True)
            row = box.row()
            row.label(text = "Dynamic Hair:")
            row = box.row()
            row.prop(rig, "hair", slider = True)
            row = box.row()
            row.prop(rig, "hair_head", slider = True)
            row = box.row()
            row.prop(rig, "hair_front", slider = True)
            row = box.row()
            row.prop(rig, "hair_back", slider = True)
            row = box.row()
            row.label(text = "Wing:")
            row = box.row()
            row.prop(rig, "wing_controller", toggle = True)
            row = box.row()
            row.label(text = "Cloth:")
            row = box.row()
            row.prop(rig, "dynamic_cape", slider = True)
            row = box.row()
            row.prop(rig, "dynamic_cloth", slider = True)
            row = box.row()
            row.label(text = "Bloody:")
            row = box.row()
            row.prop(rig, "bloody_skin", slider = True)
            row = box.row()
            row.prop(rig, "bloody_hair", slider = True)
            row = box.row()
            row.prop(rig, "bloody_cloth", slider = True)
            row = box.row()
            row.prop(rig, "bloody_wing", slider = True)


#Cloth
bpy.types.Object.dynamic_cloth = bpy.props.FloatProperty(name="Dynamic Cloth", min = 0, max = 1, default = 0.25)
bpy.types.Object.dynamic_cape = bpy.props.FloatProperty(name="Dynamic Cape", min = 0, max = 1, default = 0.25)

#Hair
bpy.types.Object.hair_controller = bpy.props.BoolProperty(name="Hair Advanced Controls", default = False)
bpy.types.Object.hair = bpy.props.FloatProperty(name="Hair", min = 0, max = 1, default = 0.1)
bpy.types.Object.hair_head = bpy.props.FloatProperty(name="Head Hair", min = 0, max = 1, default = 0.1)
bpy.types.Object.hair_front = bpy.props.FloatProperty(name="Front Hair", min = 0, max = 1, default = 0.1)
bpy.types.Object.hair_back = bpy.props.FloatProperty(name="Back Hair", min = 0, max = 1, default = 0.1)
bpy.types.Object.hair_braid = bpy.props.FloatProperty(name="Braid Hair", min = 0, max = 1, default = 0.1)

#Wings
bpy.types.Object.wing_controller = bpy.props.BoolProperty(name="Advanced Controls", default = False)

#Bloody
bpy.types.Object.bloody_skin = bpy.props.FloatProperty(name="Skin Bloody", min = 0, max = 1, default = 0)
bpy.types.Object.bloody_hair = bpy.props.FloatProperty(name="Hair Bloody", min = 0, max = 1, default = 0)
bpy.types.Object.bloody_cloth = bpy.props.FloatProperty(name="Cloth Bloody", min = 0, max = 1, default = 0)
bpy.types.Object.bloody_wing = bpy.props.FloatProperty(name="Wing Bloody", min = 0, max = 1, default = 0)