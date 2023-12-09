import bpy
import os

from bpy.props import (StringProperty,
                        EnumProperty,
                        BoolProperty,
                        IntProperty,
)
from enum import Enum
from .Operations import uv_drag
from .Minecraft import minecraftProperties, minecraftDefs
from . import addon_updater_ops
from . import icons

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

addon_keymaps = []

def add_hotkey():

	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon

	if kc:
		if bpy.app.version >= (3,2,0):
			mouse_key = "LEFTMOUSE"
		else:
			mouse_key = "EVT_TWEAK_L"

		################################################
		km = kc.keymaps.new(name='UV Editor', space_type='EMPTY')
		kmi = km.keymap_items.new('uvdrag.toolkit_quick_drag_island', mouse_key, 'ANY', alt=True)
		kmi.active = True
		addon_keymaps.append((km, kmi))
		################################################
		km = kc.keymaps.new(name='UV Editor', space_type='EMPTY')
		kmi = km.keymap_items.new('uvdrag.toolkit_quick_drag_rotate_island', mouse_key, 'ANY', ctrl=True, alt=True)
		kmi.active = True
		addon_keymaps.append((km, kmi))

def get_hotkey_entry_item(km, kmi_name, kmi_value):
	for i, km_item in enumerate(km.keymap_items):
		if km.keymap_items.keys()[i] == kmi_name:
			# if km.keymap_items[i].properties.name == kmi_value: # プロパティがある場合は有効にする
			return km_item
	return None

def remove_hotkey():
	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon
	# 複数のキーマップを登録する場合、各キーマップの登録場所の記入が必要
	km = kc.keymaps['UV Editor']

	for km, kmi in addon_keymaps:
		km.keymap_items.remove(kmi)
		wm.keyconfigs.addon.keymaps.remove(km)
	addon_keymaps.clear()


class UVDRAG_OT_AddHotkey(bpy.types.Operator):
	''' Add hotkey entry '''
	bl_idname = "wpie.add_hotkey"
	bl_label = "Add Hotkey"
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, context):
		add_hotkey()
		return {'FINISHED'}

#━━━━━━━━━━━━━

class AddonPref(bpy.types.AddonPreferences):
    bl_idname = __package__

    bktemplate_setting_bool : bpy.props.BoolProperty(default=True, name = "Bool", description = "Bool")
    compact_panel : BoolProperty(default = True)
    flip_bone : BoolProperty(update = minecraftDefs.write_flip_bone)

    auto_check_update : bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False)

    updater_interval_months : bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)

    updater_interval_days : bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31)

    updater_interval_hours : bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)

    updater_interval_minutes : bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59)

    armIK : EnumProperty(
                                update = minecraftDefs.write_armIK,
                                items = [('FK', 'FK', ''),
                                        ('IK', 'IK', '')])

    legIK : EnumProperty(
                                update = minecraftDefs.write_legIK,
                                items = [('FK', 'FK', ''),
                                        ('IK', 'IK', '')])
    
    finger : EnumProperty(
                                update = minecraftDefs.write_finger,
                                items = [('Off', 'Off', ''),
                                        ('On', 'On', '')])



    #━━━━━━━━━━━━━

    subClasses : EnumProperty(default = "one",
                                items = [('one', 'Rig Settings', ''),
                                        ('two', 'Functions', ''),
                                        ('three', 'Contact / Contributors', ''),
                                        ('four', 'Update', ''),
                                        ])

    #━━━━━━━━━━━━━

    StringFileRename : StringProperty()
    directory_select : StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})
    filePath : StringProperty(maxlen=1024, subtype='FILE_PATH')
    addRemoveEnum : EnumProperty(items = [('one', 'Add', ''), ('two', 'Remove', '')])

    #━━━━━━━━━━━━━
    
    #━━━━━━━━━━━━━
    
    def draw(self, context):
        layout = self.layout
        script_file = os.path.realpath(__file__)
        script_directory = os.path.dirname(script_file)
        
        row = layout.row()
        row.prop(self, "subClasses", expand = True)
        row.scale_y = 1.25

        #━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        if self.subClasses == 'one':
            box = layout.box()
            box.label(text = "Default settings:")
            
            row = box.row()
            row.label(text = "UI Settings:")
            row = box.row()
            row.prop(self, "compact_panel", text = "Compact Panel")
            row.operator("addonprefs.sync", text = "", icon = "FILE_REFRESH")
            row = box.row()

            lb = layout.box()
            box = lb.box()
            row = box.row()
            row.label(text = "Rig Settings:")

            box = lb.box()
            row.prop(self, "flip_bone", text = "Flip bone")
            
            row = box.row()
            row.label(text = "Arms:")
            row.prop(self, "armIK", expand = True)
            
            row = box.row()
            row.label(text = "Legs:")
            row.prop(self, "legIK", expand = True, text = "Legs")

            row = box.row()
            row.label(text = "Fingers:")
            row.prop(self, "finger", expand = True, text = "Fingers")

        #━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        if self.subClasses == 'two':
            box = layout.box()
            col = box.column()
            col.label(text='Setup Hotkey')
            col.separator()
            wm = bpy.context.window_manager
            kc = wm.keyconfigs.user

            #########################################
            reg_location = "UV Editor" # ← 登録場所を設定する
            km = kc.keymaps[reg_location]
            kmi = get_hotkey_entry_item(km, 'uvdrag.toolkit_quick_drag_island', '')  # ← オペレーターと、プロパティを設定する
            if kmi:
                col.label(text="\"" +  reg_location + "\"")
                col.context_pointer_set("keymap", km)
                uv_drag.rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
                col.separator()
            else:
                col.label(text="No hotkey entry found")
                col.operator(UVDRAG_OT_AddHotkey.bl_idname, text = "Add hotkey entry", icon = 'ZOOM_IN')
            #########################################
            km = kc.keymaps[reg_location]
            kmi = get_hotkey_entry_item(km, 'uvdrag.toolkit_quick_drag_rotate_island', '')  # ← オペレーターと、プロパティを設定する
            if kmi:
                col.label(text="\"" +  reg_location + "\"")
                col.context_pointer_set("keymap", km)
                uv_drag.rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
                col.separator()
            else:
                col.label(text="No hotkey entry found")
                col.operator(UVDRAG_OT_AddHotkey.bl_idname, text = "Add hotkey entry", icon = 'ZOOM_IN')

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        if self.subClasses == 'three':            
            pcoll = preview_collections["main"]
            discord_icon = pcoll["Discord"]
            youtube_icon = pcoll["Youtube"]
            twitter_icon = pcoll["Twitter"]

            box = layout.box()
            box.label(text = "Contact")
            box.label(text = "Kenimation")
            row = box.row()
            row.scale_y = 1.25
            row.operator("wm.url_open", text="Kenimation Youtube Channel", icon_value = youtube_icon.icon_id).url = "https://www.youtube.com/@Kenimation"
            row = box.row()
            row.operator("wm.url_open", text="Kenimation Twitter", icon_value = twitter_icon.icon_id).url = "https://twitter.com/KENIMATION"
            row = box.row()
            row.operator("wm.url_open", text="Kenimation Discord Server", icon_value = discord_icon.icon_id).url = "https://discord.gg/zgksz7E"

            box = layout.box()
            box.label(text = "Original Addons / Rig")
            box.label(text = "BlueEvilGFXs")
            row = box.row()
            row.scale_y = 1.25
            row.operator("wm.url_open", text="BlueEvilGFXs", icon_value = youtube_icon.icon_id).url = "https://www.youtube.com/channel/UCKPgR4jjSDRTqWGAd2IOL5w"
            row.operator("wm.url_open", text="Thomas Animations", icon_value = youtube_icon.icon_id).url = "https://www.youtube.com/@ThomasAnimations"

            box = layout.box()
            box.label(text = "Functions")
            row = box.row()
            row.operator("wm.url_open", text="Bookyakuno", icon_value = youtube_icon.icon_id).url = "https://www.youtube.com/@bookyakuno8779"
        
        if self.subClasses == 'four':
            layout = self.layout
            addon_updater_ops.update_settings_ui(self, context)
        #━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


preview_collections = {}
addon_keymaps = []

classes = (
            UVDRAG_OT_AddHotkey,
            AddonPref,
          )
          
def register(): 
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
 
    add_hotkey()
    icon = icons.icons("icons")
    pcoll = icon.getColl()
    icon.load(pcoll)
    preview_collections["main"] = pcoll
  
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()