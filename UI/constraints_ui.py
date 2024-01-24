import bpy
import os
from bl_ui.properties_constraint import OBJECT_PT_constraints as original_OBJECT_PT_constraints
from bl_ui.properties_constraint import BONE_PT_constraints as original_BONE_PT_constraints
from .constraints_data import DATA_constraints
from .. import addonPreferences
from bpy.types import Operator, Panel, Menu
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
	owner: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		ob = context.object
		if self.owner == 'BONE':
			bone = context.pose_bone
			con = bone.constraints.get(self.con)
			mat = ob.matrix_world @ bone.matrix
		else:
			con = ob.constraints.get(self.con)
			mat = ob.matrix_world

		con.influence = 0.0

		# Set the matrix.
		if self.owner == 'BONE':
			bone.matrix = ob.matrix_world.inverted() @ mat
		else:
			ob.matrix_world = mat
		return {"FINISHED"}

class Constraints_OT_List_Up(Operator):
	bl_idname = "constraints_list.constraints_list_up"
	bl_label = "Constraints List Move Up"
	bl_description = "Constraints List Move Up"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'CONSTRAINT':
			return len(context.object.constraints) > 0 and context.object.con_index > 0
		elif context.space_data.context == 'BONE_CONSTRAINT':
			return (len(context.active_pose_bone.constraints) > 0 and context.object.bcon_index > 0)

	def execute(self, context):
		if context.space_data.context == 'CONSTRAINT':
			name = context.object.constraints[context.object.con_index].name

			if context.object.con_index == 0:
				context.object.con_index = len(context.object.constraints) - 1
			else:
				context.object.con_index -= 1
			bpy.ops.constraint.move_to_index(constraint=name, owner="OBJECT", index=context.object.con_index)
		elif context.space_data.context == 'BONE_CONSTRAINT':
			name = context.active_pose_bone.constraints[context.object.bcon_index].name

			if context.object.bcon_index == 0:
				context.object.bcon_index = len(context.active_pose_bone.constraints) - 1
			else:
				context.object.bcon_index -= 1
			bpy.ops.constraint.move_to_index(constraint=name, owner="BONE", index=context.object.bcon_index)
		return{'FINISHED'}

class Constraints_OT_List_Down(Operator):
	bl_idname = "constraints_list.constraints_list_down"
	bl_label = "Constraints List Move Down"
	bl_description = "Constraints List Move Down"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'CONSTRAINT':
			return len(context.object.constraints) > 0 and (context.object.con_index < len(context.object.constraints) - 1)
		elif context.space_data.context == 'BONE_CONSTRAINT':
			return len(context.active_pose_bone.constraints) > 0 and (context.object.bcon_index < len(context.active_pose_bone.constraints) - 1)

	def execute(self, context):
		if context.space_data.context == 'CONSTRAINT':
			name = context.object.constraints[context.object.con_index].name

			if context.object.con_index == len(context.object.constraints) - 1:
				context.object.con_index = 0
			else:
				context.object.con_index += 1

			bpy.ops.constraint.move_to_index(constraint=name, owner="OBJECT", index=context.object.con_index)
		elif context.space_data.context == 'BONE_CONSTRAINT':
			name = context.active_pose_bone.constraints[context.object.bcon_index].name

			if context.object.bcon_index == len(context.active_pose_bone.constraints) - 1:
				context.object.bcon_index = 0
			else:
				context.object.bcon_index += 1

			bpy.ops.constraint.move_to_index(constraint=name, owner="BONE", index=context.object.bcon_index)

		return{'FINISHED'}

class Constraints_OT_List_First(Operator):
	bl_idname = "constraints_list.constraints_list_first"
	bl_label = "Constraints List Move to First"
	bl_description = "Constraints List Move to First"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'CONSTRAINT':
			return len(context.object.constraints) > 0 and context.object.con_index > 0
		elif context.space_data.context == 'BONE_CONSTRAINT':
			return (len(context.active_pose_bone.constraints) > 0 and context.object.bcon_index > 0)

	def execute(self, context):
		if context.space_data.context == 'CONSTRAINT':
			name = context.object.constraints[context.object.con_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner='OBJECT', index=0)
			if not context.object.con_index == 0:
				context.object.con_index = 0
		elif context.space_data.context == 'BONE_CONSTRAINT':
			name = context.active_pose_bone.constraints[context.object.bcon_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner='BONE', index=0)
			if not context.object.bcon_index == 0:
				context.object.bcon_index = 0
		return{'FINISHED'}

class Constraints_OT_List_Last(Operator):
	bl_idname = "constraints_list.constraints_list_last"
	bl_label = "Constraints List Move to Last"
	bl_description = "Constraints List Move to Last"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'CONSTRAINT':
			return len(context.object.constraints) > 0 and (context.object.con_index < len(context.object.constraints) - 1)

		elif context.space_data.context == 'BONE_CONSTRAINT':
			return len(context.active_pose_bone.constraints) > 0 and (context.object.bcon_index < len(context.active_pose_bone.constraints) - 1)
	
	def execute(self, context):
		if context.space_data.context == 'CONSTRAINT':
			name = context.object.constraints[context.object.con_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner="OBJECT", index=len(context.object.constraints) - 1)
			if not context.object.con_index == len(context.object.constraints) - 1:

				context.object.con_index = len(context.object.constraints) - 1
		elif context.space_data.context == 'BONE_CONSTRAINT':
			name = context.active_pose_bone.constraints[context.object.bcon_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner="BONE", index=len(context.active_pose_bone.constraints) - 1)
			if not context.object.bcon_index == len(context.active_pose_bone.constraints) - 1:

				context.object.bcon_index = len(context.active_pose_bone.constraints) - 1

		return{'FINISHED'}

class Constraints_OT_List_Up_Button(Operator):
	bl_idname = "constraints_list.constraints_list_up_button"
	bl_label = "Constraints List Move Up"
	bl_description = "Constraints List Move Up"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):

		try:
			if context.space_data.context != 'CONSTRAINT':
				return (len(context.active_pose_bone.constraints) > 0 and context.object.bcon_index > 0)
			else:
				return len(context.object.constraints) > 0 and context.object.con_index > 0
		except:
			if context.object.mode == 'POSE':
				return (len(context.active_pose_bone.constraints) > 0 and context.object.bcon_index > 0)
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
			name = context.active_pose_bone.constraints[context.object.bcon_index].name

			if context.object.bcon_index == 0:
				context.object.bcon_index = len(context.active_pose_bone.constraints) - 1
			else:
				context.object.bcon_index -= 1
			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=context.object.bcon_index)
		return{'FINISHED'}

class Constraints_OT_List_Down_Button(Operator):
	bl_idname = "constraints_list.constraints_list_down_button"
	bl_label = "Constraints List Move Down"
	bl_description = "Constraints List Move Down"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):
		
		try:
			if context.space_data.context != 'CONSTRAINT':
				return len(context.active_pose_bone.constraints) > 0 and (context.object.bcon_index < len(context.active_pose_bone.constraints) - 1)
			else:
				return len(context.object.constraints) > 0 and (context.object.con_index < len(context.object.constraints) - 1)
		except:
			if context.object.mode == 'POSE':
				return len(context.active_pose_bone.constraints) > 0 and (context.object.bcon_index < len(context.active_pose_bone.constraints) - 1)
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
			name = context.active_pose_bone.constraints[context.object.bcon_index].name

			if context.object.bcon_index == len(context.active_pose_bone.constraints) - 1:
				context.object.bcon_index = 0
			else:
				context.object.bcon_index += 1

			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=context.object.bcon_index)

		return{'FINISHED'}

class Constraints_OT_List_First_Button(Operator):
	bl_idname = "constraints_list.constraints_list_first_button"
	bl_label = "Constraints List Move to First"
	bl_description = "Constraints List Move to First"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):
		try:
			if context.space_data.context != 'CONSTRAINT':
				return (len(context.active_pose_bone.constraints) > 0 and context.object.bcon_index > 0)
			else:
				return len(context.object.constraints) > 0 and context.object.con_index > 0
		except:
			if context.object.mode == 'POSE':
				return (len(context.active_pose_bone.constraints) > 0 and context.object.bcon_index > 0)
			else:
				return len(context.object.constraints) > 0 and context.object.con_index > 0

	def execute(self, context):
		owner = self.owner
		if owner == 'OBJECT':
			name = context.object.constraints[context.object.con_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=0)
			if not context.object.con_index == 0:
				context.object.con_index = 0
		elif owner == 'BONE':
			name = context.active_pose_bone.constraints[context.object.bcon_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=0)
			if not context.object.bcon_index == 0:
				context.object.bcon_index = 0
		return{'FINISHED'}

class Constraints_OT_List_Last_Button(Operator):
	bl_idname = "constraints_list.constraints_list_last_button"
	bl_label = "Constraints List Move to Last"
	bl_description = "Constraints List Move to Last"
	bl_options = {'REGISTER', 'UNDO'}

	owner: bpy.props.StringProperty(options={'HIDDEN'})

	@classmethod
	def poll(cls, context):

		try:
			if context.space_data.context != 'CONSTRAINT':
				return len(context.active_pose_bone.constraints) > 0 and (context.object.bcon_index < len(context.active_pose_bone.constraints) - 1)
			else:
				return len(context.object.constraints) > 0 and (context.object.con_index < len(context.object.constraints) - 1)
		except:
			if context.object.mode == 'POSE':
				return len(context.active_pose_bone.constraints) > 0 and (context.object.bcon_index < len(context.active_pose_bone.constraints) - 1)
			else:
				return len(context.object.constraints) > 0 and (context.object.con_index < len(context.object.constraints) - 1)
	
	def execute(self, context):
		owner = self.owner
		if owner == 'OBJECT':
			name = context.object.constraints[context.object.con_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=len(context.object.constraints) - 1)
			if not context.object.con_index == len(context.object.constraints) - 1:

				context.object.con_index = len(context.object.constraints) - 1
		elif owner == 'BONE':
			name = context.active_pose_bone.constraints[context.object.bcon_index].name
			bpy.ops.constraint.move_to_index(constraint=name, owner=owner, index=len(context.active_pose_bone.constraints) - 1)
			if not context.object.bcon_index == len(context.active_pose_bone.constraints) - 1:

				context.object.bcon_index = len(context.active_pose_bone.constraints) - 1

		return{'FINISHED'}

class Constraints_OT_ToggleConstraints(Operator):
	bl_idname = "constraints_list.toggle_constraints"
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

class Constraints_OT_ApplyAllConstraints(Operator):
	bl_idname = "constraints_list.apply_all_constraints"
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

class Constraints_OT_DeleteAllConstraints(Operator):
	bl_idname = "constraints_list.delete_all_constraints"
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

class Constraints_OT_CopyToSelected_ListConstraintsAll(Operator):
	bl_idname = "constraints_list.copy_to_selected_constraints_list_all"
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

class Constraints_OT_CopyToSelected_ListConstraints(Operator):
	bl_idname = "constraints_list.copy_to_selected_constraints_list"
	bl_label = "Copy To Selected Constraints"
	bl_description = "Copy To Selected Constraints"
	bl_options = {'REGISTER', 'UNDO'}
	
	name: bpy.props.StringProperty(options={'HIDDEN'})
	owner: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		bpy.ops.constraint.copy_to_selected(constraint=self.name, owner = self.owner)
		return {'FINISHED'}

class Constraints_OT_Delete_Constraints_List(Operator):
	bl_idname = "constraints_list.delete_constraints_list"
	bl_label = "Delete Constraints List"
	bl_description = "Delete Constraints"
	bl_options = {'REGISTER', 'UNDO'}
	
	name: bpy.props.StringProperty(options={'HIDDEN'})
	owner: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		obj = context.object
		bpy.ops.constraint.delete(constraint=self.name, owner = self.owner)
		if self.owner == "OBJECT":
			if obj.con_index != 0:
				obj.con_index = obj.con_index - 1
		elif self.owner == "BONE":
			if obj.bcon_index != 0:
				obj.bcon_index = obj.bcon_index - 1
		return {'FINISHED'}

class Constraints_OT_Apply_Constraints_List(bpy.types.Operator):
	bl_idname = "constraints_list.apply_constraints_list"
	bl_label = "Apply Constraints"
	bl_options = {'REGISTER', 'UNDO'}

	name: bpy.props.StringProperty(options={'HIDDEN'})
	owner: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		obj = context.object
		bpy.ops.constraint.apply(constraint=self.name, owner = self.owner)
		if self.owner == "OBJECT":
			if obj.con_index != 0:
				obj.con_index = obj.con_index - 1
		elif self.owner == "BONE":
			if obj.bcon_index != 0:
				obj.bcon_index = obj.bcon_index - 1
		
		return {"FINISHED"}

class Constraints_OT_Duplicate_Constraints_List(bpy.types.Operator):
	bl_idname = "constraints_list.duplicate_constraints_list"
	bl_label = "Duplicate Constraints"
	bl_options = {'REGISTER', 'UNDO'}

	name: bpy.props.StringProperty(options={'HIDDEN'})
	owner: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		obj = context.object
		bpy.ops.constraint.copy(constraint=self.name, owner = self.owner)

		if self.owner == "OBJECT":
			obj.con_index = obj.con_index + 1
		elif self.owner == "BONE":
			obj.bcon_index = obj.bcon_index + 1
		return {"FINISHED"}

class Constraints_OT_Delete_Constraints(Operator):
	bl_idname = "constraints_list.delete_constraint"
	bl_label = "Delete Constraints List"
	bl_description = "Delete Constraints"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'CONSTRAINT' or context.space_data.context == 'BONE_CONSTRAINT':
			return True
		return False
	
	def execute(self, context):
		obj = context.object
		bone = context.active_pose_bone
		if context.space_data.context == 'CONSTRAINT':
			con_list = []
			for con in obj.constraints:
				con_list.append(con)
			constraints = con_list[obj.con_index]
			owner = "OBJECT"

		elif context.space_data.context == 'BONE_CONSTRAINT':
			con_list = []
			for con in bone.constraints:
				con_list.append(con)
			constraints = con_list[obj.bcon_index]
			owner = "BONE"

		bpy.ops.constraint.delete(constraint=constraints.name, owner = owner)

		if owner == "OBJECT":
			if obj.con_index != 0:
				obj.con_index = obj.con_index - 1
		elif owner == "BONE":
			if obj.bcon_index != 0:
				obj.bcon_index = obj.bcon_index - 1

		return {'FINISHED'}

class Constraints_OT_Apply_Constraints(bpy.types.Operator):
	bl_idname = "constraints_list.apply_constraint"
	bl_label = "Apply Constraints"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'CONSTRAINT' or context.space_data.context == 'BONE_CONSTRAINT':
			return True
		return False

	def execute(self, context):
		obj = context.object
		bone = context.active_pose_bone
		if context.space_data.context == 'CONSTRAINT':
			con_list = []
			for con in obj.constraints:
				con_list.append(con)
			constraints = con_list[obj.con_index]
			owner = "OBJECT"

		elif context.space_data.context == 'BONE_CONSTRAINT':
			con_list = []
			for con in bone.constraints:
				con_list.append(con)
			constraints = con_list[obj.bcon_index]
			owner = "BONE"

		bpy.ops.constraint.apply(constraint=constraints.name, owner = owner)

		if owner == "OBJECT":
			if obj.con_index != 0:
				obj.con_index = obj.con_index - 1
		elif owner == "BONE":
			if obj.bcon_index != 0:
				obj.bcon_index = obj.bcon_index - 1

		return {"FINISHED"}

class Constraints_OT_Duplicate_Constraints(bpy.types.Operator):
	bl_idname = "constraints_list.duplicate_constraint"
	bl_label = "Duplicate Constraints"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'CONSTRAINT' or context.space_data.context == 'BONE_CONSTRAINT':
			return True
		return False

	def execute(self, context):
		obj = context.object
		bone = context.active_pose_bone
		if context.space_data.context == 'CONSTRAINT':
			con_list = []
			for con in obj.constraints:
				con_list.append(con)
			constraints = con_list[obj.con_index]
			owner = "OBJECT"

		elif context.space_data.context == 'BONE_CONSTRAINT':
			con_list = []
			for con in bone.constraints:
				con_list.append(con)
			constraints = con_list[obj.bcon_index]
			owner = "BONE"

		bpy.ops.constraint.copy(constraint=constraints.name, owner = owner)

		if owner == "OBJECT":
			obj.con_index = obj.con_index + 1
		elif owner == "BONE":
			obj.bcon_index = obj.bcon_index + 1

		return {"FINISHED"}

class Constraints_OT_Toggle_Constraints_View(bpy.types.Operator):
	bl_idname = "constraints_list.toggle_constraints_view"
	bl_label = "Toggle Constraints View"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'CONSTRAINT' or context.space_data.context == 'BONE_CONSTRAINT':
			return True
		return False

	def execute(self, context):
		obj = context.object
		bone = context.active_pose_bone
		if context.space_data.context == 'CONSTRAINT':
			con_list = []
			for con in obj.constraints:
				con_list.append(con)
			constraints = con_list[obj.con_index]
			con = obj.constraints[constraints.name]
			if con.enabled == True:
				con.enabled = False
			else:
				con.enabled = True

		elif context.space_data.context == 'BONE_CONSTRAINT':
			con_list = []
			for con in bone.constraints:
				con_list.append(con)
			constraints = con_list[obj.bcon_index]
			con = bone.constraints[constraints.name]
			if con.enabled == True:
				con.enabled = False
			else:
				con.enabled = True

		return {"FINISHED"}

class Constraints_OT_Solo_Constraints_View(bpy.types.Operator):
	bl_idname = "constraints_list.solo_constraints_view"
	bl_label = "Solo Constraints List"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'CONSTRAINT' or context.space_data.context == 'BONE_CONSTRAINT':
			return True
		return False

	def execute(self, context):
		obj = context.object
		bone = context.active_pose_bone
		if context.space_data.context == 'CONSTRAINT':
			con_list = []
			for con in obj.constraints:
				con_list.append(con)
			for con in obj.constraints:
				if con != con_list[obj.con_index]:
					con.enabled = False
				else:
					con.enabled = True

		elif context.space_data.context == 'BONE_CONSTRAINT':
			con_list = []
			for con in bone.constraints:
				con_list.append(con)
			for con in bone.constraints:
				if con != con_list[obj.bcon_index]:
					con.enabled = False
				else:
					con.enabled = True
				
		return {"FINISHED"}

class Constraints_OT_Show_Constraints_View(bpy.types.Operator):
	bl_idname = "constraints_list.show_constraints_view"
	bl_label = "Show All Constraints List"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.space_data.context == 'CONSTRAINT' or context.space_data.context == 'BONE_CONSTRAINT':
			return True
		return False

	def execute(self, context):
		obj = context.object
		bone = context.active_pose_bone
		if context.space_data.context == 'CONSTRAINT':
			for con in obj.constraints:
				con.enabled = True

		elif context.space_data.context == 'BONE_CONSTRAINT':
			for con in bone.constraints:
				con.enabled = True
				
		return {"FINISHED"}

class ConstraintsList(bpy.types.UIList):
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
				duplicate = layout.operator("constraints_list.duplicate_constraints_list", text="", emboss=False, icon = "LAYER_ACTIVE" if index == context.object.con_index else "LAYER_USED")
				duplicate.name = constraints.name
				duplicate.owner = owner
				row = layout.row()
				row.alert = is_constraint_disabled(constraints)
				row.label(text="", icon_value=layout.icon(constraints))
				layout.prop(constraints, "name", text="", emboss=False)
				row = layout.row()
				row.prop(constraints, "influence", text="", emboss=False)
				if constraints.influence == 0:
					row = row.row()
					row.enabled = False
				disable = row.operator("disable.constraint", text="", icon='CANCEL', emboss=False)
				disable.con = constraints.name
				disable.owner  = owner 
				layout.prop(constraints, "enabled", text="", icon = "HIDE_ON", emboss=False)
				if len(context.selected_objects) > 1:
					copy = layout.operator("constraints_list.copy_to_selected_constraints_list", emboss = False, icon='COPYDOWN', text="")
					copy.name = constraints.name
					copy.owner = owner
				apply = layout.operator("constraints_list.apply_constraints_list", emboss=False, icon='CHECKMARK', text="")
				apply.name = constraints.name
				apply.owner = owner
				delete = layout.operator("constraints_list.delete_constraints_list", emboss=False, icon='X', text="")
				delete.name = constraints.name
				delete.owner = owner

		# 'GRID' layout type should be as compact as possible (typically a single icon!).
		elif self.layout_type == 'GRID':
			layout.alignment = 'CENTER'
			layout.label(text="", icon_value=icon)

class BONE_ConstraintsList(bpy.types.UIList):
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
				duplicate = layout.operator("constraints_list.duplicate_constraints_list", text="", emboss=False, icon = "LAYER_ACTIVE" if index == context.object.bcon_index else "LAYER_USED")
				duplicate.name = constraints.name
				duplicate.owner = owner
				row = layout.row()
				row.alert = is_constraint_disabled(constraints)
				row.label(text="", icon_value=layout.icon(constraints))
				layout.prop(constraints, "name", text="", emboss=False)
				row = layout.row()
				row.prop(constraints, "influence", text="", emboss=False)
				if constraints.influence == 0:
					row = row.row()
					row.enabled = False
				disable = row.operator("disable.constraint", text="", icon='CANCEL', emboss=False)
				disable.con = constraints.name
				disable.owner  = owner
				layout.prop(constraints, "enabled", text="", icon = "HIDE_ON", emboss=False)
				if len(context.selected_pose_bones) > 1:
					copy = layout.operator("constraints_list.copy_to_selected_constraints_list", emboss = False, icon='COPYDOWN', text="")
					copy.name = constraints.name
					copy.owner = owner
				apply = layout.operator("constraints_list.apply_constraints_list", emboss=False, icon='CHECKMARK', text="")
				apply.name = constraints.name
				apply.owner = owner
				delete = layout.operator("constraints_list.delete_constraints_list", emboss=False, icon='X', text="")
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

class ConstraintAddMenu:
	Constraint_TYPES_TO_LABELS = {
		enum_it.identifier: enum_it.name
		for enum_it in bpy.types.Constraint.bl_rna.properties["type"].enum_items_static
	}
	Constraint_TYPES_TO_ICONS = {
		enum_it.identifier: enum_it.icon
		for enum_it in bpy.types.Constraint.bl_rna.properties["type"].enum_items_static
	}
	Constraint_TYPES_I18N_CONTEXT = bpy.types.Constraint.bl_rna.properties["type"].translation_context

	@classmethod
	def operator_constraint_add(cls, layout, con_type):
		if bpy.context.space_data.context == 'CONSTRAINT':
			layout.operator(
				"object.constraint_add",
				text=cls.Constraint_TYPES_TO_LABELS[con_type],
				# Although these are operators, the label actually comes from an (enum) property,
				# so the property's translation context must be used here.
				text_ctxt=cls.Constraint_TYPES_I18N_CONTEXT,
				icon=cls.Constraint_TYPES_TO_ICONS[con_type],
			).type = con_type
		elif bpy.context.space_data.context == 'BONE_CONSTRAINT':
			layout.operator(
				"pose.constraint_add",
				text=cls.Constraint_TYPES_TO_LABELS[con_type],
				# Although these are operators, the label actually comes from an (enum) property,
				# so the property's translation context must be used here.
				text_ctxt=cls.Constraint_TYPES_I18N_CONTEXT,
				icon=cls.Constraint_TYPES_TO_ICONS[con_type],
			).type = con_type

class OBJECT_MT_constraints_add(ConstraintAddMenu, Menu):
	bl_label = "Add Constraints"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		ob_type = context.object.type

		if context.space_data.context == 'CONSTRAINT':
			self.bl_label = "Add Constraints"
		elif context.space_data.context == 'BONE_CONSTRAINT':
			self.bl_label = "Add Bone Constraints"

		if layout.operator_context == 'EXEC_REGION_WIN':
			layout.operator_context = 'INVOKE_REGION_WIN'
			layout.operator("WM_OT_search_single_menu", text="Search...",
							icon='VIEWZOOM').menu_idname = "OBJECT_MT_constraints_add"
			layout.separator()

		layout.operator_context = 'EXEC_REGION_WIN'

		layout.menu("OBJECT_MT_constraint_add_motion_tracking")
		layout.menu("OBJECT_MT_constraint_add_transform")
		layout.menu("OBJECT_MT_constraint_add_tracking")
		layout.menu("OBJECT_MT_constraint_add_relationship")

class OBJECT_MT_constraint_add_motion_tracking(ConstraintAddMenu, Menu):
	bl_label = "Motion Tracking"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_constraint_add(layout, 'CAMERA_SOLVER')
		self.operator_constraint_add(layout, 'FOLLOW_TRACK')
		self.operator_constraint_add(layout, 'OBJECT_SOLVER')

class OBJECT_MT_constraint_add_transform(ConstraintAddMenu, Menu):
	bl_label = "Transform"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_constraint_add(layout, 'COPY_LOCATION')
		self.operator_constraint_add(layout, 'COPY_ROTATION')
		self.operator_constraint_add(layout, 'COPY_SCALE')
		self.operator_constraint_add(layout, 'COPY_TRANSFORMS')

		self.operator_constraint_add(layout, 'LIMIT_DISTANCE')
		self.operator_constraint_add(layout, 'LIMIT_LOCATION')
		self.operator_constraint_add(layout, 'LIMIT_ROTATION')
		self.operator_constraint_add(layout, 'LIMIT_SCALE')

		self.operator_constraint_add(layout, 'MAINTAIN_VOLUME')
		self.operator_constraint_add(layout, 'TRANSFORM_CACHE')
		self.operator_constraint_add(layout, 'TRANSFORM')

class OBJECT_MT_constraint_add_tracking(ConstraintAddMenu, Menu):
	bl_label = "Tracking"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_constraint_add(layout, 'CLAMP_TO')
		self.operator_constraint_add(layout, 'DAMPED_TRACK')
		if context.space_data.context == 'BONE_CONSTRAINT':
			self.operator_constraint_add(layout, 'IK')
		self.operator_constraint_add(layout, 'LOCKED_TRACK')
		if context.space_data.context == 'BONE_CONSTRAINT':
			self.operator_constraint_add(layout, 'SPLINE_IK')
		self.operator_constraint_add(layout, 'STRETCH_TO')
		self.operator_constraint_add(layout, 'TRACK_TO')

class OBJECT_MT_constraint_add_relationship(ConstraintAddMenu, Menu):
	bl_label = "Relationship"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_constraint_add(layout, 'ACTION')
		self.operator_constraint_add(layout, 'ARMATURE')
		self.operator_constraint_add(layout, 'CHILD_OF')
		self.operator_constraint_add(layout, 'FLOOR')
		self.operator_constraint_add(layout, 'FOLLOW_PATH')
		self.operator_constraint_add(layout, 'PIVOT')
		self.operator_constraint_add(layout, 'SHRINKWRAP')

class AddConstraintMenu(Operator):
	bl_idname = "object.add_constraint_menu"
	bl_label = "Add Constraint"

	@classmethod
	def poll(cls, context):
		# NOTE: This operator only exists to add a poll to the add modifier shortcut in the property editor.
		addon_prefs = addonPreferences.getAddonPreferences(bpy.context)
		use_constraint_panel = addon_prefs.use_constraint_panel
		space = context.space_data
		if use_constraint_panel:
			return space and space.type == 'PROPERTIES' and (space.context == 'CONSTRAINT' or space.context == 'BONE_CONSTRAINT')

	def invoke(self, context, event):
		return bpy.ops.wm.call_menu(name="OBJECT_MT_constraints_add")

def drawconstraints(self, context, layout, owner, row, obj):
	addon_prefs = addonPreferences.getAddonPreferences(bpy.context)
	use_old_constraint_menu = addon_prefs.use_old_constraint_menu
	scene = context.scene
	if obj.constraints:
		row.operator("constraints_list.toggle_constraints", emboss = False, icon='HIDE_OFF', text="").owner = owner
		if len(context.selected_objects) > 1:
			row.operator("constraints_list.copy_to_selected_constraints_list_all", emboss = False, icon='COPYDOWN', text="").owner = owner
		row.operator("constraints_list.apply_all_constraints", emboss = False, icon='CHECKMARK', text="").owner = owner
		row.operator("constraints_list.delete_all_constraints", emboss = False, icon='X', text="").owner = owner

	if scene.con_panel == True:
		icon ="FULLSCREEN_ENTER"
	else:
		icon ="FULLSCREEN_EXIT"

	row.prop(scene, "con_panel", emboss = False, icon=icon, text="")

	if use_old_constraint_menu:	
		layout.operator_menu_enum("object.constraint_add", "type", text="Add Object Constraint")
	else:
		layout.operator("wm.call_menu", text="Add Constraints", icon='ADD').name = "OBJECT_MT_constraints_add"
		
	row = layout.row()
	row.template_list("ConstraintsList", "", obj, "constraints", obj, "con_index")

	col = row.column()
	col.operator("constraints_list.constraints_list_first_button", text="", icon='TRIA_UP_BAR').owner = owner
	col.operator("constraints_list.constraints_list_up_button", text="", icon='TRIA_UP').owner = owner
	col.operator("constraints_list.constraints_list_down_button", text="", icon='TRIA_DOWN').owner = owner
	col.operator("constraints_list.constraints_list_last_button", text="", icon='TRIA_DOWN_BAR').owner = owner

	if context.scene.con_panel == True:
		try:
			con_list = []
			for con in obj.constraints:
				con_list.append(con)
			constraints = con_list[obj.con_index]

			# === General settings ===
			box = layout.box()

			row = box.row()

			duplicate = row.operator("constraints_list.duplicate_constraints_list", text="", emboss=False, icon = "LAYER_ACTIVE")
			duplicate.name = constraints.name
			duplicate.owner = owner
			lrow = row.row()
			lrow.alert = is_constraint_disabled(constraints)
			lrow.label(text="", icon_value=layout.icon(constraints))
			row.prop(constraints, "name", text = "")
			row.prop(constraints, "enabled", text="", icon = "HIDE_ON", emboss=False)
			if len(context.selected_objects) > 1:
				copy = row.operator("constraints_list.copy_to_selected_constraints_list", emboss = False, icon='COPYDOWN', text="")
				copy.name = constraints.name
				copy.owner = owner
			apply = row.operator("constraints_list.apply_constraints_list", emboss=False, icon='CHECKMARK', text="")
			apply.name = constraints.name
			apply.owner = owner
			delete = row.operator("constraints_list.delete_constraints_list", emboss=False, icon='X', text="")
			delete.name = constraints.name
			delete.owner = owner

			mp = DATA_constraints(context)
			getattr(mp, constraints.type)(box, obj, constraints, owner)

		except:
			layout.label(text = "No Constraint has selected.")

def draw_boneconstraints(self, context, layout, owner, row, obj):
	addon_prefs = addonPreferences.getAddonPreferences(bpy.context)
	use_old_constraint_menu = addon_prefs.use_old_constraint_menu
	scene = context.scene
	bone = context.active_pose_bone
	if obj.mode == "POSE":
		if context.active_pose_bone.constraints:
			row.operator("constraints_list.toggle_constraints", emboss = False, icon='HIDE_OFF', text="").owner = owner
			if len(context.selected_pose_bones) > 1:
				row.operator("constraints_list.copy_to_selected_constraints_list_all", emboss = False, icon='COPYDOWN', text="").owner = owner
			row.operator("constraints_list.apply_all_constraints", emboss = False, icon='CHECKMARK', text="").owner = owner
			row.operator("constraints_list.delete_all_constraints", emboss = False, icon='X', text="").owner = owner

	if scene.con_panel == True:
		icon ="FULLSCREEN_ENTER"
	else:
		icon ="FULLSCREEN_EXIT"
		
	row.prop(scene, "con_panel", emboss = False, icon=icon, text="")

	if use_old_constraint_menu:
		layout.operator_menu_enum("pose.constraint_add", "type", text="Add Bone Constraint")
	else:
		layout.operator("wm.call_menu", text="Add Bone Constraints", icon='ADD').name = "OBJECT_MT_constraints_add"
	row = layout.row()
	row.template_list("BONE_ConstraintsList", "", bone, "constraints", obj, "bcon_index")

	col = row.column()
	col.operator("constraints_list.constraints_list_first_button", text="", icon='TRIA_UP_BAR').owner = owner
	col.operator("constraints_list.constraints_list_up_button", text="", icon='TRIA_UP').owner = owner
	col.operator("constraints_list.constraints_list_down_button", text="", icon='TRIA_DOWN').owner = owner
	col.operator("constraints_list.constraints_list_last_button", text="", icon='TRIA_DOWN_BAR').owner = owner

	if obj.mode == "POSE":
		if context.scene.con_panel == True:
			try:
				con_list = []
				for con in bone.constraints:
					con_list.append(con)
				constraints = con_list[obj.bcon_index]
				
				# === General settings ===
				box = layout.box()

				row = box.row()

				duplicate = row.operator("constraints_list.duplicate_constraints_list", text="", emboss=False, icon = "LAYER_ACTIVE")
				duplicate.name = constraints.name
				duplicate.owner = owner
				lrow = row.row()
				lrow.alert = is_constraint_disabled(constraints)
				lrow.label(text="", icon_value=layout.icon(constraints))
				row.prop(constraints, "name", text = "")
				row.prop(constraints, "enabled", text="", icon = "HIDE_ON", emboss=False)
				if len(context.selected_pose_bones) > 1:
					copy = row.operator("constraints_list.copy_to_selected_constraints_list", emboss = False, icon='COPYDOWN', text="")
					copy.name = constraints.name
					copy.owner = owner
				apply = row.operator("constraints_list.apply_constraints_list", emboss=False, icon='CHECKMARK', text="")
				apply.name = constraints.name
				apply.owner = owner
				delete = row.operator("constraints_list.delete_constraints_list", emboss=False, icon='X', text="")
				delete.name = constraints.name
				delete.owner = owner

				mp = DATA_constraints(context)
				getattr(mp, constraints.type)(box, obj, constraints, owner)

			except:
				layout.label(text = "No Constraint has selected.")

	else:
		layout.label(text = "Interaction mode is not Pose Mode.")
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

classes = (
	Disable_constraint,
	Constraints_OT_List_Up,
	Constraints_OT_List_Down,
	Constraints_OT_List_First,
	Constraints_OT_List_Last,
	Constraints_OT_List_Up_Button,
	Constraints_OT_List_Down_Button,
	Constraints_OT_List_First_Button,
	Constraints_OT_List_Last_Button,
	Constraints_OT_ToggleConstraints,
	Constraints_OT_ApplyAllConstraints,
	Constraints_OT_DeleteAllConstraints,
	Constraints_OT_CopyToSelected_ListConstraintsAll,
	Constraints_OT_CopyToSelected_ListConstraints,
	Constraints_OT_Delete_Constraints_List,
	Constraints_OT_Apply_Constraints_List,
	Constraints_OT_Duplicate_Constraints_List,
	Constraints_OT_Delete_Constraints,
	Constraints_OT_Apply_Constraints,
	Constraints_OT_Duplicate_Constraints,
	Constraints_OT_Toggle_Constraints_View,
	Constraints_OT_Solo_Constraints_View,
	Constraints_OT_Show_Constraints_View,
	ConstraintsList,
	BONE_ConstraintsList,
	OBJECT_MT_constraints_add,
	OBJECT_MT_constraint_add_motion_tracking,
	OBJECT_MT_constraint_add_transform,
	OBJECT_MT_constraint_add_tracking,
	OBJECT_MT_constraint_add_relationship,
		  ) 

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

	bpy.types.Scene.con_panel = bpy.props.BoolProperty(
		name="Expand Constraints Settings",
		description="Expand Constraint Settings Panel",
	)

	bpy.types.Object.con_index = IntProperty(
		options={'HIDDEN'},
		name="Constraints List Index",
		description="Constraints List Index",
	)

	bpy.types.Object.bcon_index = IntProperty(
		options={'HIDDEN'},
		name="Bone Constraints List Index",
		description="Bone Constraints List Index",
	)

	bpy.types.OBJECT_PT_constraints.prepend(KEN_MT_con_menu_main)
	bpy.types.BONE_PT_constraints.prepend(KEN_MT_bcon_menu_main)

	addon_prefs = addonPreferences.getAddonPreferences(bpy.context)
	use_constraint_panel = addon_prefs.use_constraint_panel
	if use_constraint_panel:
		from bpy.utils import register_class

		try:
			register_class(AddConstraintMenu)
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

	del bpy.types.Object.con_index
	del bpy.types.Object.bcon_index

	try:
		unregister_class(AddConstraintMenu)
		unregister_class(OBJECT_PT_constraints)
		unregister_class(BONE_PT_constraints)
		register_class(original_OBJECT_PT_constraints)
		register_class(original_BONE_PT_constraints)
	except RuntimeError:
		pass