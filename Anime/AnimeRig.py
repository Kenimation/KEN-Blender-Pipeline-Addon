import bpy
from bpy.props import (BoolProperty,
                       FloatProperty,
                       EnumProperty,
                       StringProperty,
                       IntProperty,
                       FloatVectorProperty,
                       )
from . import AnimeProperties, AnimeExtraProperties

def draw_horse_animerig(self, context, obj):
    rig = context.active_object
    if obj.RIG_ID == "Horse - Anime":
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.label(text = "Horse Anime Rig", icon = "OUTLINER_OB_ARMATURE")
        row = box.row()
        row.prop(rig, "horse_rig_class", expand = True)
        if rig.horse_rig_class == "Setup":
            layout = self.layout
            box = layout.box()
            row = box.row()
            row.label(text = "Asset:")
            row = box.row()
            row.prop(rig, "horse_belt", text = "Belt", toggle = True)
            row = box.row()
            row.prop(rig, "horse_saddle", text = "Saddle", toggle = True)
        elif rig.horse_rig_class == "Posing":
            layout = self.layout
            box = layout.box()
            row = box.row()
            row.label(text = "Posing:")
            if context.space_data.overlay.show_bones == True:
                icon = "HIDE_OFF"
            else:
                icon = "HIDE_ON"
            row.prop(context.space_data.overlay, "show_bones", icon = icon, emboss=False , text = "")
            box.prop(rig, "show_in_front", icon = "HIDE_OFF", text = "Show Bone In front")
            if rig.BonesCollection == True:
                icon = "DOWNARROW_HLT"
            else:
                icon = "RIGHTARROW"
            box.prop(rig, "BonesCollection", emboss=False , icon = icon)

            if rig.BonesCollection == True:
                collections = rig.data.collections
                row = box.row()
                row.prop(collections["Main"], "is_visible", text = "Main", toggle = True)
                if collections["Main"].is_visible == True:
                    row.operator("bone.selectgroup", text = "", emboss = False ,icon = "RESTRICT_SELECT_OFF").name = "Main"
                row = box.row()
                row.prop(collections["Hair"], "is_visible", text = "Hair", toggle = True)
                if collections["Hair"].is_visible == True:
                    row.operator("bone.selectgroup", text = "", emboss = False ,icon = "RESTRICT_SELECT_OFF").name = "Hair"
                row = box.row()
                row.prop(collections["R.Leg"], "is_visible", text = "Right Leg", toggle = True)
                if collections["R.Leg"].is_visible == True:
                    row.operator("bone.selectgroup", text = "", emboss = False ,icon = "RESTRICT_SELECT_OFF").name = "R.Leg"
                row.prop(collections["L.Leg"], "is_visible", text = "Left Leg", toggle = True)
                if collections["L.Leg"].is_visible == True:
                    row.operator("bone.selectgroup", text = "", emboss = False ,icon = "RESTRICT_SELECT_OFF").name = "L.Leg"

            layout = self.layout
            box = layout.box()
            row = box.row()
            row.label(text = "IK:")
            row = box.row()
            row.prop(rig, "R_Leg_Front_IK", text = "Right Front", slider = True)
            row.prop(rig, "L_Leg_Front_IK", text = "Left Front", slider = True)
            row = box.row()
            row.prop(rig, "R_Leg_Back_IK", text = "Right Back", slider = True)
            row.prop(rig, "L_Leg_Back_IK", text = "Left Back", slider = True)
            

bpy.types.Object.L_Leg_Front_IK = FloatProperty(
    min=0, max=1, default=1, name = "L_Leg_Front_IK")

bpy.types.Object.R_Leg_Front_IK = FloatProperty(
    min=0, max=1, default=1, name = "R_Leg_Front_IK")

bpy.types.Object.L_Leg_Back_IK = FloatProperty(
    min=0, max=1, default=1, name = "L_Leg_Back_IK")

bpy.types.Object.R_Leg_Back_IK = FloatProperty(
    min=0, max=1, default=1, name = "R_Leg_Back_IK")

bpy.types.Object.horse_belt = BoolProperty(
    default=True, name = "Belt")

bpy.types.Object.horse_saddle = BoolProperty(
    default=True, name = "Saddle")

bpy.types.Object.horse_rig_class = EnumProperty(
    default='Setup',
    items=[('Setup', 'Setup', ''),
            ('Posing', 'Posing', ''),
            ])