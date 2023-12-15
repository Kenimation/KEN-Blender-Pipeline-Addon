import bpy
import os

from bpy.props import (StringProperty,
                        EnumProperty,
                        BoolProperty,
                        IntProperty,
                        CollectionProperty,
)
from enum import Enum
from .Operations import uv_drag
from .AssetsUI import assetsDefs
from .Minecraft import minecraftDefs
from .Anime import AnimeProperties, AnimeDefs
from . import addon_updater_ops, icons

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

addon_keymaps = []

def getAddonPreferences(context):
    preferences = context.preferences
    addon_prefs = preferences.addons[__package__].preferences
    return addon_prefs

def write_view(self, context):
    addon_prefs = getAddonPreferences(context)
    text_file = assetsDefs.getPath("preferencesSettings.cfg")
    with open(text_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        data[3] = str(addon_prefs.view) + "\n"
        print(addon_prefs.view)

    # and write everything back
    with open(text_file, 'w') as file:
        file.writelines(data)

def write_advanced_option(self, context):
    addon_prefs = getAddonPreferences(context)
    text_file = assetsDefs.getPath("preferencesSettings.cfg")
    with open(text_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        data[6] = str(addon_prefs.advanced_option) + "\n"
        print(addon_prefs.advanced_option)

    # and write everything back
    with open(text_file, 'w') as file:
        file.writelines(data)

def write_tools(self, context):
    addon_prefs = getAddonPreferences(context)
    text_file = assetsDefs.getPath("preferencesSettings.cfg")
    with open(text_file, 'r') as file:
        # read a list of lines into data
        data = file.readlines()
        data[9] = str(addon_prefs.tools) + "\n"
        print(addon_prefs.tools)

    # and write everything back
    with open(text_file, 'w') as file:
        file.writelines(data)

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

class SyncAddonPrefs(bpy.types.Operator):
    bl_idname = "addonprefs.sync"
    bl_label = "sync. addon prefs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        if assetsDefs.readTextPrefs(4) == "True":
            addon_prefs.view = True
        else:
            addon_prefs.view = False

        if assetsDefs.readTextPrefs(7) == "True":
            addon_prefs.advanced_option = True
        else:
            addon_prefs.advanced_option = False

        if assetsDefs.readTextPrefs(10) == "True":
            addon_prefs.tools= True
        else:
            addon_prefs.tools = False

        if assetsDefs.readTextPrefs(16) == "True":
            addon_prefs.flip_bone = True
        else:
            addon_prefs.flip_bone = False

        addon_prefs.rig_scale = float(assetsDefs.readTextPrefs(13))
        addon_prefs.armIK = assetsDefs.readTextPrefs(19)
        addon_prefs.legIK = assetsDefs.readTextPrefs(22)
        addon_prefs.finger = assetsDefs.readTextPrefs(25)

        return {'FINISHED'}

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

class REGISTERED_NAME(bpy.types.PropertyGroup):
    registered_name: bpy.props.StringProperty()

class REGISTERED_NAME_LIST(bpy.types.UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        registered_name = item
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            layout.prop(registered_name, "registered_name", text = "", emboss = False)

        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class ADDREGISTERED_NAME(bpy.types.Operator):
    bl_idname = "add.registered_name"
    bl_label = "Add Registered Name"

    def execute(self, context):
        addon_prefs = getAddonPreferences(context)
        item = addon_prefs.registered_name.add()
        item.registered_name = "New Registered Name"
        return {'FINISHED'}
    
class REMOVEREGISTERED_NAME(bpy.types.Operator):
    bl_idname = "remove.registered_name"
    bl_label = "Remove Registered Name"

    def execute(self, context):
        addon_prefs = getAddonPreferences(context)
        index = addon_prefs.registered_name_index
        if index >= 0 and index < len(addon_prefs.registered_name):
            addon_prefs.registered_name.remove(index)
        return {'FINISHED'}

class AddonPref(bpy.types.AddonPreferences):
    bl_idname = __package__

    bktemplate_setting_bool : bpy.props.BoolProperty(default=True, name = "Bool", description = "Bool")
    compact_panel : bpy.props.BoolProperty(default = True, description = "Compact Ppanel")
    scene_material_panel : bpy.props.BoolProperty(default = True, description = "Turn on scene material panel in material priperties.")
    flip_bone : bpy.props.BoolProperty(default=True, update = assetsDefs.write_flip_bone)
    view : bpy.props.BoolProperty(default=True, update = write_view)
    advanced_option : bpy.props.BoolProperty(default=True, update = write_advanced_option)
    tools : bpy.props.BoolProperty(default=False, update = write_tools)

    rig_scale : bpy.props.FloatProperty(
		name='Rig Scale',
		description="Rig Scale of Anime Rig",
        update = AnimeDefs.write_rig_scale,
		default=1,
		min=1)
    
    registered_name_index : bpy.props.IntProperty(
    name="registered_name_index",
    description="registered_name_index",
    )

    registered_name : bpy.props.CollectionProperty(
         name="Registered Name",
         description="Input registered Name to enable registered function",
         type=REGISTERED_NAME)

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
                                update = assetsDefs.write_armIK,
                                items = [('FK', 'FK', ''),
                                        ('IK', 'IK', '')],
                                        default='FK')

    legIK : EnumProperty(
                                update = assetsDefs.write_legIK,
                                items = [('FK', 'FK', ''),
                                        ('IK', 'IK', '')],
                                        default='IK')
    
    finger : EnumProperty(
                                update = minecraftDefs.write_finger,
                                items = [('Off', 'Off', ''),
                                        ('On', 'On', '')],
                                        default='On')

    #━━━━━━━━━━━━━

    subClasses : EnumProperty(default = "one",
                                items = [('one', 'Settings', ''),
                                        ('two', 'Functions', ''),
                                        ('three', 'Contact / Contributors', ''),
                                        ('four', 'Update', ''),
                                        ])

    #━━━━━━━━━━━━━
    
    def draw(self, context):
        layout = self.layout
        script_file = os.path.realpath(__file__)
        script_directory = os.path.dirname(script_file)

        row = layout.row()
        row.prop(self, "subClasses", expand = True)
        row.operator("addonprefs.sync", text = "", icon = "FILE_REFRESH")
        row.scale_y = 1.25

        #━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        if self.subClasses == 'one':
            box = layout.box()
            box.label(text = "Registered Name:")
            row = box.row()
            row.template_list("REGISTERED_NAME_LIST", "", self, "registered_name", self, "registered_name_index")
            col = row.column(align=True)
            col.separator()
            col.operator("add.registered_name", text = "", icon = "ADD")
            col.operator("remove.registered_name", text = "", icon = "REMOVE")
            row = box.row()
            row.label(text = "UI Settings:")
            row = box.row()
            row.prop(self, "view", icon = "VIEW3D", text = "")
            row.prop(self, "advanced_option", icon = "OUTLINER", text = "")
            row.prop(self, "tools", icon = "TOOL_SETTINGS", text = "")
            row = box.row()
            row.prop(self, "compact_panel", text = "Compact Panel")
            row = box.row()
            row.prop(self, "scene_material_panel", text = "Scene Material Panel")
            row = box.row()
            if self.registered_name:
                if all(item.registered_name in AnimeProperties.registered_name for item in self.registered_name):
                    box = layout.box()
                    row = box.row()
                    row.label(text = "Rig Settings:")
                    for item in self.registered_name:
                        if  item.registered_name == AnimeProperties.registered_name[1]:
                            row = box.row()
                            row.label(text = "Rig Scale:")
                            row.prop(self, "rig_scale", text = "Rig Scale")

                    row = box.row()
                    row.label(text = "Flip bone:")
                    row.prop(self, "flip_bone", text = "Flip bone", toggle = True)
                    
                    row = box.row()
                    row.label(text = "Arms:")
                    row.prop(self, "armIK", expand = True)
                    
                    row = box.row()
                    row.label(text = "Legs:")
                    row.prop(self, "legIK", expand = True, text = "Legs")

                    row = box.row()
                    row.label(text = "Fingers(Minecraft):")
                    row.prop(self, "finger", expand = True, text = "Fingers")

        #━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        if self.subClasses == 'two':
            box = layout.box()
            col = box.column()
            col.label(text='Setup Hotkey:')
            col.separator()
            wm = context.window_manager
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
            OPEN_ADDON_PREFS_OF_ADDON,
            SyncAddonPrefs,
            REGISTERED_NAME,
            REGISTERED_NAME_LIST,
            ADDREGISTERED_NAME,
            REMOVEREGISTERED_NAME,
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
    
    remove_hotkey()
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()