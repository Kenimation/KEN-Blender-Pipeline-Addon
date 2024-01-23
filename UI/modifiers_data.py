import bpy

class DATA_modifiers:
	def __init__(self, context):
		"""The default DATA_PT_modifiers expects context as an argument,
		so this method exists only for compatibilty in modifiers_ui."""
		pass
	
	def ARMATURE(self, layout, ob, md):
			split = layout.split()

			col = split.column()
			col.label(text="Object:")
			col.prop(md, "object", text="")
			col.prop(md, "use_deform_preserve_volume")

			col = split.column()
			col.label(text="Bind To:")
			col.prop(md, "use_vertex_groups", text="Vertex Groups")
			col.prop(md, "use_bone_envelopes", text="Bone Envelopes")

			layout.separator()

			split = layout.split()

			row = split.row(align=True)
			row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
			sub = row.row(align=True)
			sub.active = bool(md.vertex_group)
			sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

			split.prop(md, "use_multi_modifier")

	def ARRAY(self, layout, _ob, md):
		layout.prop(md, "fit_type")

		if md.fit_type == 'FIXED_COUNT':
			layout.prop(md, "count")
		elif md.fit_type == 'FIT_LENGTH':
			layout.prop(md, "fit_length")
		elif md.fit_type == 'FIT_CURVE':
			layout.prop(md, "curve")

		layout.separator()

		split = layout.split()

		col = split.column()
		col.prop(md, "use_relative_offset")
		sub = col.column()
		sub.active = md.use_relative_offset
		sub.prop(md, "relative_offset_displace", text="")

		col.separator()

		col.prop(md, "use_object_offset")
		sub = col.column()
		sub.active = md.use_object_offset
		sub.prop(md, "offset_object", text="")

		col = split.column()

		col.prop(md, "use_constant_offset")
		sub = col.column()
		sub.active = md.use_constant_offset
		sub.prop(md, "constant_offset_displace", text="")

		col.separator()

		col.prop(md, "use_merge_vertices", text="Merge")
		sub = col.column()
		sub.active = md.use_merge_vertices
		sub.prop(md, "use_merge_vertices_cap", text="First Last")
		sub.prop(md, "merge_threshold", text="Distance")

		row = layout.row()
		split = row.split()
		col = split.column()
		col.label(text="UVs:")
		sub = col.column(align=True)
		sub.prop(md, "offset_u")
		sub.prop(md, "offset_v")
		layout.separator()

		layout.prop(md, "start_cap")
		layout.prop(md, "end_cap")

	def BEVEL(self, layout, ob, md):
		offset_type = md.offset_type
		
		row = layout.row()
		row.prop(md, "affect", expand = True)

		if offset_type == 'PERCENT':
			layout.prop(md, "width_pct")
		else:
			offset_text = "Width"
			if offset_type == 'ABSOLUTE':
				offset_text = "Absolute Distance"
			elif offset_type == 'DEPTH':
				offset_text = "Depth"
			elif offset_type == 'OFFSET':
				offset_text = "Offset"
			layout.prop(md, "width", text=offset_text)

		layout.row().prop(md, "segments")
		layout.row().prop(md, "profile")
		layout.row().prop(md, "material")

		layout.label(text="Limit Method:")
		layout.row().prop(md, "limit_method", expand=True)
		if md.limit_method == 'ANGLE':
			layout.prop(md, "angle_limit")
		elif md.limit_method == 'VGROUP':
			row = layout.row(align=True)
			row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
			row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		layout.separator()

		split = layout.split()
		col = split.column()
		col.prop(md, "use_clamp_overlap")
		col.prop(md, "loop_slide")
		col = split.column()
		col.prop(md, "mark_seam")
		col.prop(md, "mark_sharp")
		col.prop(md, "harden_normals")

		layout.label(text="Offset Type:")
		layout.row().prop(md, "offset_type", expand=True)

		layout.label(text="Miter Type:")
		layout.row().prop(md, "miter_outer", text="Outer")
		layout.row().prop(md, "miter_inner", text="Inner")
		if md.miter_inner in {'MITER_PATCH', 'MITER_ARC'}:
			layout.row().prop(md, "spread")

		layout.label(text="Face Strength Mode:")
		layout.row().prop(md, "face_strength_mode", expand=True)

		layout.label(text="Intersection Type:")
		layout.row().prop(md, "vmesh_method", expand=True)

		layout.label(text="Profile Type:")
		layout.row().prop(md, "profile_type", expand=True)
		row = layout.row()
		row.enabled = md.profile_type == 'CUSTOM'
		if md.profile_type == 'CUSTOM':
			layout.template_curveprofile(md, "custom_profile")

	def BOOLEAN(self, layout, _ob, md):
		layout.row().prop(md, "operation", expand=True)

		split = layout.split()

		col = split.column()
		col.label(text="Operand Type:")
		col.prop(md, "operand_type", text="")

		col = split.column()
		if md.operand_type == 'OBJECT':
			col.label(text="Object:")
			col.prop(md, "object", text="")
		elif md.operand_type == 'COLLECTION':
			col.label(text="Collection:")
			col.prop(md, "collection", text="")

		layout.separator()

		row = layout.row()
		row.label(text="Solver:")
		row.prop(md, "solver", expand=True)

		layout.separator()

		if md.solver == 'FAST':
			layout.prop(md, "double_threshold")
		elif md.solver == 'EXACT':
			row = layout.row()
			row.prop(md, "use_self")
			row.prop(md, "use_hole_tolerant")

		if bpy.app.debug:
			layout.prop(md, "debug_options")

	def BUILD(self, layout, _ob, md):
		split = layout.split()

		col = split.column()
		col.prop(md, "frame_start")
		col.prop(md, "frame_duration")
		col.prop(md, "use_reverse")

		col = split.column()
		col.prop(md, "use_random_order")
		sub = col.column()
		sub.active = md.use_random_order
		sub.prop(md, "seed")

	def MESH_CACHE(self, layout, _ob, md):
		layout.prop(md, "cache_format")
		layout.prop(md, "filepath")

		if md.cache_format == 'ABC':
			layout.prop(md, "sub_object")

		layout.label(text="Evaluation:")
		layout.prop(md, "factor", slider=True)
		layout.prop(md, "deform_mode")
		layout.prop(md, "interpolation")

		row = layout.row(align=True)
		row.label(text="Vertex Group:")
		row.prop_search(md, "vertex_group", _ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		layout.label(text="Time Mapping:")

		row = layout.row()
		row.prop(md, "time_mode", expand=True)
		row = layout.row()
		row.prop(md, "play_mode", expand=True)
		if md.play_mode == 'SCENE':
			layout.prop(md, "frame_start")
			layout.prop(md, "frame_scale")
		else:
			time_mode = md.time_mode
			if time_mode == 'FRAME':
				layout.prop(md, "eval_frame")
			elif time_mode == 'TIME':
				layout.prop(md, "eval_time")
			elif time_mode == 'FACTOR':
				layout.prop(md, "eval_factor")

		layout.label(text="Axis Mapping:")
		split = layout.split(factor=0.5, align=True)
		split.alert = (md.forward_axis[-1] == md.up_axis[-1])
		split.label(text="Forward/Up Axis:")
		split.prop(md, "forward_axis", text="")
		split.prop(md, "up_axis", text="")
		split = layout.split(factor=0.5)
		split.label(text="Flip Axis:")
		row = split.row()
		row.prop(md, "flip_axis")

	def MESH_SEQUENCE_CACHE(self, layout, ob, md):
		self._mesh_sequence_cache_3_0(layout, ob, md)

	def CAST(self, layout, ob, md):
		layout.row().prop(md, "cast_type", expand=True)

		split = layout.split(factor=0.25)

		col = split.column()
		col.prop(md, "use_x")
		col.prop(md, "use_y")
		col.prop(md, "use_z")

		col = split.column()
		col.prop(md, "factor")
		col.prop(md, "radius")
		col.prop(md, "size")
		col.prop(md, "use_radius_as_size")

		split = layout.split()

		col = split.column()
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
		col = split.column()
		col.label(text="Control Object:")
		col.prop(md, "object", text="")
		if md.object:
			col.prop(md, "use_transform")

	def CLOTH(self, layout, _ob, _md):
		layout.label(text="Settings are inside the Physics tab")

	def COLLISION(self, layout, _ob, _md):
		layout.label(text="Settings are inside the Physics tab")

	def CURVE(self, layout, ob, md):
		split = layout.split()

		col = split.column()
		col.label(text="Object:")
		col.prop(md, "object", text="")
		col = split.column()
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
		layout.label(text="Deformation Axis:")
		layout.row().prop(md, "deform_axis", expand=True)

	def DECIMATE(self, layout, ob, md):
		decimate_type = md.decimate_type

		row = layout.row()
		row.prop(md, "decimate_type", expand=True)

		if decimate_type == 'COLLAPSE':
			has_vgroup = bool(md.vertex_group)
			layout.prop(md, "ratio")

			split = layout.split()

			col = split.column()
			row = col.row(align=True)
			row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
			row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

			layout_info = col

			col = split.column()
			row = col.row()
			row.active = has_vgroup
			row.prop(md, "vertex_group_factor")

			col.prop(md, "use_collapse_triangulate")
			row = col.split(factor=0.75)
			row.prop(md, "use_symmetry")
			row.prop(md, "symmetry_axis", text="")

		elif decimate_type == 'UNSUBDIV':
			layout.prop(md, "iterations")
			layout_info = layout
		else:  # decimate_type == 'DISSOLVE':
			layout.prop(md, "angle_limit")
			layout.prop(md, "use_dissolve_boundaries")
			layout.label(text="Delimit:")
			row = layout.row()
			row.prop(md, "delimit")
			layout_info = layout

		layout_info.label(
			text=iface_("Face Count: {:,}".format(md.face_count)),
			translate=False,
		)

	def DISPLACE(self, layout, ob, md):
		has_texture = (md.texture is not None)

		col = layout.column(align=True)
		col.label(text="Texture:")
		col.template_ID(md, "texture", new="texture.new")

		split = layout.split()

		col = split.column(align=True)
		col.label(text="Direction:")
		col.prop(md, "direction", text="")
		if md.direction in {'X', 'Y', 'Z', 'RGB_TO_XYZ'}:
			col.label(text="Space:")
			col.prop(md, "space", text="")
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		col = split.column(align=True)
		col.active = has_texture
		col.label(text="Texture Coordinates:")
		col.prop(md, "texture_coords", text="")
		if md.texture_coords == 'OBJECT':
			col.label(text="Object:")
			col.prop(md, "texture_coords_object", text="")
			obj = md.texture_coords_object
			if obj and obj.type == 'ARMATURE':
				col.label(text="Bone:")
				col.prop_search(md, "texture_coords_bone", obj.data, "bones", text="")
		elif md.texture_coords == 'UV' and ob.type == 'MESH':
			col.label(text="UV Map:")
			col.prop_search(md, "uv_layer", ob.data, "uv_layers", text="")

		layout.separator()

		row = layout.row()
		row.prop(md, "mid_level")
		row.prop(md, "strength")

	def DYNAMIC_PAINT(self, layout, _ob, _md):
		layout.label(text="Settings are inside the Physics tab")

	def EDGE_SPLIT(self, layout, _ob, md):
		split = layout.split()

		col = split.column()
		col.prop(md, "use_edge_angle", text="Edge Angle")
		sub = col.column()
		sub.active = md.use_edge_angle
		sub.prop(md, "split_angle")

		split.prop(md, "use_edge_sharp", text="Sharp Edges")

	def EXPLODE(self, layout, ob, md):
		split = layout.split()

		col = split.column()
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
		sub = col.column()
		sub.active = bool(md.vertex_group)
		sub.prop(md, "protect")
		col.label(text="Particle UV")
		col.prop_search(md, "particle_uv", ob.data, "uv_layers", text="")

		col = split.column()
		col.prop(md, "use_edge_cut")
		col.prop(md, "show_unborn")
		col.prop(md, "show_alive")
		col.prop(md, "show_dead")
		col.prop(md, "use_size")

		layout.operator("object.explode_refresh", text="Refresh")

	def FLUID_SIMULATION(self, layout, _ob, _md):
		layout.label(text="Settings are inside the Physics tab")

	def HOOK(self, layout, ob, md):
		use_falloff = (md.falloff_type != 'NONE')
		split = layout.split()

		col = split.column()
		col.label(text="Object:")
		col.prop(md, "object", text="")
		if md.object and md.object.type == 'ARMATURE':
			col.label(text="Bone:")
			col.prop_search(md, "subtarget", md.object.data, "bones", text="")
		col = split.column()
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		layout.separator()

		row = layout.row(align=True)
		if use_falloff:
			row.prop(md, "falloff_radius")
		row.prop(md, "strength", slider=True)
		layout.prop(md, "falloff_type")

		col = layout.column()
		if use_falloff:
			if md.falloff_type == 'CURVE':
				col.template_curve_mapping(md, "falloff_curve")

		split = layout.split()

		col = split.column()
		col.prop(md, "use_falloff_uniform")

		if ob.mode == 'EDIT':
			row = col.row(align=True)
			row.operator("object.hook_reset", text="Reset")
			row.operator("object.hook_recenter", text="Recenter")

			row = layout.row(align=True)
			row.operator("object.hook_select", text="Select")
			row.operator("object.hook_assign", text="Assign")

	def LAPLACIANDEFORM(self, layout, ob, md):
		is_bind = md.is_bind

		layout.prop(md, "iterations")

		row = layout.row(align=True)
		row.enabled = not is_bind
		row.prop_search(md, "vertex_group", ob, "vertex_groups")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		layout.separator()

		row = layout.row()
		row.enabled = bool(md.vertex_group)
		row.operator("object.laplaciandeform_bind", text="Unbind" if is_bind else "Bind")

	def LAPLACIANSMOOTH(self, layout, ob, md):
		layout.prop(md, "iterations")

		split = layout.split(factor=0.25)

		col = split.column()
		col.label(text="Axis:")
		col.prop(md, "use_x")
		col.prop(md, "use_y")
		col.prop(md, "use_z")

		col = split.column()
		col.label(text="Lambda:")
		col.prop(md, "lambda_factor", text="Factor")
		col.prop(md, "lambda_border", text="Border")

		col.separator()
		col.prop(md, "use_volume_preserve")
		col.prop(md, "use_normalized")

		layout.label(text="Vertex Group:")
		row = layout.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

	def LATTICE(self, layout, ob, md):
		split = layout.split()

		col = split.column()
		col.label(text="Object:")
		col.prop(md, "object", text="")

		col = split.column()
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		layout.separator()
		layout.prop(md, "strength", slider=True)

	def MASK(self, layout, ob, md):
		layout.row().prop(md, "mode", expand=True)

		if md.mode == 'ARMATURE':
			layout.label(text="Armature:")
			row = layout.row(align=True)
			row.prop(md, "armature", text="")
			sub = row.row(align=True)
			sub.active = (md.armature is not None)
			sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
		elif md.mode == 'VERTEX_GROUP':
			layout.label(text="Vertex Group:")
			row = layout.row(align=True)
			row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
			sub = row.row(align=True)
			sub.active = bool(md.vertex_group)
			sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
			layout.prop(md, "use_smooth")

		col = layout.column()
		col.prop(md, "threshold")

	def MESH_DEFORM(self, layout, ob, md):
		split = layout.split()

		col = split.column()
		col.enabled = not md.is_bound
		col.label(text="Object:")
		col.prop(md, "object", text="")

		col = split.column()
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		sub = row.row(align=True)
		sub.active = bool(md.vertex_group)
		sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		layout.separator()
		row = layout.row()
		row.enabled = not md.is_bound
		row.prop(md, "precision")
		row.prop(md, "use_dynamic_bind")

		layout.separator()
		if md.is_bound:
			layout.operator("object.meshdeform_bind", text="Unbind")
		else:
			layout.operator("object.meshdeform_bind", text="Bind")

	def MIRROR(self, layout, _ob, md):
		axis_text = "XYZ"
		split = layout.split(factor=0.33)

		row = layout.row()
		row.label(text="Axis:")
		for i, text in enumerate(axis_text):
			row.prop(md, "use_axis", text=text, index=i, toggle = True)

		row = layout.row()
		row.label(text="Bisect:")
		for i, text in enumerate(axis_text):
			colsub = row.column()
			colsub.prop(md, "use_bisect_axis", text=text, index=i, toggle = True)

		row = layout.row()
		row.label(text="Flip:")
		for i, text in enumerate(axis_text):
			colsub = row.column()
			colsub.prop(md, "use_bisect_flip_axis", text=text, index=i, toggle = True)
			colsub.active = md.use_axis[i] and md.use_bisect_axis[i]

		col = layout.column()
		col.label(text="Mirror Object:")
		col.prop(md, "mirror_object", text="")

		col = layout.column()
		col.label(text="Options:")

		row = layout.row()
		row.prop(md, "use_clip", text="Clipping")
		row = layout.row()
		row.prop(md, "use_mirror_merge", text="Merge")

		col = layout.column()
		if md.use_mirror_merge is True:
			col.prop(md, "merge_threshold")

		row = layout.row()
		row.active = any(md.use_bisect_axis)
		row.prop(md, "bisect_threshold")

		col = layout.column()
		col.label(text="Textures:")
		row = col.row()
		lrow = row.row()
		lrow.alignment = 'LEFT'
		lrow.prop(md, "use_mirror_u", text="Mirror U")
		if md.use_mirror_u:
			row.prop(md, "mirror_offset_u", text="")
		row = layout.row()
		lrow = row.row()
		lrow.alignment = 'LEFT'
		lrow.prop(md, "use_mirror_v", text="Mirror V")
		if md.use_mirror_v:
			row.prop(md, "mirror_offset_v", text="")

		col = layout.column(align=True)
		col.prop(md, "offset_u")
		col.prop(md, "offset_v")
		col.prop(md, "use_mirror_vertex_groups", text="Vertex Groups")
		col.prop(md, "use_mirror_udim", text="Flip UDIM")

	def MULTIRES(self, layout, ob, md):
		# Changing some of the properties can not be done once there is an
		# actual displacement stored for this multires modifier. This check
		# will disallow those properties from change.
		# This is a bit stupid check but should be sufficient for the usual
		# multires usage. It might become less strict and only disallow
		# modifications if there is CD_MDISPS layer, or if there is actual
		# non-zero displacement but such checks will be too slow to be done
		# on every redraw.
		have_displacement = (md.total_levels != 0)

		split = layout.split()
		col = split.column()
		col.prop(md, "levels", text="Preview")
		col.prop(md, "sculpt_levels", text="Sculpt")
		col.prop(md, "render_levels", text="Render")

		row = col.row()
		row.enabled = not have_displacement
		row.prop(md, "quality")

		row = col.row()
		row.enabled = ob.mode == 'SCULPT'
		row.prop(md, "use_sculpt_base_mesh")

		col.prop(md, "show_only_control_edges")

		sub = col.column()
		sub.active = not have_displacement

		sub.label(text="UV Smooth:")
		sub.prop(md, "uv_smooth", text="")

		sub.label(text="Boundary Smooth:")
		sub.prop(md, "boundary_smooth", text="")

		sub.prop(md, "use_creases")
		sub.prop(md, "use_custom_normals")

		layout.separator()

		col = split.column()

		col.enabled = ob.mode != 'EDIT'
		op = col.operator("object.multires_subdivide", text="Subdivide")
		op.mode = 'CATMULL_CLARK'

		op = col.operator("object.multires_subdivide", text="Subdivide Simple")
		op.mode = 'SIMPLE'

		op = col.operator("object.multires_subdivide", text="Subdivide Linear")
		op.mode = 'LINEAR'

		col.operator("object.multires_higher_levels_delete", text="Delete Higher")
		col.operator("object.multires_unsubdivide", text="Unsubdivide")
		col.operator("object.multires_reshape", text="Reshape")
		col.operator("object.multires_base_apply", text="Apply Base")

		if not have_displacement:
			col.separator()

			col.operator("object.multires_rebuild_subdiv", text="Rebuild Subdivisions")

		col.separator()

		row = col.row()
		if md.is_external:
			row.operator("object.multires_external_pack", text="Pack External")
			row = col.row()
			row.prop(md, "filepath", text="")
		else:
			row.operator("object.multires_external_save", text="Save External...")

	def OCEAN(self, layout, _ob, md):
		if not bpy.app.build_options.mod_oceansim:
			layout.label(text="Built without OceanSim modifier")
			return

		layout.prop(md, "geometry_mode")

		if md.geometry_mode == 'GENERATE':
			row = layout.row()
			row.prop(md, "repeat_x")
			row.prop(md, "repeat_y")

		layout.separator()

		split = layout.split()

		col = split.column()
		col.prop(md, "time")
		col.prop(md, "depth")
		col.prop(md, "random_seed")

		col = split.column()
		col.prop(md, "viewport_resolution")
		col.prop(md, "resolution")
		col.prop(md, "size")
		col.prop(md, "spatial_size")

		layout.separator()

		layout.prop(md, "spectrum")

		if md.spectrum in {'TEXEL_MARSEN_ARSLOE', 'JONSWAP'}:
			split = layout.split()

			col = split.column()
			col.prop(md, "sharpen_peak_jonswap")

			col = split.column()
			col.prop(md, "fetch_jonswap")

		layout.label(text="Waves:")

		split = layout.split()

		col = split.column()
		col.prop(md, "choppiness")
		col.prop(md, "wave_scale", text="Scale")
		col.prop(md, "wave_scale_min")
		col.prop(md, "wind_velocity")

		col = split.column()
		col.prop(md, "wave_alignment", text="Alignment")
		sub = col.column()
		sub.active = (md.wave_alignment > 0.0)
		sub.prop(md, "wave_direction", text="Direction")
		sub.prop(md, "damping")

		layout.separator()

		layout.prop(md, "use_normals")

		split = layout.split()

		col = split.column()
		col.prop(md, "use_foam")
		sub = col.row()
		sub.active = md.use_foam
		sub.prop(md, "foam_coverage", text="Coverage")

		col = split.column()
		col.active = md.use_foam
		col.label(text="Foam Data Layer Name:")
		col.prop(md, "foam_layer_name", text="")

		split = layout.split()
		split.active = md.use_foam

		col = split.column()
		col.prop(md, "use_spray", text="Generate Spray")
		sub = col.row()
		sub.active = md.use_spray
		sub.prop(md, "invert_spray", text="Invert Spray")

		col = split.column()
		col.active = md.use_spray
		col.label(text="Spray Data Layer Name:")
		col.prop(md, "spray_layer_name", text="")

		layout.separator()

		if md.is_cached:
			layout.operator("object.ocean_bake", text="Delete Bake").free = True
		else:
			layout.operator("object.ocean_bake").free = False

		split = layout.split()
		split.enabled = not md.is_cached

		col = split.column(align=True)
		col.prop(md, "frame_start", text="Start")
		col.prop(md, "frame_end", text="End")

		col = split.column(align=True)
		col.label(text="Cache path:")
		col.prop(md, "filepath", text="")

		split = layout.split()
		split.enabled = not md.is_cached

		col = split.column()
		col.active = md.use_foam
		col.prop(md, "bake_foam_fade")

		col = split.column()

	def PARTICLE_INSTANCE(self, layout, ob, md):
		layout.prop(md, "object")
		if md.object:
			layout.prop_search(md, "particle_system", md.object, "particle_systems", text="Particle System")
		else:
			layout.prop(md, "particle_system_index", text="Particle System")

		split = layout.split()
		col = split.column()
		col.label(text="Create From:")
		layout.prop(md, "space", text="")
		col.prop(md, "use_normal")
		col.prop(md, "use_children")
		col.prop(md, "use_size")

		col = split.column()
		col.label(text="Show Particles When:")
		col.prop(md, "show_alive")
		col.prop(md, "show_unborn")
		col.prop(md, "show_dead")

		row = layout.row(align=True)
		row.prop(md, "particle_amount", text="Amount")
		row.prop(md, "particle_offset", text="Offset")

		row = layout.row(align=True)
		row.prop(md, "axis", expand=True)

		layout.separator()

		layout.prop(md, "use_path", text="Create Along Paths")

		col = layout.column()
		col.active = md.use_path
		col.prop(md, "use_preserve_shape")

		row = col.row(align=True)
		row.prop(md, "position", slider=True)
		row.prop(md, "random_position", text="Random", slider=True)
		row = col.row(align=True)
		row.prop(md, "rotation", slider=True)
		row.prop(md, "random_rotation", text="Random", slider=True)

		layout.separator()

		col = layout.column()
		col.prop_search(md, "index_layer_name", ob.data, "vertex_colors", text="Index Layer")
		col.prop_search(md, "value_layer_name", ob.data, "vertex_colors", text="Value Layer")

	def PARTICLE_SYSTEM(self, layout, _ob, _md):
		layout.label(text="Settings can be found inside the Particle context")

	def SCREW(self, layout, _ob, md):
		split = layout.split()

		col = split.column()
		col.prop(md, "axis")
		col.prop(md, "object", text="AxisOb")
		col.prop(md, "angle")
		col.prop(md, "steps")
		col.prop(md, "render_steps")
		col.prop(md, "use_smooth_shade")
		col.prop(md, "use_merge_vertices")
		sub = col.column()
		sub.active = md.use_merge_vertices
		sub.prop(md, "merge_threshold")

		col = split.column()
		row = col.row()
		row.active = (md.object is None or md.use_object_screw_offset is False)
		row.prop(md, "screw_offset")
		row = col.row()
		row.active = (md.object is not None)
		row.prop(md, "use_object_screw_offset")
		col.prop(md, "use_normal_calculate")
		col.prop(md, "use_normal_flip")
		col.prop(md, "iterations")
		col.prop(md, "use_stretch_u")
		col.prop(md, "use_stretch_v")

	def SHRINKWRAP(self, layout, ob, md):
		split = layout.split()
		col = split.column()
		col.label(text="Target:")
		col.prop(md, "target", text="")
		col = split.column()
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		split = layout.split()

		col = split.column()
		col.prop(md, "offset")

		col = split.column()
		col.label(text="Mode:")
		col.prop(md, "wrap_method", text="")

		if md.wrap_method in {'PROJECT', 'NEAREST_SURFACEPOINT', 'TARGET_PROJECT'}:
			col.prop(md, "wrap_mode", text="")

		if md.wrap_method == 'PROJECT':
			split = layout.split()
			col = split.column()
			col.prop(md, "subsurf_levels")
			col = split.column()

			col.prop(md, "project_limit", text="Limit")
			split = layout.split(factor=0.25)

			col = split.column()
			col.label(text="Axis:")
			col.prop(md, "use_project_x")
			col.prop(md, "use_project_y")
			col.prop(md, "use_project_z")

			col = split.column()
			col.label(text="Direction:")
			col.prop(md, "use_negative_direction")
			col.prop(md, "use_positive_direction")

			subcol = col.column()
			subcol.active = md.use_negative_direction and md.cull_face != 'OFF'
			subcol.prop(md, "use_invert_cull")

			col = split.column()
			col.label(text="Cull Faces:")
			col.prop(md, "cull_face", expand=True)

			layout.prop(md, "auxiliary_target")

	def SIMPLE_DEFORM(self, layout, ob, md):

		layout.row().prop(md, "deform_method", expand=True)

		split = layout.split()

		col = split.column()
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		split = layout.split()

		col = split.column()
		col.label(text="Axis, Origin:")
		col.prop(md, "origin", text="")

		col.prop(md, "deform_axis")

		if md.deform_method in {'TAPER', 'STRETCH', 'TWIST'}:
			row = col.row(align=True)
			row.label(text="Lock:")
			deform_axis = md.deform_axis
			if deform_axis != 'X':
				row.prop(md, "lock_x")
			if deform_axis != 'Y':
				row.prop(md, "lock_y")
			if deform_axis != 'Z':
				row.prop(md, "lock_z")

		col = split.column()
		col.label(text="Deform:")
		if md.deform_method in {'TAPER', 'STRETCH'}:
			col.prop(md, "factor")
		else:
			col.prop(md, "angle")
		col.prop(md, "limits", slider=True)

	def FLUID(self, layout, _ob, _md):
		layout.label(text="Settings are inside the Physics tab")

	def SMOOTH(self, layout, ob, md):
		split = layout.split(factor=0.25)

		col = split.column()
		col.label(text="Axis:")
		col.prop(md, "use_x")
		col.prop(md, "use_y")
		col.prop(md, "use_z")

		col = split.column()
		col.prop(md, "factor")
		col.prop(md, "iterations")
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

	def SOFT_BODY(self, layout, _ob, _md):
		layout.label(text="Settings are inside the Physics tab")

	def SOLIDIFY(self, layout, ob, md):

		layout.row().prop(md, "solidify_mode", expand=True)

		solidify_mode = md.solidify_mode

		if solidify_mode == 'NON_MANIFOLD':
			layout.prop(md, "nonmanifold_thickness_mode")
			layout.prop(md, "nonmanifold_boundary_mode")

		layout.prop(md, "thickness")
		layout.prop(md, "offset")

		split = layout.split()

		col = split.column()

		if solidify_mode == 'EXTRUDE':
			col.prop(md, "use_even_offset")

		col.prop(md, "use_flip_normals")

		if solidify_mode == 'EXTRUDE':
			col.prop(md, "use_quality_normals")

		col.prop(md, "use_rim")
		col_rim = col.column()
		col_rim.active = md.use_rim
		col_rim.prop(md, "use_rim_only")

		col = split.column()
		col.prop(md, "thickness_clamp")
		row = col.row()
		row.active = md.thickness_clamp > 0.0
		row.prop(md, "use_thickness_angle_clamp")

		col.separator()

		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		sub = row.row(align=True)
		sub.active = bool(md.vertex_group)
		sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		sub = col.row()
		sub.active = bool(md.vertex_group)
		sub.prop(md, "thickness_vertex_group", text="Factor")
		if solidify_mode == 'NON_MANIFOLD':
			sub = col.row()
			sub.active = bool(md.vertex_group)
			sub.prop(md, "use_flat_faces")

		split = layout.split()

		col = split.column()

		if solidify_mode == 'EXTRUDE':
			col.label(text="Crease:")
			col.prop(md, "edge_crease_inner", text="Inner")
			col.prop(md, "edge_crease_outer", text="Outer")
			col.prop(md, "edge_crease_rim", text="Rim")
			col.label(text="Bevel:")
			col.prop(md, "bevel_convex")
		else:
			col.label(text="Bevel:")
			col.prop(md, "bevel_convex")
			col.separator()
			col.prop(md, "nonmanifold_merge_threshold")

		col.separator()

		col.label(text="Material Index Offset:")

		sub = col.column()
		row = sub.split(factor=0.4, align=True)
		row.prop(md, "material_offset", text="")
		row = row.row(align=True)
		row.active = md.use_rim
		row.prop(md, "material_offset_rim", text="Rim")

		col.separator()

		row = col.row(align=True)
		row.label(text="Shell Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "shell_vertex_group", ob, "vertex_groups", text="")
		row = col.row(align=True)
		row.label(text="Rim Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "rim_vertex_group", ob, "vertex_groups", text="")

	def SUBSURF(self, layout, ob, md):
		from bpy import context
		layout.row().prop(md, "subdivision_type", expand=True)

		split = layout.split()
		col = split.column()

		scene = context.scene
		engine = context.engine
		show_adaptive_options = (
			engine == 'CYCLES' and md == ob.modifiers[-1]
			and scene.cycles.feature_set == 'EXPERIMENTAL' and md.use_limit_surface
		)

		if show_adaptive_options:
			col.label(text="Render:")
			col.prop(ob.cycles, "use_adaptive_subdivision", text="Adaptive")
			
			col.label(text="Viewport:")
			col.prop(md, "levels", text="Levels")

			col.separator()
			if ob.cycles.use_adaptive_subdivision:
				col.prop(ob.cycles, "dicing_rate")
			else:
				col.prop(md, "render_levels", text="Levels")


			col.separator()
		else:
			col.label(text="Subdivisions:")
			sub = col.column(align=True)
			sub.prop(md, "render_levels", text="Render")
			sub.prop(md, "levels", text="Viewport")

		sub = col.column()
		sub.prop(md, "show_only_control_edges")
		sub.active = (not show_adaptive_options) or (not ob.cycles.use_adaptive_subdivision)

		split = layout.split()
		col = split.column()

		sub = col.column()
		sub.active = (not show_adaptive_options) or (not ob.cycles.use_adaptive_subdivision)
		sub.label(text="UV Smooth:")
		sub.prop(md, "use_limit_surface")
		sub.prop(md, "quality")
		sub.prop(md, "uv_smooth", text="")
		sub.label(text="Boundary Smooth:")
		sub.prop(md, "boundary_smooth", text="")
		sub.prop(md, "use_creases")
		sub.prop(md, "use_custom_normals")

		if show_adaptive_options and ob.cycles.use_adaptive_subdivision:
			col = layout.column(align=True)
			col.scale_y = 0.6
			col.separator()
			col.label(text="Final Dicing Rate:")
			col.separator()

			render = max(scene.cycles.dicing_rate * ob.cycles.dicing_rate, 0.1)
			preview = max(scene.cycles.preview_dicing_rate * ob.cycles.dicing_rate, 0.1)
			col.label(text=f"Render {render:.2f} px, Preview {preview:.2f} px")

	def SURFACE(self, layout, _ob, _md):
		layout.label(text="Settings are inside the Physics tab")

	def SURFACE_DEFORM(self, layout, _ob, md):
		split = layout.split()
		col = split.column()
		col.active = not md.is_bound
		col.label(text="Target:")
		col.prop(md, "target", text="")

		col = split.column()
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", _ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		split = layout.split()
		col = split.column()
		col.active = not md.is_bound
		col.prop(md, "falloff")

		row = col.row()
		row.enabled = not md.is_bound
		row.active = not md.is_bound and bool(md.vertex_group)
		row.prop(md, "use_sparse_bind")

		col = split.column()
		col.prop(md, "strength")

		col = layout.column()

		if md.is_bound:
			col.operator("object.surfacedeform_bind", text="Unbind")
		else:
			col.active = md.target is not None
			col.operator("object.surfacedeform_bind", text="Bind")

	def UV_PROJECT(self, layout, ob, md):
		split = layout.split()
		col = split.column()
		col.prop_search(md, "uv_layer", ob.data, "uv_layers")
		col.separator()

		col.prop(md, "projector_count", text="Projectors")
		for proj in md.projectors:
			col.prop(proj, "object", text="")

		col = split.column()
		col.active = any([p.object and p.object.type == 'CAMERA' for p in md.projectors])

		sub = col.column(align=True)
		sub.prop(md, "aspect_x", text="Aspect X")
		sub.prop(md, "aspect_y", text="Aspect Y")

		sub = col.column(align=True)
		sub.prop(md, "scale_x", text="Scale X")
		sub.prop(md, "scale_y", text="Scale Y")

	def WARP(self, layout, ob, md):
		use_falloff = (md.falloff_type != 'NONE')
		split = layout.split()

		col = split.column()
		col.label(text="From:")
		col.prop(md, "object_from", text="")

		col = split.column()
		col.label(text="To:")
		col.prop(md, "object_to", text="")

		split = layout.split()
		col = split.column()
		obj = md.object_from
		if obj and obj.type == 'ARMATURE':
			col.label(text="Bone:")
			col.prop_search(md, "bone_from", obj.data, "bones", text="")

		col = split.column()
		obj = md.object_to
		if obj and obj.type == 'ARMATURE':
			col.label(text="Bone:")
			col.prop_search(md, "bone_to", obj.data, "bones", text="")

		split = layout.split()
		col = split.column()
		col.prop(md, "use_volume_preserve")
		col = split.column()
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		col = layout.column()

		row = col.row(align=True)
		row.prop(md, "strength")
		if use_falloff:
			row.prop(md, "falloff_radius")

		col.prop(md, "falloff_type")
		if use_falloff:
			if md.falloff_type == 'CURVE':
				col.template_curve_mapping(md, "falloff_curve")

		# 2 new columns
		split = layout.split()
		col = split.column()
		col.label(text="Texture:")
		col.template_ID(md, "texture", new="texture.new")

		col = split.column()
		col.label(text="Texture Coordinates:")
		col.prop(md, "texture_coords", text="")

		if md.texture_coords == 'OBJECT':
			layout.prop(md, "texture_coords_object", text="Object")
			obj = md.texture_coords_object
			if obj and obj.type == 'ARMATURE':
				layout.prop_search(md, "texture_coords_bone", obj.data, "bones", text="Bone")
		elif md.texture_coords == 'UV' and ob.type == 'MESH':
			layout.prop_search(md, "uv_layer", ob.data, "uv_layers")

	def WAVE(self, layout, ob, md):
		split = layout.split()

		col = split.column()
		col.label(text="Motion:")
		col.prop(md, "use_x")
		col.prop(md, "use_y")
		col.prop(md, "use_cyclic")

		col = split.column()
		col.prop(md, "use_normal")
		sub = col.column()
		sub.active = md.use_normal
		sub.prop(md, "use_normal_x", text="X")
		sub.prop(md, "use_normal_y", text="Y")
		sub.prop(md, "use_normal_z", text="Z")

		split = layout.split()

		col = split.column()
		col.label(text="Time:")
		sub = col.column(align=True)
		sub.prop(md, "time_offset", text="Offset")
		sub.prop(md, "lifetime", text="Life")
		col.prop(md, "damping_time", text="Damping")

		col = split.column()
		col.label(text="Position:")
		sub = col.column(align=True)
		sub.prop(md, "start_position_x", text="X")
		sub.prop(md, "start_position_y", text="Y")
		col.prop(md, "falloff_radius", text="Falloff")

		layout.separator()

		layout.prop(md, "start_position_object")
		row = layout.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
		split = layout.split(factor=0.33)
		col = split.column()
		col.label(text="Texture")
		col = split.column()
		col.template_ID(md, "texture", new="texture.new")
		layout.prop(md, "texture_coords")
		if md.texture_coords == 'UV' and ob.type == 'MESH':
			layout.prop_search(md, "uv_layer", ob.data, "uv_layers")
		elif md.texture_coords == 'OBJECT':
			layout.prop(md, "texture_coords_object")
			obj = md.texture_coords_object
			if obj and obj.type == 'ARMATURE':
				layout.prop_search(md, "texture_coords_bone", obj.data, "bones")

		layout.separator()

		split = layout.split()

		col = split.column()
		col.prop(md, "speed", slider=True)
		col.prop(md, "height", slider=True)

		col = split.column()
		col.prop(md, "width", slider=True)
		col.prop(md, "narrowness", slider=True)

	def REMESH(self, layout, _ob, md):
		if not bpy.app.build_options.mod_remesh:
			layout.label(text="Built without Remesh modifier")
			return

		layout.row().prop(md, "mode", expand=True)

		row = layout.row()
		if md.mode == 'VOXEL':
			layout.prop(md, "voxel_size")
			layout.prop(md, "adaptivity")
		else:
			row.prop(md, "octree_depth")
			row.prop(md, "scale")

			if md.mode == 'SHARP':
				layout.prop(md, "sharpness")

			layout.prop(md, "use_remove_disconnected")
			row = layout.row()
			row.active = md.use_remove_disconnected
			row.prop(md, "threshold")

		layout.prop(md, "use_smooth_shade")

	@staticmethod
	def vertex_weight_mask(layout, ob, md):
		layout.label(text="Influence/Mask Options:")

		split = layout.split(factor=0.4)
		split.label(text="Global Influence:")
		split.prop(md, "mask_constant", text="")

		if not md.mask_texture:
			split = layout.split(factor=0.4)
			split.label(text="Vertex Group Mask:")
			row = split.row(align=True)
			row.prop_search(md, "mask_vertex_group", ob, "vertex_groups", text="")
			row.prop(md, "invert_mask_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		if not md.mask_vertex_group:
			split = layout.split(factor=0.4)
			split.label(text="Texture Mask:")
			split.template_ID(md, "mask_texture", new="texture.new")
			if md.mask_texture:
				split = layout.split()

				col = split.column()
				col.label(text="Texture Coordinates:")
				col.prop(md, "mask_tex_mapping", text="")

				col = split.column()
				col.label(text="Use Channel:")
				col.prop(md, "mask_tex_use_channel", text="")

				if md.mask_tex_mapping == 'OBJECT':
					layout.prop(md, "mask_tex_map_object", text="Object")
					obj = md.mask_tex_map_object
					if obj and obj.type == 'ARMATURE':
						layout.prop_search(md, "mask_tex_map_bone", obj.data, "bones", text="Bone")
				elif md.mask_tex_mapping == 'UV' and ob.type == 'MESH':
					layout.prop_search(md, "mask_tex_uv_layer", ob.data, "uv_layers")

	def VERTEX_WEIGHT_EDIT(self, layout, ob, md):
		split = layout.split()

		col = split.column()
		col.label(text="Vertex Group:")
		col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

		col.label(text="Default Weight:")
		col.prop(md, "default_weight", text="")

		col = split.column()
		col.prop(md, "use_add")
		sub = col.column()
		sub.active = md.use_add
		sub.prop(md, "add_threshold")

		col = col.column()
		col.prop(md, "use_remove")
		sub = col.column()
		sub.active = md.use_remove
		sub.prop(md, "remove_threshold")

		layout.separator()

		row = layout.row(align=True)
		row.prop(md, "falloff_type")
		row.prop(md, "invert_falloff", text="", icon='ARROW_LEFTRIGHT')
		if md.falloff_type == 'CURVE':
			layout.template_curve_mapping(md, "map_curve")

		row = layout.row(align=True)
		row.prop(md, "normalize")

		# Common mask options
		layout.separator()
		self.vertex_weight_mask(layout, ob, md)

	def VERTEX_WEIGHT_MIX(self, layout, ob, md):
		split = layout.split()

		col = split.column()
		col.label(text="Vertex Group A:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group_a", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group_a", text="", icon='ARROW_LEFTRIGHT')
		col.label(text="Default Weight A:")
		col.prop(md, "default_weight_a", text="")

		col.label(text="Mix Mode:")
		col.prop(md, "mix_mode", text="")

		col = split.column()
		col.label(text="Vertex Group B:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group_b", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group_b", text="", icon='ARROW_LEFTRIGHT')
		col.label(text="Default Weight B:")
		col.prop(md, "default_weight_b", text="")

		col.label(text="Mix Set:")
		col.prop(md, "mix_set", text="")

		row = layout.row(align=True)
		row.prop(md, "normalize")

		# Common mask options
		layout.separator()
		self.vertex_weight_mask(layout, ob, md)

	def VERTEX_WEIGHT_PROXIMITY(self, layout, ob, md):
		split = layout.split()

		col = split.column()
		col.label(text="Vertex Group:")
		col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

		col = split.column()
		col.label(text="Target Object:")
		col.prop(md, "target", text="")

		split = layout.split()

		col = split.column()
		col.label(text="Distance:")
		col.prop(md, "proximity_mode", text="")
		if md.proximity_mode == 'GEOMETRY':
			col.row().prop(md, "proximity_geometry")

		col = split.column()
		col.label()
		col.prop(md, "min_dist")
		col.prop(md, "max_dist")

		layout.separator()
		row = layout.row(align=True)
		row.prop(md, "falloff_type")

		if md.falloff_type == 'CURVE':
			layout.template_curve_mapping(md, "map_curve")

		row.prop(md, "invert_falloff", text="", icon='ARROW_LEFTRIGHT')

		row = layout.row(align=True)
		row.prop(md, "normalize")

		# Common mask options
		layout.separator()
		self.vertex_weight_mask(layout, ob, md)

	def SKIN(self, layout, _ob, md):
		row = layout.row()
		row.operator("object.skin_armature_create", text="Create Armature")
		row.operator("mesh.customdata_skin_add")

		layout.separator()

		row = layout.row(align=True)
		row.prop(md, "branch_smoothing")
		row.prop(md, "use_smooth_shade")

		split = layout.split()

		col = split.column()
		col.label(text="Selected Vertices:")
		sub = col.column(align=True)
		sub.operator("object.skin_loose_mark_clear", text="Mark Loose").action = 'MARK'
		sub.operator("object.skin_loose_mark_clear", text="Clear Loose").action = 'CLEAR'

		sub = col.column()
		sub.operator("object.skin_root_mark", text="Mark Root")
		sub.operator("object.skin_radii_equalize", text="Equalize Radii")

		col = split.column()
		col.label(text="Symmetry Axes:")
		col.prop(md, "use_x_symmetry")
		col.prop(md, "use_y_symmetry")
		col.prop(md, "use_z_symmetry")

	def TRIANGULATE(self, layout, _ob, md):
		row = layout.row()

		col = row.column()
		col.label(text="Quad Method:")
		col.prop(md, "quad_method", text="")
		col.prop(md, "keep_custom_normals")
		col = row.column()
		col.label(text="Ngon Method:")
		col.prop(md, "ngon_method", text="")
		col.label(text="Minimum Vertices:")
		col.prop(md, "min_vertices", text="")

	def UV_WARP(self, layout, ob, md):
		split = layout.split()
		col = split.column()
		col.prop(md, "center")

		col = split.column()
		col.label(text="UV Axis:")
		col.prop(md, "axis_u", text="")
		col.prop(md, "axis_v", text="")

		split = layout.split()
		col = split.column()
		col.label(text="From:")
		col.prop(md, "object_from", text="")

		col = split.column()
		col.label(text="To:")
		col.prop(md, "object_to", text="")

		split = layout.split()
		col = split.column()
		obj = md.object_from
		if obj and obj.type == 'ARMATURE':
			col.label(text="Bone:")
			col.prop_search(md, "bone_from", obj.data, "bones", text="")

		col = split.column()
		obj = md.object_to
		if obj and obj.type == 'ARMATURE':
			col.label(text="Bone:")
			col.prop_search(md, "bone_to", obj.data, "bones", text="")

		split = layout.split()
		col = split.column()
		col.label(text="Offset:")
		col.prop(md, "offset", text="")

		col = split.column()
		col.label(text="Scale:")
		col.prop(md, "scale", text="")

		col = split.column()
		col.label(text="Rotate:")
		col.prop(md, "rotation", text="")

		split = layout.split()

		col = split.column()
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		col = split.column()
		col.label(text="UV Map:")
		col.prop_search(md, "uv_layer", ob.data, "uv_layers", text="")

	def WIREFRAME(self, layout, ob, md):
		has_vgroup = bool(md.vertex_group)

		split = layout.split()

		col = split.column()
		col.prop(md, "thickness", text="Thickness")

		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		sub = row.row(align=True)
		sub.active = has_vgroup
		sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
		row = col.row(align=True)
		row.active = has_vgroup
		row.prop(md, "thickness_vertex_group", text="Factor")

		col.prop(md, "use_crease", text="Crease Edges")
		row = col.row()
		row.active = md.use_crease
		row.prop(md, "crease_weight", text="Crease Weight")

		col = split.column()

		col.prop(md, "offset")
		col.prop(md, "use_even_offset", text="Even Thickness")
		col.prop(md, "use_relative_offset", text="Relative Thickness")
		col.prop(md, "use_boundary", text="Boundary")
		col.prop(md, "use_replace", text="Replace Original")

		col.prop(md, "material_offset", text="Material Offset")

	def WELD(self, layout, ob, md):
		layout.row().prop(md, "mode", expand=True)
		layout.prop(md, "merge_threshold", text="Distance")

		if md.mode == 'CONNECTED':
			layout.prop(md, "loose_edges")

		row = layout.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

	def DATA_TRANSFER(self, layout, ob, md):
		row = layout.row(align=True)
		row.prop(md, "object")
		sub = row.row(align=True)
		sub.active = bool(md.object)
		sub.prop(md, "use_object_transform", text="", icon='GROUP')

		layout.separator()

		split = layout.split(factor=0.333)
		split.prop(md, "use_vert_data")
		use_vert = md.use_vert_data
		row = split.row()
		row.active = use_vert
		row.prop(md, "vert_mapping", text="")
		if use_vert:
			col = layout.column(align=True)
			split = col.split(factor=0.333, align=True)
			sub = split.column(align=True)
			sub.prop(md, "data_types_verts")
			sub = split.column(align=True)
			row = sub.row(align=True)
			row.prop(md, "layers_vgroup_select_src", text="")
			row.label(icon='RIGHTARROW')
			row.prop(md, "layers_vgroup_select_dst", text="")
			row = sub.row(align=True)
			row.label(text="", icon='NONE')

		layout.separator()

		split = layout.split(factor=0.333)
		split.prop(md, "use_edge_data")
		use_edge = md.use_edge_data
		row = split.row()
		row.active = use_edge
		row.prop(md, "edge_mapping", text="")
		if use_edge:
			col = layout.column(align=True)
			split = col.split(factor=0.333, align=True)
			sub = split.column(align=True)
			sub.prop(md, "data_types_edges")

		layout.separator()

		split = layout.split(factor=0.333)
		split.prop(md, "use_loop_data")
		use_loop = md.use_loop_data
		row = split.row()
		row.active = use_loop
		row.prop(md, "loop_mapping", text="")
		if use_loop:
			col = layout.column(align=True)
			split = col.split(factor=0.333, align=True)
			sub = split.column(align=True)
			sub.prop(md, "data_types_loops")
			sub = split.column(align=True)
			row = sub.row(align=True)
			row.label(text="", icon='NONE')
			row = sub.row(align=True)
			row.prop(md, "layers_vcol_select_src", text="")
			row.label(icon='RIGHTARROW')
			row.prop(md, "layers_vcol_select_dst", text="")
			row = sub.row(align=True)
			row.prop(md, "layers_uv_select_src", text="")
			row.label(icon='RIGHTARROW')
			row.prop(md, "layers_uv_select_dst", text="")
			col.prop(md, "islands_precision")

		layout.separator()

		split = layout.split(factor=0.333)
		split.prop(md, "use_poly_data")
		use_poly = md.use_poly_data
		row = split.row()
		row.active = use_poly
		row.prop(md, "poly_mapping", text="")
		if use_poly:
			col = layout.column(align=True)
			split = col.split(factor=0.333, align=True)
			sub = split.column(align=True)
			sub.prop(md, "data_types_polys")

		layout.separator()

		split = layout.split()
		col = split.column()
		row = col.row(align=True)
		sub = row.row(align=True)
		sub.active = md.use_max_distance
		sub.prop(md, "max_distance")
		row.prop(md, "use_max_distance", text="", icon='STYLUS_PRESSURE')

		col = split.column()
		col.prop(md, "ray_radius")

		layout.separator()

		split = layout.split()
		col = split.column()
		col.prop(md, "mix_mode")
		col.prop(md, "mix_factor")

		col = split.column()
		row = col.row()
		row.active = bool(md.object)
		row.operator("object.datalayout_transfer", text="Generate Data Layers")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		sub = row.row(align=True)
		sub.active = bool(md.vertex_group)
		sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

	def NORMAL_EDIT(self, layout, ob, md):
		has_vgroup = bool(md.vertex_group)
		do_polynors_fix = not md.no_polynors_fix
		needs_object_offset = (((md.mode == 'RADIAL') and not md.target) or
							   ((md.mode == 'DIRECTIONAL') and md.use_direction_parallel))

		row = layout.row()
		row.prop(md, "mode", expand=True)

		split = layout.split()

		col = split.column()
		col.prop(md, "target", text="")
		sub = col.column(align=True)
		sub.active = needs_object_offset
		sub.prop(md, "offset")
		row = col.row(align=True)

		col = split.column()
		row = col.row()
		row.active = (md.mode == 'DIRECTIONAL')
		row.prop(md, "use_direction_parallel")

		subcol = col.column(align=True)
		subcol.label(text="Mix Mode:")
		subcol.prop(md, "mix_mode", text="")
		subcol.prop(md, "mix_factor")
		row = subcol.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		sub = row.row(align=True)
		sub.active = has_vgroup
		sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
		row = subcol.row(align=True)
		row.prop(md, "mix_limit")
		row.prop(md, "no_polynors_fix", text="", icon='UNLOCKED' if do_polynors_fix else 'LOCKED')

	def CORRECTIVE_SMOOTH(self, layout, ob, md):
		is_bind = md.is_bind

		layout.prop(md, "factor", text="Factor")
		layout.prop(md, "iterations")
		layout.prop(md, "scale")
		row = layout.row()
		row.prop(md, "smooth_type")

		split = layout.split()

		col = split.column()
		col.label(text="Vertex Group:")
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

		col = split.column()
		col.prop(md, "use_only_smooth")
		col.prop(md, "use_pin_boundary")

		layout.prop(md, "rest_source")
		if md.rest_source == 'BIND':
			layout.operator("object.correctivesmooth_bind", text="Unbind" if is_bind else "Bind")

	def WEIGHTED_NORMAL(self, layout, ob, md):
		layout.label(text="Weighting Mode:")
		split = layout.split(align=True)
		col = split.column(align=True)
		col.prop(md, "mode", text="")
		col.prop(md, "weight", text="Weight")
		col.prop(md, "keep_sharp")

		col = split.column(align=True)
		row = col.row(align=True)
		row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
		row.active = bool(md.vertex_group)
		row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
		col.prop(md, "thresh", text="Threshold")
		col.prop(md, "use_face_influence")

	def MESH_TO_VOLUME(self, layout, ob, md):
		layout.prop(md, "object")

		layout.separator()

		layout.prop(md, "density")
		layout.prop(md, "use_fill_volume")
		layout.prop(md, "exterior_band_width")

		row = layout.row()
		row.active = not md.use_fill_volume
		row.prop(md, "interior_band_width")

		layout.separator()

		row = layout.row()
		row.label(text="Resolution Mode:")
		row.prop(md, "resolution_mode", text="")

		if md.resolution_mode == 'VOXEL_AMOUNT':
			layout.prop(md, "voxel_amount")
		elif md.resolution_mode == 'VOXEL_SIZE':
			layout.prop(md, "voxel_size")

	def VOLUME_DISPLACE(self, layout, ob, md):
		layout.label(text="Texture:")
		layout.template_ID(md, "texture", new="texture.new")

		layout.separator()

		row = layout.row()
		row.label(text="Texture mapping:")
		row.prop(md, "texture_map_mode", text="")

		if md.texture_map_mode == 'OBJECT':
			row = layout.row()
			row.label(text="Object:")
			row.prop(md, "texture_map_object", text="")

		layout.separator()

		layout.prop(md, "strength")
		layout.prop(md, "texture_sample_radius", text="Sample Radius")

		layout.prop(md, "texture_mid_level", text="Mid Level")

	def VOLUME_TO_MESH(self, layout, ob, md):
		layout.prop(md, "object")
		layout.prop(md, "grid_name")

		layout.separator()

		row = layout.row()
		row.label(text="Resolution Mode:")
		row.prop(md, "resolution_mode", text="")

		if md.resolution_mode == 'VOXEL_AMOUNT':
			layout.prop(md, "voxel_amount")
		elif md.resolution_mode == 'VOXEL_SIZE':
			layout.prop(md, "voxel_size")

		layout.separator()

		layout.prop(md, "threshold")
		layout.prop(md, "adaptivity")
		layout.prop(md, "use_smooth_shade")

	def NODES(self, layout, ob, md):
		if md.node_group:
			layout.template_ID(md, "node_group", new="node.new_geometry_node_group_assign")

			layout.label(text = "Geometry Node has no internal panel.") 

			for item in md.node_group.interface.items_tree:
				if item.in_out == "INPUT" and item.name != "Geometry":
					row = layout.row()
					row.label(text = item.name) 
					row.label(text = str(md[item.identifier])) 

			layout.label(text = "Output Attribute") 

			for item in md.node_group.interface.items_tree:
				if item.in_out == "OUTPUT" and item.name != "Geometry":
					row = layout.row()
					row.label(text = item.name) 
		else:
			layout.operator("node.new_geometry_node_group_assign", text = "New Geometry Node")

	def GP_SUBDIV(self, layout, ob, md):
		row = layout.row()
		row.prop(md, "subdivision_type", expand = True)
		layout.prop(md, "level", text = "Levels")

	def GP_LINEART(self, layout, ob, md):
		row = layout.row()
		layout.prop(md, "source_type")
		if md.source_type == "OBJECT":
			row = layout.row()
			if not md.source_object:
				row.alert = True
			row.prop(md, "source_object", text = "Object")
		if md.source_type == 'COLLECTION':
			row = layout.row()
			if not md.source_collection:
				row.alert = True
			row.prop(md, "source_collection", text = "Collection")
			row.prop(md, "use_invert_collectio", text = "")
		row = layout.row()
		if not md.target_layer:
			row.alert = True
		row.prop(md, "target_layer", text = "Layer")
		row = layout.row()
		if not md.target_material:
			row.alert = True
		row.prop(md, "target_material", text = "Material")
		layout.prop(md, "thickness", text = "Thickness")
		layout.prop(md, "opacity", text = "Opacity")
		row = layout.row()
		row.prop(md, "use_contour", text = "")
		row.prop(md, "silhouette_filtering", text = "")
		row = layout.row()
		row.prop(md, "use_crease", text = "")
		row.prop(md, "crease_threshold")
		layout.prop(md, "use_intersection", text = "Intersection")
		layout.prop(md, "use_material", text = "Material")
		layout.prop(md, "use_edge_mark", text = "Edge Mark")
		layout.prop(md, "use_loose", text = "Loose")
		layout.prop(md, "use_light_contour", text = "Light Contour")
		layout.prop(md, "use_shadow", text = "Shadow")
		layout.label(text = "Bake")
		row = layout.row()
		row.operator("object.lineart_bake_strokes")
		row.operator("object.lineart_bake_strokes_all")
		row = layout.row()
		row.operator("object.lineart_clear")
		row.operator("object.lineart_clear_all")
