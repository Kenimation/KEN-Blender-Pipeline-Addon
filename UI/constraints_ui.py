import bpy
import os
from bl_ui.properties_constraint import OBJECT_PT_constraints as original_OBJECT_PT_constraints
from bl_ui.properties_constraint import BONE_PT_constraints as original_BONE_PT_constraints
from .constraints_data import DATA_constraints
from .. import addonPreferences
from bpy.types import Operator, OperatorFileListElement, Panel
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty

con_targer = ["CHILD_OF", "TRACK_TO", "FOLLOW_PATH", "COPY_ROTATION", "COPY_LOCATION", "COPY_SCALE", "COPY_TRANSFORMS", "ACTION", "LOCKED_TRACK", "LIMIT_DISTANCE", "STRETCH_TO", "FLOOR", "CLAMP_TO", "TRANSFORM", "SHRINKWRAP", "DAMPED_TRACK", "SPLINE_IK", "PIVOT", "IK"]

def is_constraint_disabled(con):
	"""Checks if the name of the modifier should be diplayed with a red
	background.
	"""
	if con.type in con_targer:
		if not con.target:
			return True
	
	return False

class Disable_constraint(bpy.types.Operator):
    bl_idname = "disable.constraint"
    bl_label = "Disable Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    con: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        ob = bpy.context.object
        if context.object.mode == 'OBJECT':
            constraint = ob.constraints.get(self.con)
            if constraint:
                mw = ob.matrix_world.copy()
                constraint.influence = 0
                ob.matrix_world = mw
        elif context.object.mode == 'POSE':
            bone = context.active_pose_bone
            constraint = bone.constraints.get(self.con)
            if constraint:
                mw = bone.matrix.copy()
                constraint.influence = 0
                bone.matrix = mw
        return {"FINISHED"}

class Constraints_OT_List_Up(Operator):
	bl_idname = "constraints.list_up"
	bl_label = "Constraints List Move Up"
	bl_description = "Constraints List Move Up"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):

		try:
			if context.space_data.context != 'CONSTRAINT':
				return (len(context.active_pose_bone.constraints) > 0 and context.object.con_index > 0)
			else:
				return len(context.object.constraints) > 0 and context.object.con_index > 0
		except:
			if context.object.mode == 'POSE':
				return (len(context.active_pose_bone.constraints) > 0 and context.object.con_index > 0)
			else:
				return len(context.object.constraints) > 0 and context.object.con_index > 0

	def execute(self, context):
		owner = self.owner
		if owner == 'OBJECT':
			name = context.object.constraints[context.object.con_index].name

			if context.object.con_index == 0:
				context.object.con_index = len(context.object.constraints) - 1
			else:
				context.object.con_index -= 1
			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=context.object.con_index)
		elif owner == 'BONE':
			name = context.active_pose_bone.constraints[context.object.con_index].name

			if context.object.con_index == 0:
				context.object.con_index = len(context.active_pose_bone.constraints) - 1
			else:
				context.object.con_index -= 1
			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=context.object.con_index)
		return{'FINISHED'}

class Constraints_OT_List_Down(Operator):
	bl_idname = "constraints.list_down"
	bl_label = "Constraints List Move Down"
	bl_description = "Constraints List Move Down"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):
		
		try:
			if context.space_data.context != 'CONSTRAINT':
				return len(context.active_pose_bone.constraints) > 0 and (context.object.con_index < len(context.active_pose_bone.constraints) - 1)
			else:
				return len(context.object.constraints) > 0 and (context.object.con_index < len(context.object.constraints) - 1)
		except:
			if context.object.mode == 'POSE':
				return len(context.active_pose_bone.constraints) > 0 and (context.object.con_index < len(context.active_pose_bone.constraints) - 1)
			else:
				return len(context.object.constraints) > 0 and (context.object.con_index < len(context.object.constraints) - 1)

	def execute(self, context):
		owner = self.owner
		if owner == 'OBJECT':
			name = context.object.constraints[context.object.con_index].name

			if context.object.con_index == len(context.object.constraints) - 1:
				context.object.con_index = 0
			else:
				context.object.con_index += 1

			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=context.object.con_index)
		elif owner == 'BONE':
			name = context.active_pose_bone.constraints[context.object.con_index].name

			if context.object.con_index == len(context.active_pose_bone.constraints) - 1:
				context.object.con_index = 0
			else:
				context.object.con_index += 1

			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=context.object.con_index)

		return{'FINISHED'}

class Constraints_OT_List_First(Operator):
	bl_idname = "constraints.list_first"
	bl_label = "Constraints List Move to First"
	bl_description = "Constraints List Move to First"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):

		try:
			if context.space_data.context != 'CONSTRAINT':
				return (len(context.active_pose_bone.constraints) > 0 and context.object.con_index > 0)
			else:
				return len(context.object.constraints) > 0 and context.object.con_index > 0
		except:
			if context.object.mode == 'POSE':
				return (len(context.active_pose_bone.constraints) > 0 and context.object.con_index > 0)
			else:
				return len(context.object.constraints) > 0 and context.object.con_index > 0

	def execute(self, context):
		owner = self.owner
		if not context.object.con_index == 0:
			context.object.con_index = 0

		if owner == 'OBJECT':
			name = context.object.constraints[context.object.con_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=0)
		elif owner == 'BONE':
			name = context.active_pose_bone.constraints[context.object.con_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=0)
		return{'FINISHED'}

class Constraints_OT_List_Last(Operator):
	bl_idname = "constraints.list_last"
	bl_label = "Constraints List Move to Last"
	bl_description = "Constraints List Move to Last"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):

		try:
			if context.space_data.context != 'CONSTRAINT':
				return len(context.active_pose_bone.constraints) > 0 and (context.object.con_index < len(context.active_pose_bone.constraints) - 1)
			else:
				return len(context.object.constraints) > 0 and (context.object.con_index < len(context.object.constraints) - 1)
		except:
			if context.object.mode == 'POSE':
				return len(context.active_pose_bone.constraints) > 0 and (context.object.con_index < len(context.active_pose_bone.constraints) - 1)
			else:
				return len(context.object.constraints) > 0 and (context.object.con_index < len(context.object.constraints) - 1)
	
	def execute(self, context):
		owner = self.owner
		if owner == 'OBJECT':
			if not context.object.con_index == len(context.object.constraints) - 1:

				context.object.con_index = len(context.object.constraints) - 1

			name = context.object.constraints[context.object.con_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=len(context.object.constraints) - 1)
		elif owner == 'BONE':
			if not context.object.con_index == len(context.active_pose_bone.constraints) - 1:

				context.object.con_index = len(context.active_pose_bone.constraints) - 1

			name = context.active_pose_bone.constraints[context.object.con_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=len(context.active_pose_bone.constraints) - 1)

		return{'FINISHED'}

class KEN_OT_ToggleConstraints(Operator):
	bl_idname = "ken.toggle_constraints"
	bl_label = "Switch Constraints Enabled"
	bl_description = "Shows or hides all of constraints"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context != 'CONSTRAINT':
				for bone in context.selected_pose_bones:
					if bone.constraints:
						return True
			else:
				for obj in context.selected_objects:
					if obj.constraints:
						return True
		except:
			if context.object.mode == 'POSE':
				for bone in context.selected_pose_bones:
					if bone.constraints:
						return True
			else:
				for obj in context.selected_objects:
					if obj.constraints:
						return True
		return False

	def execute(self, context):
		owner = self.owner
		is_apply = True
		if owner == 'OBJECT':
			for con in context.active_object.constraints:
				if con.enabled:
					is_apply = False
					break
			for obj in context.selected_objects:
				for con in obj.constraints:
					con.enabled = is_apply
		elif owner == 'BONE':
			for con in context.active_pose_bone.constraints:
				if con.enabled:
					is_apply = False
					break
			for bone in context.selected_pose_bones:
				for con in bone.constraints:
					con.enabled = is_apply

		if is_apply:
			self.report(type={"INFO"}, message="Applied constraints to Enabled")
		else:
			self.report(type={"INFO"}, message="Unregistered constraints apply to Enabled")
		return {'FINISHED'}

class KEN_OT_ApplyAllConstraints(Operator):
	bl_idname = "ken.apply_all_constraints"
	bl_label = "Apply All Constraints"
	bl_description = "Applies to all constraints of selected object"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context != 'CONSTRAINT':
				for bone in context.selected_pose_bones:
					if bone.constraints:
						return True
			else:
				for obj in context.selected_objects:
					if obj.constraints:
						return True
		except:
			if context.object.mode == 'POSE':
				for bone in context.selected_pose_bones:
					if bone.constraints:
						return True
			else:
				for obj in context.selected_objects:
					if obj.constraints:
						return True
		return False

	def execute(self, context):
		owner = self.owner
		obj = context.object

		if owner == 'OBJECT':
			for obj in context.selected_objects:
				for con in obj.constraints[:]:
					bpy.ops.constraint.apply(constraint=con.name, owner = owner)
		elif owner == 'BONE':
			for bone in context.selected_pose_bones:
				for con in bone.constraints[:]:
					bpy.ops.constraint.apply(constraint=con.name, owner = owner)
		return {'FINISHED'}

class KEN_OT_DeleteAllConstraints(Operator):
	bl_idname = "ken.delete_all_constraints"
	bl_label = "Remove All Constraints"
	bl_description = "Remove all constraints of selected object"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context != 'CONSTRAINT':
				for bone in context.selected_pose_bones:
					if bone.constraints:
						return True
			else:
				for obj in context.selected_objects:
					if obj.constraints:
						return True
		except:
			if context.object.mode == 'POSE':
				for bone in context.selected_pose_bones:
					if bone.constraints:
						return True
			else:
				for obj in context.selected_objects:
					if obj.constraints:
						return True
		return False

	def execute(self, context):
		owner = self.owner
		obj = context.object

		if owner == 'OBJECT':
			for obj in context.selected_objects:
				for con in obj.constraints[:]:
					obj.constraints.remove(con)
		elif owner == 'BONE':
			for bone in context.selected_pose_bones:
				for con in bone.constraints[:]:
					bone.constraints.remove(con)
		return {'FINISHED'}

class KEN_OT_CopyToSelected_ListConstraintsAll(Operator):
	bl_idname = "ken.copy_to_selected_constraints_list_all"
	bl_label = "Copy All Constraints To Selected"
	bl_description = "Copy All Constraints To Selected"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context != 'CONSTRAINT':
				for bone in context.selected_pose_bones:
					if bone.constraints:
						return True
			else:
				for obj in context.selected_objects:
					if obj.constraints:
						return True
		except:
			if context.object.mode == 'POSE':
				for bone in context.selected_pose_bones:
					if bone.constraints:
						return True
			else:
				for obj in context.selected_objects:
					if obj.constraints:
						return True
		return False

	def execute(self, context):
		owner = self.owner
		obj = context.object
		if owner == 'OBJECT':
			for con in context.object.constraints[:]:
				bpy.ops.constraint.copy_to_selected(constraint=con.name, owner = owner)
		elif owner == 'BONE':
			for con in context.active_pose_bone.constraints[:]:
				bpy.ops.constraint.copy_to_selected(constraint=con.name, owner = owner)

		return {'FINISHED'}

class KEN_OT_CopyToSelected_ListConstraints(Operator):
	bl_idname = "ken.copy_to_selected_constraints_list"
	bl_label = "Copy To Selected Constraints"
	bl_description = "Copy To Selected Constraints"
	bl_options = {'REGISTER', 'UNDO'}
	
	name: bpy.props.StringProperty(options={'HIDDEN'})
	owner: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		bpy.ops.constraint.copy_to_selected(constraint=self.name, owner = self.owner)
		return {'FINISHED'}

class KEN_OT_DeleteListConstraints(Operator):
	bl_idname = "ken.delete_constraints_list"
	bl_label = "Delete Constraints List"
	bl_description = "Delete Constraints"
	bl_options = {'REGISTER', 'UNDO'}
	
	name: bpy.props.StringProperty(options={'HIDDEN'})
	owner: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		bpy.ops.constraint.delete(constraint=self.name, owner = self.owner)
		return {'FINISHED'}

class Apply_Constraints(bpy.types.Operator):
	bl_idname = "apply.constraints"
	bl_label = "Apply Constraints"
	bl_options = {'REGISTER', 'UNDO'}

	name: bpy.props.StringProperty(options={'HIDDEN'})
	owner: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		bpy.ops.constraint.apply(constraint=self.name, owner = self.owner)
		return {"FINISHED"}

class Duplicate_Constraints(bpy.types.Operator):
	bl_idname = "duplicate.constraints"
	bl_label = "Duplicate Constraints"
	bl_options = {'REGISTER', 'UNDO'}

	name: bpy.props.StringProperty(options={'HIDDEN'})
	owner: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		bpy.ops.constraint.copy(constraint=self.name, owner = self.owner)
		return {"FINISHED"}

class Constraints(bpy.types.UIList):
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
		constraints = item
		# draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			# You should always start your row layout by a label (icon + text), or a non-embossed text field,
			# this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
			# We use icon_value of label, as our given i
			# con is an integer value, not an enum ID.
			# Note "data" names should never be translated!

			if constraints:
				owner = "OBJECT"
				duplicate = layout.operator("duplicate.constraints", text="", emboss=False, icon = "LAYER_ACTIVE" if index == context.object.con_index else "LAYER_USED")
				duplicate.name = constraints.name
				duplicate.owner = owner
				row = layout.row()
				row.alert = is_constraint_disabled(constraints)
				row.label(text="", icon_value=layout.icon(constraints))
				layout.prop(constraints, "name", text="", emboss=False)
				layout.prop(constraints, "enabled", text="", icon = "HIDE_ON", emboss=False)
				if len(context.selected_objects) > 1:
					copy = layout.operator("ken.copy_to_selected_constraints_list", emboss = False, icon='COPYDOWN', text="")
					copy.name = constraints.name
					copy.owner = owner
				apply = layout.operator("apply.constraints", emboss=False, icon='CHECKMARK', text="")
				apply.name = constraints.name
				apply.owner = owner
				delete = layout.operator("ken.delete_constraints_list", emboss=False, icon='X', text="")
				delete.name = constraints.name
				delete.owner = owner

		# 'GRID' layout type should be as compact as possible (typically a single icon!).
		elif self.layout_type == 'GRID':
			layout.alignment = 'CENTER'
			layout.label(text="", icon_value=icon)

class BONE_Constraints(bpy.types.UIList):
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
		constraints = item
		# draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			# You should always start your row layout by a label (icon + text), or a non-embossed text field,
			# this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
			# We use icon_value of label, as our given i
			# con is an integer value, not an enum ID.
			# Note "data" names should never be translated!

			if constraints:
				owner = "BONE"
				duplicate = layout.operator("duplicate.constraints", text="", emboss=False, icon = "LAYER_ACTIVE" if index == context.object.con_index else "LAYER_USED")
				duplicate.name = constraints.name
				duplicate.owner = owner
				row = layout.row()
				row.alert = is_constraint_disabled(constraints)
				row.label(text="", icon_value=layout.icon(constraints))
				layout.prop(constraints, "name", text="", emboss=False)
				layout.prop(constraints, "enabled", text="", icon = "HIDE_ON", emboss=False)
				if len(context.selected_pose_bones) > 1:
					copy = layout.operator("ken.copy_to_selected_constraints_list", emboss = False, icon='COPYDOWN', text="")
					copy.name = constraints.name
					copy.owner = owner
				apply = layout.operator("apply.constraints", emboss=False, icon='CHECKMARK', text="")
				apply.name = constraints.name
				apply.owner = owner
				delete = layout.operator("ken.delete_constraints_list", emboss=False, icon='X', text="")
				delete.name = constraints.name
				delete.owner = owner

		# 'GRID' layout type should be as compact as possible (typically a single icon!).
		elif self.layout_type == 'GRID':
			layout.alignment = 'CENTER'
			layout.label(text="", icon_value=icon)

class ObjectConstraintPanel:
	bl_context = "constraint"

	@classmethod
	def poll(cls, context):
		return (context.object)

class BoneConstraintPanel:
	bl_context = "bone_constraint"

	@classmethod
	def poll(cls, context):
		return (context.pose_bone)

class OBJECT_PT_constraints(ObjectConstraintPanel, Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_label = "Object Constraints"
	bl_options = {'HIDE_HEADER'}
	
	def draw(self, context):
		addon_prefs = addonPreferences.getAddonPreferences(context)
		layout = self.layout
		scene = context.scene
		obj = context.object
		row = layout.row()
		
		lrow = row.row()
		lrow.alignment = 'LEFT'
		lrow.prop(addon_prefs, "use_constraint_panel", text = "Object Constraint List", icon = "CONSTRAINT", emboss = False)
		row = row.row()
		row.alignment = 'RIGHT'

		owner = "OBJECT"
		drawconstraints(self, context, layout, owner, row, obj)

class BONE_PT_constraints(BoneConstraintPanel, Panel):
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_label = "Object Constraints"
	bl_options = {'HIDE_HEADER'}

	def draw(self, context):
		addon_prefs = addonPreferences.getAddonPreferences(context)
		layout = self.layout
		scene = context.scene
		obj = context.object
		row = layout.row()
		
		lrow = row.row()
		lrow.alignment = 'LEFT'
		lrow.prop(addon_prefs, "use_constraint_panel", text = "Bone Constraint List", icon = "CONSTRAINT_BONE", emboss = False)
		row = row.row()
		row.alignment = 'RIGHT'

		owner = "BONE"
		draw_boneconstraints(self, context, layout, owner, row, obj)

def drawconstraints(self, context, layout, owner, row, obj):
	scene = context.scene
	bone = context.active_pose_bone
	if obj.constraints:
		row.operator("ken.toggle_constraints", emboss = False, icon='HIDE_OFF', text="").owner = owner
		if len(context.selected_objects) > 1:
			row.operator("ken.copy_to_selected_constraints_list_all", emboss = False, icon='COPYDOWN', text="").owner = owner
		row.operator("ken.apply_all_constraints", emboss = False, icon='CHECKMARK', text="").owner = owner
		row.operator("ken.delete_all_constraints", emboss = False, icon='X', text="").owner = owner

	if scene.con_panel == True:
		icon ="FULLSCREEN_ENTER"
	else:
		icon ="FULLSCREEN_EXIT"
		
	row.prop(scene, "con_panel", emboss = False, icon=icon, text="")

	layout.operator_menu_enum("object.constraint_add", "type", text="Add Object Constraint")
	row = layout.row()
	row.template_list("Constraints", "", obj, "constraints", obj, "con_index")

	col = row.column()
	col.operator("constraints.list_first", text="", icon='TRIA_UP_BAR').owner = owner
	col.operator("constraints.list_up", text="", icon='TRIA_UP').owner = owner
	col.operator("constraints.list_down", text="", icon='TRIA_DOWN').owner = owner
	col.operator("constraints.list_last", text="", icon='TRIA_DOWN_BAR').owner = owner

	if context.scene.con_panel == True:
		try:
			con_list = []
			for con in obj.constraints:
				con_list.append(con)
			constraints = con_list[obj.con_index]

			# === General settings ===
			box = layout.box()

			row = box.row()

			duplicate = row.operator("duplicate.constraints", text="", emboss=False, icon = "LAYER_ACTIVE")
			duplicate.name = constraints.name
			duplicate.owner = owner
			lrow = row.row()
			lrow.alert = is_constraint_disabled(constraints)
			lrow.label(text="", icon_value=layout.icon(constraints))
			row.prop(constraints, "name", text = "")
			row.prop(constraints, "enabled", text="", icon = "HIDE_ON", emboss=False)
			if len(context.selected_objects) > 1:
				copy = row.operator("ken.copy_to_selected_constraints_list", emboss = False, icon='COPYDOWN', text="")
				copy.name = constraints.name
				copy.owner = owner
			apply = row.operator("apply.constraints", emboss=False, icon='CHECKMARK', text="")
			apply.name = constraints.name
			apply.owner = owner
			delete = row.operator("ken.delete_constraints_list", emboss=False, icon='X', text="")
			delete.name = constraints.name
			delete.owner = owner

			mp = DATA_constraints(context)
			getattr(mp, constraints.type)(box, obj, constraints, owner)

		except:
			layout.label(text = "No Constraint has selected.")

def draw_boneconstraints(self, context, layout, owner, row, obj):
	scene = context.scene
	bone = context.active_pose_bone
	if obj.mode == "POSE":
		if context.active_pose_bone.constraints:
			row.operator("ken.toggle_constraints", emboss = False, icon='HIDE_OFF', text="").owner = owner
			if len(context.selected_pose_bones) > 1:
				row.operator("ken.copy_to_selected_constraints_list_all", emboss = False, icon='COPYDOWN', text="").owner = owner
			row.operator("ken.apply_all_constraints", emboss = False, icon='CHECKMARK', text="").owner = owner
			row.operator("ken.delete_all_constraints", emboss = False, icon='X', text="").owner = owner

	if scene.con_panel == True:
		icon ="FULLSCREEN_ENTER"
	else:
		icon ="FULLSCREEN_EXIT"
		
	row.prop(scene, "con_panel", emboss = False, icon=icon, text="")

	layout.operator_menu_enum("pose.constraint_add", "type", text="Add Bone Constraint")
	row = layout.row()
	row.template_list("BONE_Constraints", "", bone, "constraints", obj, "con_index")

	col = row.column()
	col.operator("constraints.list_first", text="", icon='TRIA_UP_BAR').owner = owner
	col.operator("constraints.list_up", text="", icon='TRIA_UP').owner = owner
	col.operator("constraints.list_down", text="", icon='TRIA_DOWN').owner = owner
	col.operator("constraints.list_last", text="", icon='TRIA_DOWN_BAR').owner = owner

	if obj.mode == "POSE":
		if context.scene.con_panel == True:
			try:
				con_list = []
				for con in context.active_pose_bone.constraints:
					con_list.append(con)
				constraints = con_list[obj.con_index]
				
				# === General settings ===
				box = layout.box()

				row = box.row()

				duplicate = row.operator("duplicate.constraints", text="", emboss=False, icon = "LAYER_ACTIVE")
				duplicate.name = constraints.name
				duplicate.owner = owner
				lrow = row.row()
				lrow.alert = is_constraint_disabled(constraints)
				lrow.label(text="", icon_value=layout.icon(constraints))
				row.prop(constraints, "name", text = "")
				row.prop(constraints, "enabled", text="", icon = "HIDE_ON", emboss=False)
				if len(context.selected_pose_bones) > 1:
					copy = row.operator("ken.copy_to_selected_constraints_list", emboss = False, icon='COPYDOWN', text="")
					copy.name = constraints.name
					copy.owner = owner
				apply = row.operator("apply.constraints", emboss=False, icon='CHECKMARK', text="")
				apply.name = constraints.name
				apply.owner = owner
				delete = row.operator("ken.delete_constraints_list", emboss=False, icon='X', text="")
				delete.name = constraints.name
				delete.owner = owner

				mp = DATA_constraints(context)
				getattr(mp, constraints.type)(box, obj, constraints, owner)

			except:
				layout.label(text = "No Constraint has selected.")

	else:
		layout.label(text = "Object mode is not Pose mode.")
		layout.operator("object.posemode_toggle", text = "Toggle Pose Mode")

def KEN_MT_con_menu_main(self, context):
	addon_prefs = addonPreferences.getAddonPreferences(context)
	if (context.active_object):
		# if (len(context.active_object.modifiers)):
		lrow = self.layout.row(align=True)
		row = lrow.row(align=True)
		row.alignment = 'LEFT'
		row.prop(addon_prefs, "use_constraint_panel", text = "Toggle Constraint List", icon = "CONSTRAINT", emboss = False)

def KEN_MT_bcon_menu_main(self, context):
	addon_prefs = addonPreferences.getAddonPreferences(context)
	if (context.active_object):
		# if (len(context.active_object.modifiers)):
		lrow = self.layout.row(align=True)
		row = lrow.row(align=True)
		row.alignment = 'LEFT'
		row.prop(addon_prefs, "use_constraint_panel", text = "Toggle Bone Constraint List", icon = "CONSTRAINT_BONE", emboss = False)

def ken_constraint_panel(self, context):
	addon_prefs = addonPreferences.getAddonPreferences(context)
	use_constraint_panel = addon_prefs.use_constraint_panel

	from bpy.utils import register_class, unregister_class

	if use_constraint_panel:
		try:
			register_class(OBJECT_PT_constraints)
			register_class(BONE_PT_constraints)
		except ValueError:
			unregister_class(OBJECT_PT_constraints)
			unregister_class(BONE_PT_constraints)
			register_class(original_OBJECT_PT_constraints)
			register_class(original_BONE_PT_constraints)
	else:
		try:
			unregister_class(OBJECT_PT_constraints)
			unregister_class(BONE_PT_constraints)
			register_class(original_OBJECT_PT_constraints)
			register_class(original_BONE_PT_constraints)
		except RuntimeError:
			pass

bpy.types.Scene.con_panel = bpy.props.BoolProperty(
	name="Expand Constraints Settings",
	description="Expand Constraint Settings Panel",
)

bpy.types.Object.con_index = bpy.props.IntProperty(
	name="Constraints List Index",
	description="Constraints List Index",
)

classes = (
	Disable_constraint,
	Constraints_OT_List_Up,
	Constraints_OT_List_Down,
	Constraints_OT_List_First,
	Constraints_OT_List_Last,
	KEN_OT_ToggleConstraints,
	KEN_OT_ApplyAllConstraints,
	KEN_OT_DeleteAllConstraints,
	KEN_OT_CopyToSelected_ListConstraintsAll,
	KEN_OT_CopyToSelected_ListConstraints,
	KEN_OT_DeleteListConstraints,
	Apply_Constraints,
	Duplicate_Constraints,
	Constraints,
	BONE_Constraints,
		  ) 

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

	bpy.types.OBJECT_PT_constraints.prepend(KEN_MT_con_menu_main)
	bpy.types.BONE_PT_constraints.prepend(KEN_MT_bcon_menu_main)

	addon_prefs = addonPreferences.getAddonPreferences(bpy.context)
	use_constraint_panel = addon_prefs.use_constraint_panel
	if use_constraint_panel:
		from bpy.utils import register_class

		try:
			register_class(OBJECT_PT_constraints)
			register_class(BONE_PT_constraints)
		except ValueError:
			pass
		
def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)
	
	bpy.types.OBJECT_PT_constraints.remove(KEN_MT_con_menu_main)
	bpy.types.BONE_PT_constraints.remove(KEN_MT_bcon_menu_main)

	try:
		unregister_class(OBJECT_PT_constraints)
		unregister_class(BONE_PT_constraints)
		register_class(original_OBJECT_PT_constraints)
		register_class(original_BONE_PT_constraints)
	except RuntimeError:
		pass