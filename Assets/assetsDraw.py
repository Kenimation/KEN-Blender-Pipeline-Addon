import bpy
import bmesh

import os
from . import assetsDefs, assetsProperties
from .Anime import AnimeProperties
from .Libraries import materials, lights, cameras, particles
from .. import addonPreferences
from ..UI import modifiers_panel, constraints_panel

def drawheader(context, addon_prefs, row, obj):
	scene = context.scene
	if scene.myProps == 'one':
		if addon_prefs.view == True:
			row.prop(scene, "view", icon = "VIEW3D", text = "")
		if addon_prefs.advanced_option == True:
			if obj and obj.type == 'MESH' and scene.advanced_option == True:
				row.prop(scene, "simulation", icon = "PHYSICS", text = "")
				row.prop(scene, "particles_properties", icon = "PARTICLES", text = "")
			row.prop(scene, "advanced_option", icon = "OUTLINER", text = "")
		if addon_prefs.tools == True:
			row.prop(scene, "tools", icon = "TOOL_SETTINGS", text = "")

	if scene.myProps == 'two':
		if scene.libraries == 'three':
			row.prop(scene, "camera", text = "Local Camera")
		if scene.libraries == 'one' or scene.libraries == 'four':
			row.scale_x = 0.25
			row.operator("outliner.orphans_purge", text = "Purge").do_recursive=True
			row.scale_x = 1

def draw_tools(addon_prefs, self, scene, obj):
	layout = self.layout
	box = layout.box()
	row = box.row()
	row.label(text = "Tools", icon = "TOOL_SETTINGS")
	row.prop(scene, "Object_Type", text = "")
	row.operator("object.select_by_type", text = "", icon = "RESTRICT_SELECT_OFF", emboss=False).type = scene.Object_Type
	if any(item.registered_name == AnimeProperties.registered_name[1] for item in addon_prefs.registered_name) or any(item.registered_name == AnimeProperties.registered_name[2] for item in addon_prefs.registered_name):
		if scene.QuickImport == True:
			icon = "DOWNARROW_HLT"
		else:
			icon = "RIGHTARROW"
		box.prop(scene, "QuickImport", text = "Quick Import", icon = icon, emboss=False)
		if scene.QuickImport == True:
			QuickImport = box.box()
			QuickImport.label(text = "Object Import")
			QuickImport.operator("import.mc_world", text = "Minecraft World Import")
			row = QuickImport.row()
			col = row.column_flow(columns = 2)
			col.operator("import.minecraftmodel", text = "Minecraft Obj")
			col.operator("import.minecraftjson", text = "Minecraft Json")
			QuickImport.label(text = "Image Import")
			row = QuickImport.row()
			row.operator("import.alpha_image", text = "Alpha Plane")
			row.operator("import.3d_item", text = "3D Item from file")

	if obj:
		if obj.type == 'MESH':
			if scene.EditingTools == True:
				icon = "DOWNARROW_HLT"
			else:
				icon = "RIGHTARROW"
			box.prop(scene, "EditingTools", text = "Editing Tools", icon = icon, emboss=False)
			if scene.EditingTools == True:
				EditingTools = box.box()
				EditingTools.label(text = "Editing Tools")
				row = EditingTools.row()
				row.operator("select.alphauv", text = "Alpha Editing")
				row.operator("scale.uv", text = "Scale Faces")

			if scene.VertexGroupTool == True:
				icon = "DOWNARROW_HLT"
			else:
				icon = "RIGHTARROW"
			box.prop(scene, "VertexGroupTool", text = "Vertex Group Tool", icon = icon, emboss=False)
			if scene.VertexGroupTool == True:
				VertexGroupTool = box.box()
				VertexGroupTool.label(text = "Add Vertex Group")
				VertexGroupTool.prop(scene, "VertexGroupMenu", expand = True)
				row = VertexGroupTool.row()  
				if scene.VertexGroupMenu == 'one':
					row.prop(scene, "VertexGroupName", text = "")
				else:
					row = VertexGroupTool.row()
					row.prop(scene, "VertexGroupPart", text = "")
					row.prop(scene, "VertexGroupLR", expand = True)
					
				row = VertexGroupTool.row()
				row.prop(scene, "FixName", text = "")
				row.prop(scene, "FixNameType", expand = True)
				VertexGroupTool.operator("add.vertex_group", text = "Add")

				VertexGroupTool.label(text = "Add Vertex Group Loop")
				row = VertexGroupTool.row()
				row.prop(scene, "VertexGroupName", text = "Name")
				row.prop(scene, "VertexGroupCount", text = "")
				row.prop(scene, "VertexGroupMiiror", text = "", icon = "ARROW_LEFTRIGHT")
				VertexGroupTool.operator("add.vertex_group_loop", text = "Add Vertex Group Loop")

		if obj.type == 'ARMATURE':
			if obj.mode == 'POSE':
				if scene.BoneTool == True:
					icon = "DOWNARROW_HLT"
				else:
					icon = "RIGHTARROW"
				box.prop(scene, "BoneTool", text = "Bone Tool", icon = icon, emboss=False)
				if scene.BoneTool == True:
					BoneTool = box.box()
					BoneTool.label(text = "Constraints Driver")
					row = BoneTool.row()
					row.prop(scene, "Constraints_Type", text = "")
					row.prop(scene, "Rig_Prop", text = "")
					row = BoneTool.row()
					row.operator("add.constraintsdriver", text = "Add")
					row.operator("remove.constraintsdriver", text = "Remove")
					BoneTool.label(text = "Damped Track Child")
					row = BoneTool.row()
					row.operator("add.dampedtrackchild", text = "Track Child")
					row.prop(scene, "Damped_Track_Influence", slider = True)
					row = BoneTool.row()
					row.operator("add.copyrotationparent", text = "Copy Parent Rotation")
					row.prop(scene, "Copy_Rotation_Influence", slider = True)
					BoneTool.label(text = "Damped Track Loop")
					row = BoneTool.row()
					row.prop(scene, "Track_Prefix", text = "")
					row.operator("add.dampedtrackloop", text = "Add")

def draw_edit(scene, box):
	if scene.object_properties == False:
		box.label(text = "Copy Transforms")
		box.operator("copy.trans", text = "All Transform")
		row = box.row(align = True)
		row.operator("copy.loc", text = "Location")
		row.operator("copy.rota", text = "Rotation")
		row.operator("copy.size", text = "Scale")

def draw_transform(addon_prefs, context, box, obj):
	row = box.row()
	if obj.type == 'ARMATURE':
		if obj.mode == 'POSE':
			actobj = context.active_pose_bone
			row.label(text = "Pose Transforms", icon = "BONE_DATA")
			if actobj:
				row.prop(actobj, "name", text = "")
			row.prop(context.object.pose, "use_auto_ik", icon = "CON_KINEMATIC", text = "")
			row.prop(context.object.pose, "use_mirror_x", icon = "MOD_MIRROR", text = "")
		else:
			actobj = context.active_object
			row.label(text = "Object Transforms", icon = "OBJECT_DATAMODE")
	elif obj.type != 'ARMATURE':
		actobj = context.active_object
		row.label(text = "Object Transforms", icon = "OBJECT_DATAMODE")

	if actobj:
		row = box.row()
		if addon_prefs.compact_panel == False:
			row.label(text = "Location")
			row = box.row()
		row.prop(actobj, "location", text = "")
		row = box.row()
		if addon_prefs.compact_panel == False:
			row.label(text = "Rotation")
		row.prop(actobj, "rotation_mode", text = "")
		row = box.row()
		if actobj.rotation_mode == 'QUATERNION':
			row.prop(actobj, "rotation_quaternion", text = "")
		else:
			row.prop(actobj, "rotation_euler", text = "")
		row = box.row()
		if addon_prefs.compact_panel== False:
			row.label(text = "Scale")
			row = box.row()
		row.prop(actobj, "scale", text = "")
		if obj.type == "MESH" or obj.type == "ARMATURE" and obj.mode == "OBJECT":
			row = box.row()
			if addon_prefs.compact_panel== False:
				row.label(text = "Dimensions")
				row = box.row()
			row.prop(actobj, "dimensions", text = "")

def drawedit_transform(addon_prefs, context, box, obj):
	sel_mode = context.tool_settings.mesh_select_mode[:]
	if sel_mode[0]:
		edit_icon = 'VERTEXSEL'
	elif sel_mode[1]:
		edit_icon ='EDGESEL'
	elif sel_mode[2]:
		edit_icon ='FACESEL'
	
	if obj.type == 'MESH':
		box.label(text = "Edit Transforms", icon = edit_icon)

		if addon_prefs.compact_panel == False:
			box.label(text = "Location")
		row = box.row()
		row.prop(obj, "location", text = "")

	elif obj.type == 'ARMATURE':
		actobj = context.active_bone
		row = box.row()
		row.label(text = "Bone Transforms", icon = "BONE_DATA")
		row.prop(actobj, "name", text = "")
		row.prop(context.object.pose, "use_mirror_x", icon = "MOD_MIRROR", text = "")
		if addon_prefs.compact_panel== False:
			box.label(text = "Head")
		row = box.row()
		row.prop(actobj, "head", text = "")
		if addon_prefs.compact_panel== False:
			box.label(text = "Tail")
		row = box.row()
		row.prop(actobj, "tail", text = "")
		box.prop(actobj, "roll", text = "Roll")
		box.prop(actobj, "tail_radius", text = "Radius")
		box.prop(actobj, "length", text = "Length")
		box.prop(actobj, "envelope_distance", text = "Envelope")

def draw_properties(addon_prefs, context, row, obj, pcoll):
	scene = context.scene
	if obj.type == 'ARMATURE':
		row.label(text = "", icon = "OUTLINER_OB_ARMATURE")
		row.prop(obj, "name", text = "Name")

		if any(item.registered_name in AnimeProperties.registered_name for item in addon_prefs.registered_name):
			if obj.mode != 'EDIT' and context.active_object.RIG_ID in AnimeProperties.kenriglist:
				if context.active_object.RIG_ID == AnimeProperties.kenriglist[2]:
					ken_icon = pcoll["Dual"]
					ken_icon02 = pcoll["Dual_02"]
					if obj.ken_anime_rig == True:
						rig_icon = ken_icon02
					else:
						rig_icon = ken_icon
					row.prop(obj, "ken_anime_rig", icon_value = rig_icon.icon_id, text = "", emboss=False)
				else:
					ken_icon = pcoll["Minecraft"]
					ken_icon02 = pcoll["Minecraft_02"]
					if obj.ken_mc_rig == True:
						rig_icon = ken_icon02
					else:
						rig_icon = ken_icon
					row.prop(obj, "ken_mc_rig", icon_value = rig_icon.icon_id, text = "", emboss=False)
		else:
			row.prop(scene, "object_properties", icon = "ARMATURE_DATA", text = "")
			
	else:
		if obj.type == 'MESH':
			objicon = "OUTLINER_OB_MESH"
		elif obj.type == 'LIGHT':
			objicon = "OUTLINER_OB_LIGHT"
		elif obj.type == 'CAMERA':
			objicon = "OUTLINER_OB_CAMERA"
		elif obj.type == 'EMPTY':
			objicon = "OUTLINER_OB_EMPTY"
		elif obj.type == 'CURVE':
			objicon = "OUTLINER_OB_CURVE"
		else:
			objicon = "OUTLINER_OB_MESH"
		row.label(icon = objicon)
		row.prop(obj, "name", text = "Name")
		if obj.type == 'MESH':
			row.prop(scene, "object_properties", icon = "OBJECT_DATAMODE", text = "")
			row.prop(scene, "mat", icon = "MATERIAL", text = "")

def drawbone_properties(box, context, obj):
	actobj = context.active_bone
	actpos = context.active_pose_bone
	box.prop(obj.data, "display_type", text = "Display As")
	box.prop(obj, "show_in_front", text = "In Front")
	box.prop(obj.data, "show_names", text = "Show Names")
	row = box.row()
	row.prop(obj.data, "show_axes", text = "Axes")
	row.prop(obj.data, "axes_position", text = "Position")
	box.prop(obj.data, "relation_line_position", text = "Relations", expand = True)
	box.label(text = "Bone Properties")
	if obj.mode == "EDIT":
		box.prop(actobj, "parent", text = "Parent")
		box.prop(actobj, "use_connect", text = "Connected")

	box.prop(actobj, "use_deform", text = "Deform")
	row = box.row()
	row.prop(actobj.color, "palette", text = "Bone Color")
	row.operator("armature.copy_bone_color_to_selected", text = "", icon = "UV_SYNC_SELECT").bone_type='EDIT'

	if obj.mode == "POSE":
		row = box.row()
		row.prop(actpos.color, "palette", text = "Pose Bone Color")
		row.operator("armature.copy_bone_color_to_selected", text = "", icon = "UV_SYNC_SELECT").bone_type='POSE'
		box.prop(actobj, "hide", toggle = False, icon = 'BLANK1')
		box.prop(actpos, "custom_shape", text = "Custom Shape")
		if actpos.custom_shape:
			box.prop(actpos, "custom_shape_translation", text = "")
			box.prop(actpos, "custom_shape_rotation_euler", text = "")
			box.prop(actpos, "custom_shape_scale_xyz", text = "")
			box.prop(actpos, "use_custom_shape_bone_size", text = "Scale to Bone Length")
			box.prop(actobj, "show_wire", text = "Wireframe")

	if obj.BonesCollection == True:
		icon = "DOWNARROW_HLT"
	else:
		icon = "RIGHTARROW"
	box.prop(obj, "BonesCollection", emboss=False , icon = icon)

	if obj.BonesCollection == True:

		row = box.row()

		rows = 1

		row.template_list(
			"DATA_UL_bone_collections",
			"collections",
			obj.data,
			"collections",
			obj.data.collections,
			"active_index",
			rows=rows,
		)

		col = row.column(align=True)
		col.operator("armature.collection_add", icon='ADD', text="")
		col.operator("armature.collection_remove", icon='REMOVE', text="")
		col.separator()
		col.operator("armature.collection_move", icon='TRIA_UP', text="").direction = 'UP'
		col.operator("armature.collection_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
		col.separator()

		col.menu("ARMATURE_MT_collection_context_menu", icon='DOWNARROW_HLT', text="")

		row = box.row()

		sub = row.row(align=True)
		sub.operator("armature.collection_assign", text="Assign")
		sub.operator("armature.collection_unassign", text="Remove")

		sub = row.row(align=True)
		sub.operator("armature.collection_select", text="Select")
		sub.operator("armature.collection_deselect", text="Deselect")

def drawmesh_properties(box, context, obj):
	scene = context.scene
	box.prop(obj, "parent", text = "Parent")
	box.prop(obj, "color", text = "Color")
	box.prop(obj, "display_type", text = "Display As")
	box.prop(obj, "show_bounds", text = "Bounds")
	row = box.row()
	row.prop(obj, "show_in_front", text = "In Front")
	if obj.show_bounds == True or obj.display_type == 'BOUNDS':
		row.prop(obj, "display_bounds_type", text = "")
	if obj.type == 'MESH' and scene.render.engine in ["CYCLES"]:
		if scene.ray_visility == True:
			icon = "DOWNARROW_HLT"
		else:
			icon = "RIGHTARROW"
		box.prop(scene, "ray_visility", text = "Ray Visility", icon = icon, emboss=False) 
		if context.scene.ray_visility == True:
			raybox = box.box()
			raybox.prop(obj, "visible_camera", toggle = True, text = "Camera")
			raybox.prop(obj, "visible_diffuse", toggle = True, text = "Diffuse")
			raybox.prop(obj, "visible_glossy", toggle = True, text = "Glossy")
			raybox.prop(obj, "visible_transmission", toggle = True, text = "Transmission")
			raybox.prop(obj, "visible_volume_scatter", toggle = True, text = "Volume Scatter")
			raybox.prop(obj, "visible_shadow", toggle = True, text = "Shadow")
		if scene.light_group == True:
				icon = "DOWNARROW_HLT"
		else:
			icon = "RIGHTARROW"
		box.prop(scene, "light_group", text = "Light Group", icon = icon, emboss=False)
		if scene.light_group == True:
			ob = context.object
			view_layer = context.view_layer
			row = box.row(align=True)
			row.use_property_decorate = False

			sub = row.column(align=True)
			sub.prop_search(ob, "lightgroup", view_layer, "lightgroups", text="Light Group", results_are_suggestions=True)

			sub = row.column(align=True)
			sub.enabled = bool(ob.lightgroup) and not any(lg.name == ob.lightgroup for lg in view_layer.lightgroups)
			sub.operator("scene.view_layer_add_lightgroup", icon='ADD', text="").name = ob.lightgroup
		lights.draw_light_linking(scene, box, obj)

def drawobj_properties(self, context, obj):
	layout = self.layout
	box = layout.box()
	if obj.type == 'ARMATURE':
		box.label(text = "Armature Properties", icon = "OUTLINER")
		drawbone_properties(box, context, obj)

	elif obj.type == 'MESH':
		box.label(text = "Object Properties", icon = "OUTLINER")
		drawmesh_properties(box, context, obj)

def draw_data(self, context, obj):
	scene = context.scene
	modifiers_type = ["MESH", 'CURVE','GPENCIL']

	if obj.type == 'EMPTY':
		layout = self.layout
		box = layout.box()
		box.label(text = "Quick Empty Data", icon = "EMPTY_DATA")
		box.prop(obj, "empty_display_type", text = "Display As")
		box.prop(obj, "empty_display_size", text = "Size")
	
	elif obj.type == 'CURVE':
		layout = self.layout
		box = layout.box()
		box.label(text = "Quick Curve Data", icon = "CURVE_DATA")
		row = box.row()
		row.prop(obj.data, "dimensions", expand = True)
		box.prop(obj.data, "resolution_u", text = "Preview U")
		box.prop(obj.data, "render_resolution_u", text = "Render U")
		box.prop(obj.data, "extrude", text = "Extrude")
		row = box.row()
		row.prop(obj.data, "bevel_mode", expand = True)
		if not obj.data.bevel_mode == 'OBJECT':
			box.prop(obj.data, "bevel_depth", text = "Depth")
			box.prop(obj.data, "bevel_resolution", text = "Resolution")
		else:
			box.prop(obj.data, "bevel_object", text = "Object")
		box.prop(obj.data, "use_fill_caps", text = "Fill Caps")

	elif obj.type == 'LIGHT':
		layout = self.layout
		box = layout.box()
		box.label(text = "Quick Light", icon = "LIGHT_DATA")
		light = obj.data
		lights.draw_light_data(box, light)
		
	elif obj.type == 'CAMERA':
		layout = self.layout
		box = layout.box()
		box.label(text = "Quick Camera", icon = "CAMERA_DATA")
		type = "obj"
		cameras.draw_cam_data(context, box, obj, type)
		if scene.cam_shake == True:
			icon = "DOWNARROW_HLT"
		else:
			icon = "RIGHTARROW"
		box.prop(context.scene, "cam_shake", text = "Camera Shakify", icon = icon, emboss=False)
		if context.scene.cam_shake == True:
			cameras.draw_cam_shake(box, obj)

		if scene.cam_save == True:
			icon = "DOWNARROW_HLT"
		else:
			icon = "RIGHTARROW"
		box.prop(context.scene, "cam_save", text = "Camera Save List", icon = icon, emboss=False)
		if context.scene.cam_save == True:
			cameras.draw_save_cam(context, box)
	
	elif obj.type == 'GPENCIL':
		layout = self.layout
		box = layout.box()
		box.label(text = "LineArt", icon = "OUTLINER_DATA_GREASEPENCIL")
		drawlineart(context, box, obj)

	elif obj.type in modifiers_type:
		layout = self.layout
		box = layout.box()
		row = box.row()
		if scene.showmodifier == True:
			icon = "MODIFIER"
			text = "Modifiers List"
		else:
			icon = "MODIFIER_DATA"
			text = "Expand Modifiers List"
		row.prop(scene, "showmodifier", text = text, icon = icon, emboss=False)
		if scene.showmodifier == True:
			modifiers_panel.drawmodifiers(self, context, box, row, obj)

		if obj.type == 'MESH':
			if scene.particles_properties == True:
				particles.draw_particles(self, context)
			if scene.simulation == True:
				drawsimulation(self, context)

	layout = self.layout
	box = layout.box()
	row = box.row()
	if scene.showconstraints == True:
		if obj.mode != 'POSE':
			icon = "CONSTRAINT"
			text = "Constraints List"
		if obj.mode == 'POSE':
			icon = "CONSTRAINT_BONE"
			text = "Bone Constraints List"
	else:
		icon = "HIDE_OFF"
		text = "Expand Constraints List"
	row.prop(scene, "showconstraints", text = text, icon = icon, emboss=False)
	if scene.showconstraints == True:
		if obj.mode != "POSE":
			owner = "OBJECT"
			constraints_panel.drawconstraints(self, context, box, owner, row, obj)
		else:
			owner = "BONE"
			constraints_panel.draw_boneconstraints(self, context, box, owner, row, obj)

def draw_view(addon_prefs, context, box, row, obj):
	scene = context.scene
	row.label(text = "View", icon = "VIEW3D")
	row.prop(context.space_data.overlay, "show_bones", icon = "BONE_DATA", text = "")
	row.prop(context.space_data.overlay, "show_overlays", icon = "OVERLAY", text = "")
	row = box.row()
	row.prop(context.scene.render, "use_simplify", text = "Use Simplify", toggle = True)
	row.prop(context.scene.render, "simplify_subdivision", text = "Subdivision")
	box.prop(context.space_data, "lens", text = "Focal Length")
	row = box.row()
	row.prop(context.space_data, "clip_start", text = "Clip Start")
	row.prop(context.space_data, "clip_end", text = "Clip End")
	if obj:
		if obj.mode == "EDIT":
			box.label(text = "Nomrals", icon = "NORMALS_FACE")
			row = box.row()
			row.prop(context.space_data.overlay, "show_vertex_normals", text = "", icon = "NORMALS_VERTEX")
			row.prop(context.space_data.overlay, "show_split_normals", text = "", icon = "NORMALS_VERTEX_FACE")
			row.prop(context.space_data.overlay, "show_face_normals", text = "", icon = "NORMALS_FACE")
			row.prop(context.space_data.overlay, "normals_length", text = "Size")
	box.label(text = "Cursor", icon = "CURSOR")
	if addon_prefs.compact_panel == False:
		box.label(text = "Cursor Location")
	row = box.row()
	row.prop(scene.cursor, "location" ,text = "")
	box.operator("rest.cursor", text = "Rest Cursor")
	   
def drawlineart(context, box, obj):
	gpd = obj.data
	gpl = gpd.layers.active
	row = box.row()
	layer_rows = 7

	col = row.column()
	col.template_list("GPENCIL_UL_layer", "", gpd, "layers", gpd.layers, "active_index",
						rows=layer_rows, sort_reverse=True, sort_lock=True)

	col = row.column()
	sub = col.column(align=True)
	sub.operator("gpencil.layer_add", icon='ADD', text="")
	sub.operator("gpencil.layer_remove", icon='REMOVE', text="")

	sub.separator()

	if gpl:
		sub.menu("GPENCIL_MT_layer_context_menu", icon='DOWNARROW_HLT', text="")

		if len(gpd.layers) > 1:
			col.separator()

			sub = col.column(align=True)
			sub.operator("gpencil.layer_move", icon='TRIA_UP', text="").type = 'UP'
			sub.operator("gpencil.layer_move", icon='TRIA_DOWN', text="").type = 'DOWN'

			col.separator()

			sub = col.column(align=True)
			sub.operator("gpencil.layer_isolate", icon='RESTRICT_VIEW_ON', text="").affect_visibility = True
			sub.operator("gpencil.layer_isolate", icon='LOCKED', text="").affect_visibility = False

		col = box.row(align=True)
		col.prop(gpl, "blend_mode", text="Blend")

		col = box.row(align=True)
		col.prop(gpl, "opacity", text="Opacity", slider=True)

		col = box.row(align=True)
		col.prop(gpl, "use_lights")

	row = box.row()
	row.label(text = "Strokes")
	row = box.row()
	row.label(text = "Stroke Depth Order")
	row = box.row()
	row.prop(gpd, "stroke_depth_order", text="")

	if obj:
		row.enabled = not obj.show_in_front

	row = box.row()
	row.label(text = "Stroke Thickness Space")
	row = box.row()
	row.prop(gpd, "stroke_thickness_space", text="")
	row = box.row()
	row.prop(gpd, "pixel_factor", text="Thickness Scale")
	row = box.row()
	row.prop(gpd, "edit_curve_resolution")

def drawsimulation(self, context):
	obj = context.object
	layout = self.layout
	modifiers = obj.modifiers
	box = layout.box()
	box.label(text = "Simulation Cache", icon = "PHYSICS")
	try:
		modifiers["Cloth"]
		box.operator("object.modifier_remove", text = "Cloth", icon = "X").modifier="Cloth"
		row = box.row()
		row.label(text = "Cloth", icon = "MOD_CLOTH")
		jump = row.operator("bpy.ops", text = "", icon = "KEYFRAME_HLT", emboss=False)
		jump.object = str(modifiers["Cloth"].point_cache.frame_start)
		jump.id = "jump_frame"
		row.prop(modifiers["Cloth"], "show_viewport", text = "")
		row.prop(modifiers["Cloth"], "show_render", text = "")
		row = box.row()
		row.prop(modifiers["Cloth"].settings, "quality", text = "Quality Steps")
		row.prop(modifiers["Cloth"].settings, "time_scale", text = "Speed Multiplier")
		row = box.row()
		row.prop(modifiers["Cloth"].point_cache, "frame_start", text = "Start")
		row.prop(modifiers["Cloth"].point_cache, "frame_end", text = "End")
		box.prop(modifiers["Cloth"].settings, "vertex_group_mass", text = "Pin Group")
		box.label(text = "- Stiffness -")
		box.prop(modifiers["Cloth"].settings, "tension_stiffness", text = "Tension")
		box.prop(modifiers["Cloth"].settings, "compression_stiffness", text = "Compression")
		box.prop(modifiers["Cloth"].settings, "shear_stiffness", text = "Shear")
		box.prop(modifiers["Cloth"].settings, "bending_stiffness", text = "Bending")
		box.label(text = "- Damping -")
		box.prop(modifiers["Cloth"].settings, "tension_damping", text = "Tension")
		box.prop(modifiers["Cloth"].settings, "compression_damping", text = "Compression")
		box.prop(modifiers["Cloth"].settings, "shear_damping", text = "Shear")
		box.prop(modifiers["Cloth"].settings, "bending_damping", text = "Bending")
		row = box.row()
		row.prop(modifiers["Cloth"].collision_settings, "use_collision", text = "Object Collisions", toggle = True)
		if modifiers["Cloth"].collision_settings.use_collision == True:
			row.prop(modifiers["Cloth"].collision_settings, "use_self_collision", text = "Self Collisions", toggle = True)
			row = box.row()
			row.prop(modifiers["Cloth"].collision_settings, "collision_quality", text = "Quality")
			row.prop(modifiers["Cloth"].collision_settings, "distance_min", text = "Distance")
	except:
		box.operator("object.modifier_add", text = "Cloth", icon = "MOD_CLOTH").type='CLOTH'
	try:
		modifiers["Collision"]
		box.operator("object.modifier_remove", text = "Collision", icon = "X").modifier = 'Collision'
		row = box.row()
		row.label(text = "Collision", icon = "MOD_PHYSICS")
		if obj.collision.use == True:
			use = "HIDE_OFF"
		else:
			use = "HIDE_ON"
		row.prop(obj.collision, "use", text = "", toggle = True, icon = use, emboss = False)
		box.prop(obj.collision, "use_particle_kill", text = "Kill Particles", toggle = True)
		box.prop(obj.collision, "stickiness", text = "Stickiness")
		box.prop(obj.collision, "damping_factor", text = "Damping")
		box.prop(obj.collision, "damping_random", text = "Randomize")
		box.prop(obj.collision, "friction_factor", text = "Friction")
		box.prop(obj.collision, "friction_random", text = "Randomize")
	except:
		box.operator("object.modifier_add", text = "Collision", icon = "MOD_PHYSICS").type='COLLISION'

	row = box.row()
	row.operator("ptcache.bake_all", text = "Bake All Dynamics").bake=True
	row.operator("ptcache.free_bake_all", text = "Delete All Bakes")

def draw_cycles(scene, box):
	box.prop(scene.cycles, "device", text = "Device")
	box.prop(scene.cycles, "shading_system")
	box.label(text = "Samples")
	row = box.row()   
	row.prop(scene.cycles, "use_adaptive_sampling", text = "Noise Threshold")
	if scene.cycles.use_adaptive_sampling == True:
		row.prop(scene.cycles, "adaptive_threshold", text = "")
	row = box.row()
	row.prop(scene.cycles, "samples", text = "Max")
	if scene.cycles.use_adaptive_sampling == True:
		row.prop(scene.cycles, "adaptive_min_samples", text = "Min")
	box.prop(scene.cycles, "time_limit", text = "Time Limit")
	row = box.row()
	row.prop(scene.cycles, "use_denoising", text = "Denoising")
	if scene.cycles.use_denoising == True:
		row.prop(scene.cycles, "denoiser", text = "")
		row = box.row()
		row.prop(scene.cycles, "denoising_input_passes", text = "")
		if scene.cycles.denoiser == "OPENIMAGEDENOISE":
			row.prop(scene.cycles, "denoising_prefilter", text = "")
	row = box.row()
	row.prop(scene.cycles, "use_light_tree", text = "Light Tree")
	if scene.cycles.use_light_tree == False:
		row.prop(scene.cycles, "light_sampling_threshold", text = "Light Threshold")
	if scene.lightpath == True:
		icon = "DOWNARROW_HLT"
	else:
		icon = "RIGHTARROW"
	box.prop(scene, "lightpath", text = "Light Path", icon = icon, emboss=False)
	if scene.lightpath == True:
		box.prop(scene.cycles, "max_bounces", text = "Total")
		box.prop(scene.cycles, "diffuse_bounces", text = "Diffuse")
		box.prop(scene.cycles, "glossy_bounces", text = "Glossy")
		box.prop(scene.cycles, "transmission_bounces", text = "Transmission")
		box.prop(scene.cycles, "volume_bounces", text = "Volume")
		box.prop(scene.cycles, "transparent_max_bounces", text = "Transparent")
		box.label(text = "Caustics")
		row = box.row()
		row.prop(scene.cycles, "caustics_reflective", toggle = True)
		row.prop(scene.cycles, "caustics_refractive", toggle = True)

def draw_eevee(scene, box):
	box.label(text = "Samples")
	box.prop(scene.eevee, "taa_render_samples", text = "Samples")
	box.prop(scene.eevee, "use_gtao", text = "Ambient Occlusion")
	if scene.eevee.use_gtao == True:
		box.prop(scene.eevee, "gtao_distance", text = "Distance")
		box.prop(scene.eevee, "gtao_factor", text = "Factor")
		box.prop(scene.eevee, "gtao_quality", text = "Trace Precision")
		row = box.row()
		row.prop(scene.eevee, "use_gtao_bent_normals", text = "Bent Normals")
		row.prop(scene.eevee, "use_gtao_bounce", text = "Bounce")
	box.prop(scene.eevee, "use_ssr", text = "Screen Space Reflection")
	if scene.eevee.use_ssr == True:
		row = box.row()
		row.prop(scene.eevee, "use_ssr_refraction", text = "Refraction")
		row.prop(scene.eevee, "use_ssr_halfres", text = "Half Res Trace")
		box.prop(scene.eevee, "ssr_quality", text = "Trace Precision")
		box.prop(scene.eevee, "ssr_max_roughness", text = "Max Roughness")
		box.prop(scene.eevee, "ssr_thickness", text = "Thickness")
		box.prop(scene.eevee, "ssr_border_fade", text = "Edge Fade")
		box.prop(scene.eevee, "ssr_firefly_fac", text = "Clamp")
	box.label(text = "Shadows")
	box.prop(scene.eevee, "shadow_cube_size", text = "Cube Size")
	box.prop(scene.eevee, "shadow_cascade_size", text = "Cascade Size")
	row = box.row()
	row.prop(scene.eevee, "use_shadow_high_bitdepth", text = "High Bit Depth")
	row.prop(scene.eevee, "use_soft_shadows", text = "Soft Shadows")
	box.prop(scene.eevee, "light_threshold", text = "Light Threshold")
	box.label(text = "Subsurface Scattering")
	box.prop(scene.eevee, "sss_samples", text = "Samples")
	box.prop(scene.eevee, "sss_jitter_threshold", text = "Jitter Threshol")
	box.label(text = "Volumetrics")
	row = box.row()
	row.prop(scene.eevee, "volumetric_start", text = "Start")
	row.prop(scene.eevee, "volumetric_end", text = "End")
	box.prop(scene.eevee, "volumetric_tile_size", text = "Tile Size")
	box.prop(scene.eevee, "volumetric_samples", text = "Samples")
	box.prop(scene.eevee, "use_volumetric_lights", text = "Volumetric Lights")
	if scene.eevee.use_volumetric_lights == True:
		box.prop(scene.eevee, "volumetric_light_clamp", text = "Light Clamping")
	box.prop(scene.eevee, "use_volumetric_shadows", text = "Volumetric Shadows")
	if scene.eevee.use_volumetric_shadows == True:
		box.prop(scene.eevee, "volumetric_shadow_samples", text = "Sample")
	box.prop(scene.eevee, "use_bloom", text = "Bloom")
	if scene.eevee.use_bloom == True:
		box.prop(scene.eevee, "bloom_color", text = "Color")
		box.prop(scene.eevee, "bloom_threshold", text = "Threshold")
		box.prop(scene.eevee, "bloom_intensity", text = "Intensity")
		box.prop(scene.eevee, "bloom_radius", text = "Radius")
		box.prop(scene.eevee, "bloom_knee", text = "Knee")
		box.prop(scene.eevee, "bloom_clamp", text = "Clamp")
	box.prop(scene.eevee, "use_motion_blur", text = "MotionBlur")
	if scene.eevee.use_motion_blur == True:
		box.prop(scene.eevee, "motion_blur_position", text = "Position")
		box.prop(scene.eevee, "motion_blur_shutter", text = "Shutter")
		box.prop(scene.eevee, "motion_blur_depth_scale", text = "Background Sepration")
		box.prop(scene.eevee, "motion_blur_max", text = "Max Blur")
		box.prop(scene.eevee, "motion_blur_steps", text = "Steps")

def drawfile_format(scene, box):
	row = box.row()
	if scene.render.image_settings.file_format != 'OPEN_EXR_MULTILAYER':
		row.prop(scene.render.image_settings, "color_mode", text = "Color", expand = True)
	if scene.render.image_settings.file_format == 'PNG':
		row.prop(scene.render.image_settings, "color_depth", text = "Color Depth", expand = True)
		box.prop(scene.render.image_settings, "compression", text = "Compression")
	if scene.render.image_settings.file_format == 'FFMPEG':
		box.prop(scene.render.ffmpeg, "format")
		box.prop(scene.render.ffmpeg, "codec")
	if scene.render.image_settings.file_format == 'OPEN_EXR_MULTILAYER':
		box.prop(scene.render.image_settings, "color_depth", expand = True)
		box.prop(scene.render.image_settings, "exr_codec")

