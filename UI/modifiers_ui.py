import bpy
import os
from bl_ui.properties_data_modifier import DATA_PT_modifiers as original_DATA_PT_modifiers
from bl_ui.properties_data_modifier import DATA_PT_gpencil_modifiers as original_DATA_PT_gpencil_modifiers
from .. import addonPreferences
from .modifiers_data import DATA_modifiers
from bpy.types import Operator, OperatorFileListElement, Panel
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty

def object_type_has_modifiers(object):
    obs_with_mods = {
        'MESH',
        'CURVE',
        'CURVES',
        'SURFACE',
        'FONT',
        'LATTICE',
        'POINTCLOUD',
        'VOLUME'
    }
    return object.type in obs_with_mods

def is_modifier_disabled(mod):
	"""Checks if the name of the modifier should be diplayed with a red
	background.
	"""
	if mod.type == 'ARMATURE' and not mod.object:
		return True

	elif mod.type == 'BOOLEAN':
		if ((mod.operand_type == 'OBJECT' and not mod.object)
				or (mod.operand_type == 'COLLECTION' and not mod.collection)):
			return True

	elif mod.type == 'CAST':
		if not any((mod.use_x, mod.use_y, mod.use_z)) or mod.factor == 0:
			return True

	elif mod.type == 'CURVE' and not mod.object:
		return True

	elif mod.type == 'DATA_TRANSFER' and not mod.object:
		return True

	elif mod.type == 'DISPLACE':
		if (mod.direction == 'RGB_TO_XYZ' and not mod.texture) or mod.strength == 0:
			return True

	elif mod.type == 'HOOK' and not mod.object:
		return True

	elif mod.type == 'LAPLACIANDEFORM' and not mod.vertex_group:
		return True

	elif mod.type == 'LAPLACIANSMOOTH':
		if not any((mod.use_x, mod.use_y, mod.use_z)) or mod.lambda_factor == 0:
			return True

	elif mod.type == 'LATTICE' and not mod.object:
		return True

	elif mod.type == 'MESH_CACHE' and (not mod.filepath or mod.factor == 0):
		return True

	elif mod.type == 'MESH_DEFORM' and not mod.object:
		return True

	elif mod.type == 'MESH_SEQUENCE_CACHE' and (not mod.cache_file or not mod.object_path):
		return True

	elif mod.type == 'MESH_TO_VOLUME' and not mod.object:
		return True

	elif mod.type == 'NODES' and not mod.node_group:
		return True

	elif mod.type == 'NORMAL_EDIT' and (mod.mode == 'DIRECTIONAL' and not mod.target):
		return True

	elif mod.type == 'PARTICLE_INSTANCE':
		if not mod.object:
			return True

		if not mod.object.particle_systems:
			return True
		else:
			for m in mod.object.modifiers:
				if m.type == 'PARTICLE_SYSTEM' and m.particle_system == mod.particle_system:
					if not m.show_viewport:
						return True

	elif mod.type == 'SHRINKWRAP' and not mod.target:
		return True

	elif mod.type == 'SMOOTH':
		if not any((mod.use_x, mod.use_y, mod.use_z)) or mod.factor == 0:
			return True

	elif mod.type == 'SUBSURF' and mod.levels == 0:
		return True

	elif mod.type == 'SURFACE_DEFORM' and not mod.target:
		return True

	elif mod.type == 'VERTEX_WEIGHT_EDIT' and not mod.vertex_group:
		return True

	elif mod.type == 'VERTEX_WEIGHT_MIX' and not mod.vertex_group_a:
		return True

	elif mod.type == 'VERTEX_WEIGHT_PROXIMITY' and (not mod.vertex_group or not mod.target):
		return True

	elif mod.type == 'VOLUME_DISPLACE' and not mod.texture:
		return True

	elif mod.type == 'VOLUME_TO_MESH' and not mod.object:
		return True

	elif mod.type == 'GP_LINEART' and (not mod.source_collection or not mod.target_layer or not mod.target_material):
		return True

	return False

class ModifiersList_OT_ApplyAllModifiers(Operator):
	bl_idname = "modifiers_list.apply_all_modifiers"
	bl_label = "Apply All Modifiers"
	bl_description = "Applies to all modifiers of selected object"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		for obj in context.selected_objects:
			if obj.modifiers:
				return True
			if obj.grease_pencil_modifiers:
				return True
		return False

	def execute(self, context):
		for obj in context.selected_objects:
			for mod in obj.modifiers[:]:
				bpy.ops.object.modifier_apply(modifier=mod.name)
			for mod in obj.grease_pencil_modifiers[:]:
				bpy.ops.object.gpencil_modifiers_apply(modifier=mod.name)
		return {'FINISHED'}

class ModifiersList_OT_DeleteAllModifiers(Operator):
	bl_idname = "modifiers_list.delete_all_modifiers"
	bl_label = "Remove All Modifiers"
	bl_description = "Remove all modifiers of selected object"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		for obj in context.selected_objects:
			if obj.modifiers:
				return True
			if obj.grease_pencil_modifiers:
				return True
		return False

	def execute(self, context):
		for obj in context.selected_objects:
			for mod in obj.modifiers[:]:
				obj.modifiers.remove(mod)
			for mod in obj.grease_pencil_modifiers[:]:
				obj.grease_pencil_modifiers.remove(mod)
		return {'FINISHED'}

class ModifiersList_OT_ToggleApplyModifiersCage(Operator):
	bl_idname = "modifiers_list.toggle_apply_modifier_cage"
	bl_label = "Switch Modifiers Apply/Unapply to show on Cage"
	bl_description = "Shows or hides application to show on Cage all modifiers of selected object"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object:
			if context.active_object.modifiers:
				return True
			if context.active_object.grease_pencil_modifiers:
				return True
		return False

	def execute(self, context):
		is_apply = True
		for mod in context.active_object.modifiers:
			if mod.show_on_cage:
				is_apply = False
				break
		for obj in context.selected_objects:
			for mod in obj.modifiers:
				mod.show_on_cage = is_apply

		for mod in context.active_object.grease_pencil_modifiers:
			if mod.show_on_cage:
				is_apply = False
				break
		for obj in context.selected_objects:
			for mod in obj.grease_pencil_modifiers:
				mod.show_on_cage = is_apply

		if is_apply:
			self.report(type={"INFO"}, message="Applied modifiers to show on Cage")
		else:
			self.report(type={"INFO"}, message="Unregistered modifiers apply to show on Cage")
		return {'FINISHED'}

class ModifiersList_OT_ToggleApplyModifiersEditMode(Operator):
	bl_idname = "modifiers_list.toggle_apply_modifier_editmode"
	bl_label = "Switch Modifiers Apply/Unapply to show in Edit Mode"
	bl_description = "Shows or hides application to show in Edit Mode all modifiers of selected object"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object:
			if context.active_object.modifiers:
				return True
			if context.active_object.grease_pencil_modifiers:
				return True
		return False

	def execute(self, context):
		is_apply = True
		for mod in context.active_object.modifiers:
			if mod.show_in_editmode:
				is_apply = False
				break
		for obj in context.selected_objects:
			for mod in obj.modifiers:
				mod.show_in_editmode = is_apply

		for mod in context.active_object.grease_pencil_modifiers:
			if mod.show_in_editmode:
				is_apply = False
				break
		for obj in context.selected_objects:
			for mod in obj.grease_pencil_modifiers:
				mod.show_in_editmode = is_apply

		if is_apply:
			self.report(type={"INFO"}, message="Applied modifiers to show in Edit Mode")
		else:
			self.report(type={"INFO"}, message="Unregistered modifiers apply to show in Edit Mode")
		return {'FINISHED'}

class ModifiersList_OT_ToggleApplyModifiersView(Operator):
	bl_idname = "modifiers_list.toggle_apply_modifier_view"
	bl_label = "Switch Modifiers Apply/Unapply to View"
	bl_description = "Shows or hides application to view all modifiers of selected object"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object:
			if context.active_object.modifiers:
				return True
			if context.active_object.grease_pencil_modifiers:
				return True
		return False

	def execute(self, context):
		is_apply = True
		for mod in context.active_object.modifiers:
			if mod.show_viewport:
				is_apply = False
				break
		for obj in context.selected_objects:
			for mod in obj.modifiers:
				mod.show_viewport = is_apply

		for mod in context.active_object.grease_pencil_modifiers:
			if mod.show_viewport:
				is_apply = False
				break
		for obj in context.selected_objects:
			for mod in obj.grease_pencil_modifiers:
				mod.show_viewport = is_apply

		if is_apply:
			self.report(type={"INFO"}, message="Applied modifiers to view")
		else:
			self.report(type={"INFO"}, message="Unregistered modifiers apply to view")
		return {'FINISHED'}

class ModifiersList_OT_ToggleApplyModifiersRender(Operator):
	bl_idname = "modifiers_list.toggle_apply_modifier_render"
	bl_label = "Switch Modifiers Apply/Unapply to Render"
	bl_description = "Shows or hides application to Render all modifiers of selected object"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object:
			if context.active_object.modifiers:
				return True
			if context.active_object.grease_pencil_modifiers:
				return True
		return False

	def execute(self, context):
		is_apply = True
		for mod in context.active_object.modifiers:
			if mod.show_render:
				is_apply = False
				break
		for obj in context.selected_objects:
			for mod in obj.modifiers:
				mod.show_render = is_apply

		for mod in context.active_object.grease_pencil_modifiers:
			if mod.show_render:
				is_apply = False
				break
		for obj in context.selected_objects:
			for mod in obj.grease_pencil_modifiers:
				mod.show_render = is_apply

		if is_apply:
			self.report(type={"INFO"}, message="Applied modifiers to Render")
		else:
			self.report(type={"INFO"}, message="Unregistered modifiers apply to Render")
		return {'FINISHED'}

class ModifiersList_OT_CopyToSelected_ListModifiers(Operator):
	bl_idname = "modifiers_list.copy_to_selected_modifier"
	bl_label = "Copy To Selected Modifiers"
	bl_description = "Copy To Selected Modifiers"
	bl_options = {'REGISTER', 'UNDO'}
	
	name: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):
		if len(context.selected_objects) > 1:
			for obj in context.selected_objects:
				if obj.modifiers:
					return True
				if obj.grease_pencil_modifiers:
					return True
		return False

	def execute(self, context):
		if context.object.type != "GPENCIL":
			bpy.ops.object.modifier_copy_to_selected(modifier=self.name)
		else:
			bpy.ops.object.gpencil_modifier_copy_to_selected(modifier=self.name)
		return {'FINISHED'}

class ModifiersList_OT_CopyToSelected_ListModifiersAll(Operator):
	bl_idname = "modifiers_list.copy_to_selected_all_modifiers"
	bl_label = "Copy All Modifiers To Selected"
	bl_description = "Copy All Modifiers To Selected"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if len(context.selected_objects) > 1:
			for obj in context.selected_objects:
				if obj.modifiers:
					return True
				if obj.grease_pencil_modifiers:
					return True
		return False

	def execute(self, context):
		for mod in context.object.modifiers[:]:
			bpy.ops.object.modifier_copy_to_selected(modifier=mod.name)
		for mod in context.object.grease_pencil_modifiers[:]:
			bpy.ops.object.gpencil_modifier_copy_to_selected(modifier=mod.name)
		return {'FINISHED'}

class ModifiersList_OT_Delete_Modifiers_List(Operator):
	bl_idname = "modifiers_list.delete_modifiers_list"
	bl_label = "Delete Modifiers List"
	bl_description = "Delete Modifiers"
	bl_options = {'REGISTER', 'UNDO'}
	
	name: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):
		for obj in context.selected_objects:
			if obj.modifiers:
				return True
			if obj.grease_pencil_modifiers:
				return True
		return False

	def execute(self, context):
		obj = context.object
		if obj.type != "GPENCIL":
			modifier = obj.modifiers[self.name]
			obj.modifiers.remove(modifier)
		else:
			modifier = obj.grease_pencil_modifiers[self.name]
			obj.grease_pencil_modifiers.remove(modifier)

		if obj.mod_index != 0:
			obj.mod_index = obj.mod_index - 1

		return {'FINISHED'}

class ModifiersList_OT_Duplicate_Modifiers_List(bpy.types.Operator):
	bl_idname = "modifiers_list.duplicate_modifiers_list"
	bl_label = "Duplicate Modifiers"
	bl_options = {'REGISTER', 'UNDO'}

	name: bpy.props.StringProperty(options={'HIDDEN'})
	index: bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		obj = context.object
		if obj.type != "GPENCIL":
			bpy.ops.object.modifier_copy(modifier=self.name)
		else:
			bpy.ops.object.gpencil_modifier_copy(modifier=self.name)

		obj.mod_index = self.index + 1

		return {"FINISHED"}

class ModifiersList_OT_Apply_Modifiers_List(bpy.types.Operator):
	bl_idname = "modifiers_list.apply_modifiers_list"
	bl_label = "Apply Modifiers"
	bl_options = {'REGISTER', 'UNDO'}

	name: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		obj = context.object
		if obj.type != "GPENCIL":
			bpy.ops.object.modifier_apply(modifier=self.name)
		else:
			bpy.ops.object.gpencil_modifier_apply(modifier=self.name)

		if obj.mod_index != 0:
			obj.mod_index = obj.mod_index - 1

		return {"FINISHED"}

class ModifiersList_OT_Delete_Modifier(Operator):
	bl_idname = "modifiers_list.delete_modifier"
	bl_label = "Delete Modifiers List"
	bl_description = "Delete Modifiers"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context == 'MODIFIER':
				for obj in context.selected_objects:
					if obj.modifiers:
						return True
					if obj.grease_pencil_modifiers:
						return True
		except:
			for obj in context.selected_objects:
				if obj.modifiers:
					return True
				if obj.grease_pencil_modifiers:
					return True
		return False

	def execute(self, context):
		obj = context.object
		if obj.type != "GPENCIL":
			mod_list = []
			for mod in obj.modifiers:
				mod_list.append(mod)
			modifier = mod_list[obj.mod_index]
		else:
			mod_list = []
			for mod in obj.grease_pencil_modifiers:
				mod_list.append(mod)
			modifier = mod_list[obj.mod_index]

		if obj.type != "GPENCIL":
			modifier = obj.modifiers[modifier.name]
			obj.modifiers.remove(modifier)
		else:
			modifier = obj.grease_pencil_modifiers[modifier.name]
			obj.grease_pencil_modifiers.remove(modifier)

		if obj.mod_index != 0:
			obj.mod_index = obj.mod_index - 1

		return {'FINISHED'}

class ModifiersList_OT_Duplicate_Modifier(bpy.types.Operator):
	bl_idname = "modifiers_list.duplicate_modifier"
	bl_label = "Duplicate Modifiers List"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context == 'MODIFIER':
				return True
		except:
			return True
		return False

	def execute(self, context):
		obj = context.object
		if obj.type != "GPENCIL":
			mod_list = []
			for mod in obj.modifiers:
				mod_list.append(mod)
			modifier = mod_list[obj.mod_index]
		else:
			mod_list = []
			for mod in obj.grease_pencil_modifiers:
				mod_list.append(mod)
			modifier = mod_list[obj.mod_index]

		if obj.type != "GPENCIL":
			bpy.ops.object.modifier_copy(modifier=modifier.name)
		else:
			bpy.ops.object.gpencil_modifier_copy(modifier=modifier.name)

		obj.mod_index = obj.mod_index + 1

		return {"FINISHED"}

class ModifiersList_OT_Apply_Modifier(bpy.types.Operator):
	bl_idname = "modifiers_list.apply_modifier"
	bl_label = "Apply Modifiers List"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context == 'MODIFIER':
				return True
		except:
			return True
		return False

	def execute(self, context):
		obj = context.object
		if obj.type != "GPENCIL":
			mod_list = []
			for mod in obj.modifiers:
				mod_list.append(mod)
			modifier = mod_list[obj.mod_index]
		else:
			mod_list = []
			for mod in obj.grease_pencil_modifiers:
				mod_list.append(mod)
			modifier = mod_list[obj.mod_index]

		if obj.type != "GPENCIL":
			bpy.ops.object.modifier_apply(modifier=modifier.name)
		else:
			bpy.ops.object.gpencil_modifier_apply(modifier=modifier.name)

		if obj.mod_index != 0:
			obj.mod_index = obj.mod_index - 1

		return {"FINISHED"}

class ModifiersList_OT_Toggle_Modifiers_View(bpy.types.Operator):
	bl_idname = "modifiers_list.toggle_modifier_view"
	bl_label = "Toggle Modifiers View"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'MODIFIER':
			return True
		return False

	def execute(self, context):
		obj = context.object
		if obj.type != "GPENCIL":
			mod_list = []
			for mod in obj.modifiers:
				mod_list.append(mod)
			modifier = mod_list[obj.mod_index]
		else:
			mod_list = []
			for mod in obj.grease_pencil_modifiers:
				mod_list.append(mod)
			modifier = mod_list[obj.mod_index]

		if obj.type != "GPENCIL":
			modifier = obj.modifiers[modifier.name]
			if modifier.show_viewport == True:
				modifier.show_viewport = False
			else:
				modifier.show_viewport = True
		else:
			modifier = obj.grease_pencil_modifiers[modifier.name]
			if modifier.show_viewport == True:
				modifier.show_viewport = False
			else:
				modifier.show_viewport = True

		return {"FINISHED"}

class ModifiersList_OT_Solo_Modifiers_View(bpy.types.Operator):
	bl_idname = "modifiers_list.solo_modifier_view"
	bl_label = "Solo Modifiers List"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'MODIFIER':
			return True
		return False

	def execute(self, context):
		obj = context.object
		if obj.type != "GPENCIL":
			mod_list = []
			for mod in obj.modifiers:
				mod_list.append(mod)
			modifier = mod_list[obj.mod_index]
		else:
			mod_list = []
			for mod in obj.grease_pencil_modifiers:
				mod_list.append(mod)
			modifier = mod_list[obj.mod_index]

		for obj in context.selected_objects:
			for mod in obj.modifiers[:]:
				if mod != modifier:
					mod.show_viewport = False
				else:
					mod.show_viewport = True
				
			for mod in obj.grease_pencil_modifiers[:]:
				if mod != modifier:
					mod.show_viewport = False
				else:
					mod.show_viewport = True
				
		return {"FINISHED"}

class ModifiersList_OT_Show_Modifiers_View(bpy.types.Operator):
	bl_idname = "modifiers_list.show_modifier_view"
	bl_label = "Show All Modifiers List"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'MODIFIER':
			return True
		return False

	def execute(self, context):
		obj = context.object

		for obj in context.selected_objects:
			for mod in obj.modifiers[:]:
				mod.show_viewport = True
				
			for mod in obj.grease_pencil_modifiers[:]:
				mod.show_viewport = True
				
		return {"FINISHED"}

class ModifierButtonsPanel:
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "modifier"
	bl_options = {'HIDE_HEADER'}

class ModifiersList(bpy.types.UIList):
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
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		modifiers = item
		# draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			# You should always start your row layout by a label (icon + text), or a non-embossed text field,
			# this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
			# We use icon_value of label, as our given i
			# con is an integer value, not an enum ID.
			# Note "data" names should never be translated!

			if modifiers:

				duplicate = layout.operator("modifiers_list.duplicate_modifiers_list", text="", emboss=False, icon = "LAYER_ACTIVE" if index == context.object.mod_index else "LAYER_USED")
				duplicate.name = modifiers.name
				duplicate.index = index
				row = layout.row()
				row.alert = is_modifier_disabled(modifiers)
				row.label(text="", icon_value=layout.icon(modifiers))
				layout.prop(modifiers, "name", text="", emboss=False)
				if 'show_on_cage' in modifiers.bl_rna.properties:
					layout.prop(modifiers, "show_on_cage", text="", icon="MESH_DATA")
				if 'show_in_editmode' in modifiers.bl_rna.properties:
					layout.prop(modifiers, "show_in_editmode", text="", icon="EDITMODE_HLT")
				layout.prop(modifiers, "show_viewport", text="", emboss=False, icon="RESTRICT_VIEW_ON")
				layout.prop(modifiers, "show_render", text="", emboss=False, icon="RESTRICT_RENDER_ON")
				if len(context.selected_objects) > 1:
					layout.operator("modifiers_list.copy_to_selected_modifier", emboss = False, icon='COPYDOWN', text="").name = modifiers.name
				layout.operator("modifiers_list.apply_modifiers_list", emboss=False, icon='CHECKMARK', text="").name = modifiers.name
				layout.operator("modifiers_list.delete_modifiers_list", emboss=False, icon='X', text="").name = modifiers.name

		# 'GRID' layout type should be as compact as possible (typically a single icon!).
		elif self.layout_type == 'GRID':
			layout.alignment = 'CENTER'
			layout.label(text="", icon_value=icon)

class ModifiersList_OT_List_Up(Operator):
	bl_idname = "modifiers_list.modifiers_list_up"
	bl_label = "Modifiers List Move Up"
	bl_description = "Modifiers List Move Up"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context == 'MODIFIER':
				return ((len(context.object.modifiers) > 0 or len(context.object.grease_pencil_modifiers) > 0) and context.object.mod_index > 0)
		except:
			return ((len(context.object.modifiers) > 0 or len(context.object.grease_pencil_modifiers) > 0) and context.object.mod_index > 0)

	def execute(self, context):
		if context.object.type != "GPENCIL":
			name = context.object.modifiers[context.object.mod_index].name

			if context.object.mod_index == 0:
				context.object.mod_index = len(context.object.modifiers) - 1
			else:
				context.object.mod_index -= 1
			bpy.ops.object.modifier_move_to_index(modifier=name, index=context.object.mod_index)
		else:
			name = context.object.grease_pencil_modifiers[context.object.mod_index].name

			if context.object.mod_index == 0:
				context.object.mod_index = len(context.object.grease_pencil_modifiers) - 1
			else:
				context.object.mod_index -= 1
			bpy.ops.object.gpencil_modifier_move_to_index(modifier=name, index=context.object.mod_index)
		return{'FINISHED'}

class ModifiersList_OT_List_Down(Operator):
	bl_idname = "modifiers_list.modifiers_list_down"
	bl_label = "Modifiers List Move Down"
	bl_description = "Modifiers List Move Down"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context == 'MODIFIER':
				return ((len(context.object.modifiers) > 0 or len(context.object.grease_pencil_modifiers) > 0) and ((context.object.mod_index < len(context.object.modifiers) - 1) or(context.object.mod_index < len(context.object.grease_pencil_modifiers) - 1)))
		except:
			return ((len(context.object.modifiers) > 0 or len(context.object.grease_pencil_modifiers) > 0) and ((context.object.mod_index < len(context.object.modifiers) - 1) or(context.object.mod_index < len(context.object.grease_pencil_modifiers) - 1)))

	def execute(self, context):
		if context.object.type != "GPENCIL":
			name = context.object.modifiers[context.object.mod_index].name

			if context.object.mod_index == len(context.object.modifiers) - 1:
				context.object.mod_index = 0
			else:
				context.object.mod_index += 1
			bpy.ops.object.modifier_move_to_index(modifier=name, index=context.object.mod_index)
		else:
			name = context.object.grease_pencil_modifiers[context.object.mod_index].name

			if context.object.mod_index == len(context.object.grease_pencil_modifiers) - 1:
				context.object.mod_index = 0
			else:
				context.object.mod_index += 1
			bpy.ops.object.gpencil_modifier_move_to_index(modifier=name, index=context.object.mod_index)

		return{'FINISHED'}

class ModifiersList_OT_List_First(Operator):
	bl_idname = "modifiers_list.modifiers_list_first"
	bl_label = "Modifiers List Move to First"
	bl_description = "Modifiers List Move to First"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context == 'MODIFIER':
				return ((len(context.object.modifiers) > 0 or len(context.object.grease_pencil_modifiers) > 0) and context.object.mod_index > 0)
		except:
			return ((len(context.object.modifiers) > 0 or len(context.object.grease_pencil_modifiers) > 0) and context.object.mod_index > 0)

	def execute(self, context):
		if context.object.type != "GPENCIL":
			name = context.object.modifiers[context.object.mod_index].name
			bpy.ops.object.modifier_move_to_index(modifier=name, index=0)
		else:
			name = context.object.grease_pencil_modifiers[context.object.mod_index].name
			bpy.ops.object.gpencil_modifier_move_to_index(modifier=name, index=0)

		if not context.object.mod_index == 0:
			context.object.mod_index = 0
		return{'FINISHED'}

class ModifiersList_OT_List_Last(Operator):
	bl_idname = "modifiers_list.modifiers_list_last"
	bl_label = "Modifiers List Move to Last"
	bl_description = "Modifiers List Move to Last"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context == 'MODIFIER':
				return ((len(context.object.modifiers) > 0 or len(context.object.grease_pencil_modifiers) > 0) and ((context.object.mod_index < len(context.object.modifiers) - 1) or(context.object.mod_index < len(context.object.grease_pencil_modifiers) - 1)))
		except:
			return ((len(context.object.modifiers) > 0 or len(context.object.grease_pencil_modifiers) > 0) and ((context.object.mod_index < len(context.object.modifiers) - 1) or(context.object.mod_index < len(context.object.grease_pencil_modifiers) - 1)))

	def execute(self, context):
		if context.object.type != "GPENCIL":
			name = context.object.modifiers[context.object.mod_index].name
			bpy.ops.object.modifier_move_to_index(modifier=name, index=len(context.object.modifiers) - 1)
			if not context.object.mod_index == len(context.object.modifiers) - 1:

				context.object.mod_index = len(context.object.modifiers) - 1
		else:
			name = context.object.grease_pencil_modifiers[context.object.mod_index].name
			bpy.ops.object.gpencil_modifier_move_to_index(modifier=name, index=len(context.object.grease_pencil_modifiers) - 1)
			if not context.object.mod_index == len(context.object.grease_pencil_modifiers) - 1:

				context.object.mod_index = len(context.object.grease_pencil_modifiers) - 1

		return{'FINISHED'}

class DATA_PT_modifiers(ModifierButtonsPanel, Panel):
	bl_label = "Modifiers"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "modifier"
	bl_options = {'HIDE_HEADER'}

	@classmethod
	def poll(cls, context):
		ob = context.object
		if ob is not None:
			return object_type_has_modifiers(ob)
		return False
	
	def draw(self, context):
		addon_prefs = addonPreferences.getAddonPreferences(context)
		layout = self.layout
		scene = context.scene
		obj = context.object
		row = layout.row()
		
		lrow = row.row()
		lrow.alignment = 'LEFT'
		lrow.prop(addon_prefs, "use_modifier_panel", text = "Modifier List", icon = "MODIFIER", emboss = False)
		row = row.row()
		row.alignment = 'RIGHT'

		drawmodifiers(self, context, layout, row, obj)

class DATA_PT_gpencil_modifiers(ModifierButtonsPanel, Panel):
	bl_label = "Modifiers"

	@classmethod
	def poll(cls, context):
		ob = context.object
		return ob and ob.type == 'GPENCIL'

	def draw(self, context):
		addon_prefs = addonPreferences.getAddonPreferences(context)
		layout = self.layout
		scene = context.scene
		obj = context.object
		row = layout.row()
		
		lrow = row.row()
		lrow.alignment = 'LEFT'
		lrow.prop(addon_prefs, "use_modifier_panel", text = "Modifier List", icon = "MODIFIER", emboss = False)
		row = row.row()
		row.alignment = 'RIGHT'

		drawmodifiers(self, context, layout, row, obj)

def KEN_MT_mod_menu_main(self, context):
	addon_prefs = addonPreferences.getAddonPreferences(context)
	if (context.active_object):
		# if (len(context.active_object.modifiers)):
		lrow = self.layout.row(align=True)
		row = lrow.row(align=True)
		row.alignment = 'LEFT'
		row.prop(addon_prefs, "use_modifier_panel", text = "Toggle Modifier List", icon = "MODIFIER_OFF", emboss = False)

def drawmodifiers(self, context, layout, row, obj):
	scene = context.scene
	if obj.modifiers or obj.grease_pencil_modifiers:
		row.operator("modifiers_list.toggle_apply_modifier_cage", icon='MESH_DATA', text="")
		row.operator("modifiers_list.toggle_apply_modifier_editmode", icon='EDITMODE_HLT', text="")
		row.operator("modifiers_list.toggle_apply_modifier_view", icon='RESTRICT_VIEW_OFF', text="")
		row.operator("modifiers_list.toggle_apply_modifier_render", icon='RESTRICT_RENDER_OFF', text="")
		if len(context.selected_objects) > 1:
			row.operator("modifiers_list.copy_to_selected_all_modifiers", emboss = False, icon='COPYDOWN', text="")
		row.operator("modifiers_list.apply_all_modifiers", emboss = False, icon='CHECKMARK', text="")
		row.operator("modifiers_list.delete_all_modifiers", emboss = False, icon='X', text="")

	if scene.mod_panel == True:
		icon ="FULLSCREEN_ENTER"
	else:
		icon ="FULLSCREEN_EXIT"
	rrow = row
	rrow.scale_x = 1.1
	rrow.prop(scene, "mod_panel", emboss = False, icon=icon, text="")

	if obj.type != "GPENCIL":
		layout.operator("wm.call_menu", text="Add Modifier", icon='ADD').name = "OBJECT_MT_modifier_add"
		row = layout.row()
		row.template_list("ModifiersList", "", obj, "modifiers", obj, "mod_index")
	else:
		layout.operator_menu_enum("object.gpencil_modifier_add", "type")
		row = layout.row()
		row.template_list("ModifiersList", "", obj, "grease_pencil_modifiers", obj, "mod_index")

	col = row.column()
	col.operator("modifiers_list.modifiers_list_first", text="", icon='TRIA_UP_BAR')
	col.operator("modifiers_list.modifiers_list_up", text="", icon='TRIA_UP')
	col.operator("modifiers_list.modifiers_list_down", text="", icon='TRIA_DOWN')
	col.operator("modifiers_list.modifiers_list_last", text="", icon='TRIA_DOWN_BAR')

	if context.scene.mod_panel == True:
		if obj.modifiers or obj.grease_pencil_modifiers:
			try:
				if obj.type != "GPENCIL":
					mod_list = []
					for mod in obj.modifiers:
						mod_list.append(mod)
					modifiers = mod_list[obj.mod_index]
				else:
					mod_list = []
					for mod in obj.grease_pencil_modifiers:
						mod_list.append(mod)
					modifiers = mod_list[obj.mod_index]

				col = layout.column(align=True)

				# === General settings ===
				box = col.box()

				row = box.row()

				row.operator("modifiers_list.duplicate_modifiers", text="", emboss=False, icon = "LAYER_ACTIVE")
				lrow = row.row()
				lrow.alert = is_modifier_disabled(modifiers)
				lrow.label(text="", icon_value=layout.icon(modifiers))
				row.prop(modifiers, "name", text = "")
				if 'show_on_cage' in modifiers.bl_rna.properties:
					row.prop(modifiers, "show_on_cage", text="", icon="MESH_DATA")
				if 'show_in_editmode' in modifiers.bl_rna.properties:
					row.prop(modifiers, "show_in_editmode", text="", icon="EDITMODE_HLT")
				row.prop(modifiers, "show_viewport", text="", emboss=False, icon="RESTRICT_VIEW_ON")
				row.prop(modifiers, "show_render", text="", emboss=False, icon="RESTRICT_RENDER_ON")
				if len(context.selected_objects) > 1:
					row.operator("modifiers_list.copy_to_selected_modifier", emboss = False, icon='COPYDOWN', text="").name = modifiers.name
				row.operator("modifiers_list.apply_modifier", emboss=False, icon='CHECKMARK', text="")
				row.operator("modifiers_list.delete_modifier", emboss=False, icon='X', text="")
				
				try:
					mp = DATA_modifiers(context)
					getattr(mp, modifiers.type)(box, obj, modifiers)
				except:
					box.label(text = "Modifier has no panel")
			except:
				layout.label(text = "No Modifier has selected.")

def ken_modifier_panel(self, context):
	addon_prefs = addonPreferences.getAddonPreferences(context)
	use_modifier_panel = addon_prefs.use_modifier_panel

	from bpy.utils import register_class, unregister_class

	if use_modifier_panel:
		try:
			register_class(DATA_PT_modifiers)
			register_class(DATA_PT_gpencil_modifiers)
		except ValueError:
			unregister_class(DATA_PT_modifiers)
			unregister_class(DATA_PT_gpencil_modifiers)
			register_class(original_DATA_PT_modifiers)
			register_class(original_DATA_PT_gpencil_modifiers)
	else:
		try:
			unregister_class(DATA_PT_modifiers)
			unregister_class(DATA_PT_gpencil_modifiers)
			register_class(original_DATA_PT_modifiers)
			register_class(original_DATA_PT_gpencil_modifiers)
		except RuntimeError:
			pass

bpy.types.Scene.mod_panel = bpy.props.BoolProperty(
	name="Expand Modifiers Settings",
	description="Expand Modifiers Settings Panel",
)

bpy.types.Object.mod_index = bpy.props.IntProperty(
	name="Modifiers List Index",
	description="Modifiers List Index",
)

classes = (
			ModifiersList_OT_ApplyAllModifiers,
			ModifiersList_OT_DeleteAllModifiers,
			ModifiersList_OT_ToggleApplyModifiersCage,
			ModifiersList_OT_ToggleApplyModifiersEditMode,
			ModifiersList_OT_ToggleApplyModifiersView,
			ModifiersList_OT_ToggleApplyModifiersRender,
			ModifiersList_OT_CopyToSelected_ListModifiers,
			ModifiersList_OT_CopyToSelected_ListModifiersAll,
			ModifiersList_OT_Duplicate_Modifiers_List,
			ModifiersList_OT_Apply_Modifiers_List,
			ModifiersList_OT_Delete_Modifiers_List,
			ModifiersList_OT_Duplicate_Modifier,
			ModifiersList_OT_Apply_Modifier,
			ModifiersList_OT_Delete_Modifier,
			ModifiersList_OT_Toggle_Modifiers_View,
			ModifiersList_OT_Solo_Modifiers_View,
			ModifiersList_OT_Show_Modifiers_View,
			ModifiersList_OT_List_Up,
			ModifiersList_OT_List_Down,
			ModifiersList_OT_List_First,
			ModifiersList_OT_List_Last,
			ModifiersList,
		  ) 

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

	bpy.types.DATA_PT_modifiers.prepend(KEN_MT_mod_menu_main)

	addon_prefs = addonPreferences.getAddonPreferences(bpy.context)
	use_modifier_panel = addon_prefs.use_modifier_panel
	if use_modifier_panel:
		from bpy.utils import register_class

		try:
			register_class(DATA_PT_modifiers)
			register_class(DATA_PT_gpencil_modifiers)
		except ValueError:
			pass
		

def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)

	bpy.types.DATA_PT_modifiers.remove(KEN_MT_mod_menu_main)

	try:
		unregister_class(DATA_PT_modifiers)
		unregister_class(DATA_PT_gpencil_modifiers)
		register_class(original_DATA_PT_modifiers)
		register_class(original_DATA_PT_gpencil_modifiers)
	except RuntimeError:
		pass
