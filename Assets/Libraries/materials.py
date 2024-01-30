import bpy
from .. import assetsDefs

class Materials_List_Remove(bpy.types.Operator):
	bl_idname = "materials.remove_list"
	bl_label = "Remove Material List"
	bl_options = {'REGISTER', 'UNDO'}

	mat: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		mat = bpy.data.materials[self.mat]
		bpy.data.materials.remove(mat)
		context.scene.mat_index = context.scene.mat_index - 1
		self.report({"INFO"}, "Material in list removed.")
		return {"FINISHED"}

class Materials_Replace(bpy.types.Operator):
	bl_idname = "materials.replace"
	bl_label = "Replace Material"
	bl_options = {'REGISTER', 'UNDO'}

	mat: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		mat_data = bpy.data.materials[self.mat]
		for obj in context.selected_objects:
			try:
				if obj.data.materials:
					# assign to 1st material slot
					slot = context.object.active_material_index
					obj.data.materials[slot] = mat_data
				else:
					# no slots
					obj.data.materials.append(mat_data)
			except:
				continue
		self.report({"INFO"}, "Replace " + mat_data.name + " Material")
		return {"FINISHED"}

class Materials_Append(bpy.types.Operator):
	bl_idname = "materials.append"
	bl_label = "Append Material"
	bl_options = {'REGISTER', 'UNDO'}

	mat: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		mat_data = bpy.data.materials[self.mat]
		for obj in context.selected_objects:
			try:
				context.view_layer.objects.active = obj
				if obj.material_slots and obj.data.materials[obj.active_material_index] is None:
					obj.data.materials[obj.active_material_index] = mat_data
				else:
					obj.data.materials.append(mat_data)
					obj.active_material_index = len(obj.data.materials) - 1
			except:
				continue
		self.report({"INFO"}, "Append " + mat_data.name + " Material.")
		return {"FINISHED"}
	
class Materials_Duplicate(bpy.types.Operator):
	bl_idname = "materials.duplicate"
	bl_label = "Material Duplicate"
	bl_options = {'REGISTER', 'UNDO'}

	mat: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		obj = context.object
		mat_data = bpy.data.materials[self.mat]
		new_mat = mat_data.copy()

		context.object.data.materials.append(new_mat)
		obj.active_material_index = len(obj.data.materials) - 1
		context.scene.mat_index = len(bpy.data.materials) - 1
		self.report({"INFO"}, mat_data.name + " Material has been Duplicated.")
		return {"FINISHED"}
	
class Materials_Single(bpy.types.Operator):
	bl_idname = "materials.single"
	bl_label = "Material Make Single"
	bl_options = {'REGISTER', 'UNDO'}

	mat: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		mat_data = bpy.data.materials[self.mat]
		slot = context.object.active_material_index
		new_mat = mat_data.copy()
		context.object.data.materials[slot] = new_mat

		self.report({"INFO"}, mat_data.name + " Material Make Single.")
		return {"FINISHED"}
	
class Materials_Clear(bpy.types.Operator):
	bl_idname = "materials.clear"
	bl_label = "Clear Object Materials"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		selected_objects = context.selected_objects
		for obj in selected_objects:
			# Remove all material slots from the object
			for i in reversed(range(len(obj.material_slots))):
				bpy.ops.object.material_slot_remove()

		self.report({"INFO"}, "Object Materials have been cleared.")
		return {"FINISHED"}

class MATERIALS(bpy.types.UIList):
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
		ma = item.material
		# draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			# You should always start your row layout by a label (icon + text), or a non-embossed text field,
			# this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
			# We use icon_value of label, as our given icon is an integer value, not an enum ID.
			# Note "data" names should never be translated!
			if ma:
				layout.prop(ma, "name", text="", emboss=False, icon_value=icon)
			else:
				layout.label(text="", translate=False, icon_value=icon)
		# 'GRID' layout type should be as compact as possible (typically a single icon!).
		elif self.layout_type == 'GRID':
			layout.alignment = 'CENTER'
			layout.label(text="", icon_value=icon)

class SCENEMATERIALS(bpy.types.UIList):
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
		ma = item
		# draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			# You should always start your row layout by a label (icon + text), or a non-embossed text field,
			# this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
			# We use icon_value of label, as our given icon is an integer value, not an enum ID.
			# Note "data" names should never be translated!
			if ma:
				layout.prop(ma, "name", text="", emboss=False, icon_value=icon)
				row = layout.row()
				row.scale_x = 0.2
				row.label(text = str(ma.users))
				layout.operator("materials.select", icon = "RESTRICT_SELECT_OFF", emboss = False ,text = "").mat = ma.name
				layout.prop(ma,"use_fake_user", text = "", emboss=False)
				if ma.use_fake_user == False:
					layout.operator("materials.remove_list", text = "", icon = "X", emboss=False).mat = ma.name
		# 'GRID' layout type should be as compact as possible (typically a single icon!).
		elif self.layout_type == 'GRID':
			layout.alignment = 'CENTER'
			layout.label(text="", icon_value=icon)

	def filter_items(self,context,data,propname):
		filtered = []
		ordered = []
		items = getattr(data, propname)
		helper_funcs = bpy.types.UI_UL_list

		filtered = [self.bitflag_filter_item] * len(items)

		ordered = helper_funcs.sort_items_by_name(items, "name")

		filtered_items = [o for o in bpy.data.materials if o.name !='Dots Stroke']

		for i, item in enumerate(items):
			if not item in filtered_items:
				filtered[i] &= ~self.bitflag_filter_item
				
		return filtered,ordered

def draw_materials(self, context, box):
	obj = context.object
	scene = context.scene
	row = box.row()
	row.scale_x = 1.75
	matnum = len(bpy.data.materials)-1
	row.label(text = "Materials Library: Total "+str(matnum), icon = "MATERIAL")
	if obj and obj.type == "MESH" and obj.mode == "OBJECT":
		row.operator("object.material_slot_remove", text = "", icon = "REMOVE", emboss=False)
		row.operator("object.material_slot_add", text = "", icon = "ADD", emboss=False)

	if scene.mat_fake_use == True:
		icon = "FAKE_USER_ON"
	else:
		icon = "FAKE_USER_OFF"
	row.prop(scene, "mat_fake_use", text = "", icon = icon, emboss = False)
	row.scale_x = 0.75
	row.operator("materials.clean_resources", icon = "BRUSH_DATA", text = "Clean")

	if obj and obj.type == "MESH" and obj.active_material:
		if scene.scene_mat == False:
			state = "Object Material"
			mat = obj.active_material
			row = box.row()
			row.prop(scene, "scene_mat", icon = "SCENE_DATA", text = "")
		else:
			state = "Scene Material"
			mat = bpy.data.materials[scene.mat_index]
			row = box.row()
			row.prop(scene, "scene_mat", icon = "SCENE_DATA", text = "")
	else:
		state = "Scene Material"
		mat = bpy.data.materials[scene.mat_index]
		row = box.row()

	row.label(text = state)
	if obj and obj.type == "MESH":
		if scene.scene_mat == False:
			row.operator("materials.clear", text = "Clear Material")
		row = box.row(align = True)
		row.template_list("MATERIALS", "", obj, "material_slots", obj, "active_material_index")
	else:
		row = box.row()
	row.template_list("SCENEMATERIALS", "", bpy.data, "materials", scene, "mat_index")

	if obj and obj.type == "MESH":
		addmat = bpy.data.materials[scene.mat_index]
		if addmat and addmat.name != 'Dots Stroke':
			row = box.row()
			row.operator("materials.append", text = "Append").mat = addmat.name
			row.operator("materials.replace", text = "Replace").mat = addmat.name

	if mat and mat.name != 'Dots Stroke':
		
		box.label(text = "Prep Tools", icon = "TOOL_SETTINGS")
		if state == "Object Material":
			objmat = box.operator("prep.material", text = "Prep Materials")
			objmat.type = "obj"
		else:
			row = box.row()
			indexmat = row.operator("prep.material", text = "Prep Scene Material")
			indexmat.type = "index"
			indexmat.mat = mat.name
			allmat = row.operator("prep.material", text = "Prep All Materials")
			allmat.type = "scene"
			   
		row = box.row()
		row.label(icon_value=row.icon(mat))
		row.prop(mat, "name", text = "")
		row.scale_x = 1
		row.operator("materials.select", icon = "RESTRICT_SELECT_OFF", emboss = False ,text = "").mat = mat.name
		row.prop(mat,"use_fake_user", text = "", emboss=False)

		if obj and obj.type == "MESH" and obj.active_material:
			if obj.mode == "OBJECT":
				row.scale_x = 0.1
				row.operator("materials.single", text = str(mat.users)).mat = mat.name

				row.scale_x = 1
				row.operator("materials.duplicate", text = "", icon = "DUPLICATE", emboss=False).mat = mat.name

				row.operator("object.material_slot_remove", text = "", icon = "X", emboss=False)
			elif obj.mode == "EDIT":
				row = box.row(align=True)
				row.operator("object.material_slot_assign", text="Assign")
				row.operator("object.material_slot_select", text="Select")
				row.operator("object.material_slot_deselect", text="Deselect")

		drawnode_tree(scene, box, mat)

	else:
		if obj and obj.type == "MESH":
			if not obj.data.materials:
				box.label(text = "Object has no Material")
				box.operator("new.material", text = "New Material", icon = "MATERIAL")
			if obj.material_slots and obj.data.materials[obj.active_material_index] is None:
				box.label(text = "Material slot has no Material")
				box.operator("new.material", text = "New Material", icon = "MATERIAL")
		else:
			box.label(text = "Scene has no Material")
			box.operator("new.material", text = "New Material", icon = "MATERIAL")

def draw_material_properties(self, context, obj):
	scene = context.scene
	layout = self.layout
	box = layout.box()
	row = box.row()
	row.label(text = "Quick Material", icon = "MATERIAL")
	box.template_list("MATERIALS", "", obj, "material_slots", obj, "active_material_index")
	if obj.data.materials:
		mat = obj.active_material
		row.label(icon_value=layout.icon(mat))
		row.prop(mat, "name", text ="")
		row.scale_x = 1
		if obj.mode == "OBJECT":
			row.scale_x = 0.2
			row.operator("materials.single", text = str(mat.users)).mat = mat.name
			row.scale_x = 1
			row.operator("materials.duplicate", text = "", icon = "DUPLICATE", emboss=False).mat = mat.name

		if obj.mode == "EDIT":
			row = box.row()
			row.operator("object.material_slot_assign", text = "Assign")
			row.operator("object.material_slot_select", text = "Select")

		drawnode_tree(scene, box, mat)

	if not obj.data.materials or not obj.active_material:
		box.label(text = "No Available Object")
		box.operator("new.material", text = "New Material", icon = "MATERIAL")

def drawnode_tree(scene, box, mat):
	if mat.node_tree.nodes:
		ntree = mat.node_tree
		id = len(ntree.nodes)
		node = ntree.get_output_node('EEVEE')
		input = find_node_input(node, "Surface")
		if scene.mat_surface == True:
			icon = "DOWNARROW_HLT"
		else:
			icon = "RIGHTARROW"
		box.prop(scene, "mat_surface", text = "Materials Surface", icon = icon, emboss=False)
		if scene.mat_surface == True:
			node_view = box.box()
			node_view.operator("add.image", text = "Add Image Texture", icon = "IMAGE_DATA").mat = mat.name
			node_view.template_node_view(ntree, node, input)
		for node in mat.node_tree.nodes:
			if node.name == 'Animated_Texture':
				box.label(text = node.name)
				nodebox = box.box()
				if not node.inputs[input].links:
					box.prop(node.inputs[0], "default_value", text = "Frame Number")
					row = nodebox.row()
					nodebox.prop(node.inputs[2], "default_value", text = "Frame Muiltply")

			drawnoderamp(node, box, 'ColorRamp_Specular', "Specular Color Ramp")
			drawnoderamp(node, box, 'ColorRamp_Roughness', "Roughness Color Ramp")
			drawnoderamp(node, box, 'ColorRamp_Bump', "Bump Color Ramp")
			if node.name.split(".")[0] == 'Combine Normal Map':
				if all(len(outputs_socket.links) > 0 for outputs_socket in node.outputs):
					box.label(text = node.name)
					nodebox = box.box()
					nodebox.prop(node.inputs[3], "default_value", text = "Bump Strength")
					nodebox.prop(node.inputs[1], "default_value", text = "Nomral Strength")

			if node.name.split(".")[0] == 'Bump Map':
				if all(len(outputs_socket.links) > 0 for outputs_socket in node.outputs):
					box.label(text = node.name)
					nodebox = box.box()
					nodebox.prop(node.inputs[0], "default_value", text = "Bump Strength")
					nodebox.prop(node.inputs[1], "default_value", text = "Distance")

			if node.name.split(".")[0] == 'Normal Map':
				if all(len(outputs_socket.links) > 0 for outputs_socket in node.outputs):
					box.label(text = node.name)
					nodebox = box.box()
					nodebox.prop(node.inputs[0], "default_value", text = "Normal Strength")

			drawnodelist(box, node, id, "Glass_Dispersion")
			drawnodelist(box, node, id, "Emission Object")
			drawnodelist(box, node, id, "Illumination Object")

		box.label(text = "Material Settings")
		box.prop(mat, "blend_method")
		box.prop(mat, "shadow_method")
		row = box.row()
		row.prop(mat, "show_transparent_back", toggle = True)
		row.prop(mat, "use_screen_refraction", toggle = True)
			
	elif mat.grease_pencil:
		gpcolor = mat.grease_pencil
		box.prop(gpcolor, "show_stroke", text="Stroke")
		if gpcolor.show_stroke == True:
			strokebox = box.box()
			strokebox.prop(gpcolor, "mode")

			strokebox.prop(gpcolor, "stroke_style", text="Style")

			strokebox.prop(gpcolor, "color", text="Base Color")
			strokebox.prop(gpcolor, "use_stroke_holdout")

			if gpcolor.stroke_style == 'TEXTURE':
				row = strokebox.row()
				row.enabled = not gpcolor.lock
				strokebox = row.column(align=True)
				strokebox.template_ID(gpcolor, "stroke_image", open="image.open")

			if gpcolor.stroke_style == 'TEXTURE':
				row = strokebox.row()
				row.prop(gpcolor, "mix_stroke_factor", text="Blend", slider=True)
				if gpcolor.mode == 'LINE':
					strokebox.prop(gpcolor, "pixel_size", text="UV Factor")

			if gpcolor.mode in {'DOTS', 'BOX'}:
				strokebox.prop(gpcolor, "alignment_mode")
				strokebox.prop(gpcolor, "alignment_rotation")

			if gpcolor.mode == 'LINE':
				strokebox.prop(gpcolor, "use_overlap_strokes")

		box.prop(gpcolor, "show_fill", text="Fill")
		if gpcolor.show_fill == True:
			fillbox = box.box()
			fillbox.prop(gpcolor, "fill_style", text="Style")

			if gpcolor.fill_style == 'SOLID':
				fillbox.prop(gpcolor, "fill_color", text="Base Color")
				fillbox.prop(gpcolor, "use_fill_holdout")

			elif gpcolor.fill_style == 'GRADIENT':
				fillbox.prop(gpcolor, "gradient_type")

				fillbox.prop(gpcolor, "fill_color", text="Base Color")
				fillbox.prop(gpcolor, "mix_color", text="Secondary Color")
				fillbox.prop(gpcolor, "use_fill_holdout")
				fillbox.prop(gpcolor, "mix_factor", text="Blend", slider=True)
				fillbox.prop(gpcolor, "flip", text="Flip Colors")

				fillbox.prop(gpcolor, "texture_offset", text="Location")

				row = fillbox.row()
				row.enabled = gpcolor.gradient_type == 'LINEAR'
				row.prop(gpcolor, "texture_angle", text="Rotation")

				fillbox.prop(gpcolor, "texture_scale", text="Scale")

			elif gpcolor.fill_style == 'TEXTURE':
				fillbox.prop(gpcolor, "fill_color", text="Base Color")
				fillbox.prop(gpcolor, "use_fill_holdout")

				fillbox.template_ID(gpcolor, "fill_image", open="image.open")

				fillbox.prop(gpcolor, "mix_factor", text="Blend", slider=True)

				fillbox.prop(gpcolor, "texture_offset", text="Location")
				fillbox.prop(gpcolor, "texture_angle", text="Rotation")
				fillbox.prop(gpcolor, "texture_scale", text="Scale")
				fillbox.prop(gpcolor, "texture_clamp", text="Clip Image")

		box.label(text = "Settings")
		box.prop(gpcolor, "pass_index")

def drawnoderamp(node, box, name, text):
	if node.name.split(".")[0] == name:
		box.label(text = text)
		nodebox = box.box()
		nodebox.template_color_ramp(node, "color_ramp", expand=True)

def drawnodelist(box, node, id, name):
	if node.name.split(".")[0] == name:
		if all(len(input_socket.links) > 0 for input_socket in node.inputs):
			return
		elif all(len(outputs_socket.links) > 0 for outputs_socket in node.outputs):
			box.label(text = node.name)
			nodebox = box.box()
			inputs = len(node.inputs)
			for input in range(inputs):
				if not node.inputs[input].links:
					nodebox.prop(node.inputs[input], "default_value", text = node.inputs[input].name)

def find_node_input(node, input_name):
	for input in node.inputs:
		if input.name == input_name:
			return input
	return None

bpy.types.Scene.mat_surface = bpy.props.BoolProperty(
	name="Toggle Materials Surface",
	description="Toggle Materials Surface",
)
bpy.types.Scene.mat_fake_use = bpy.props.BoolProperty(
	name="Toggle Materials Fake_User",
	description="Toggle Materials Fake_User",
	update = assetsDefs.update_mat_fake_use
)
bpy.types.Scene.mat = bpy.props.BoolProperty(
	name="Material",
	description="Material",
	default=False,
)
bpy.types.Scene.mat_index = bpy.props.IntProperty(
	name="mat_index",
	description="mat_index",
)

bpy.types.Scene.scene_mat = bpy.props.BoolProperty(
	name="Switch Materials",
	description="Switch Scene Material",
)

classes = (
			Materials_List_Remove,
			Materials_Replace,
			Materials_Append,
			Materials_Duplicate,
			Materials_Single,
			Materials_Clear,
			MATERIALS,
			SCENEMATERIALS,
		  )

def register(): 
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
  
def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)