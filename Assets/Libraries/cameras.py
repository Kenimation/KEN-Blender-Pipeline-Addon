import bpy
from .. import assetsDefs

class Cameras_List_Remove(bpy.types.Operator):
	bl_idname = "cameras.remove_list"
	bl_label = "Cameras Remove in List"
	bl_options = {'REGISTER', 'UNDO'}

	cam: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		obj = bpy.data.objects.get(self.cam)
			# Remove the object from the scene
		bpy.data.objects.remove(obj, do_unlink=True)
		context.scene.cam_index = context.scene.cam_index - 1
		self.report({"INFO"}, self.cam + " has been removed.")
		return {"FINISHED"}
	
class Cameras_Set_View(bpy.types.Operator):
	bl_idname = "cameras.set_view"
	bl_label = "Set Local Camera"
	bl_options = {'REGISTER', 'UNDO'}

	cam: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		context.scene.camera = bpy.data.objects[self.cam]
		self.report({"INFO"}, "Local Camera Set" + self.cam)
		return {"FINISHED"}

class CAMERAS(bpy.types.UIList):
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
		obj = bpy.data.objects[item.name]
		cam = obj.data
		# draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			# You should always start your row layout by a label (icon + text), or a non-embossed text field,
			# this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
			# We use icon_value of label, as our given icon is an integer value, not an enum ID.
			# Note "data" names should never be translated!

			if context.scene.camera == bpy.data.objects[item.name]:
				view = "RESTRICT_RENDER_OFF"
			else:
				view = "RESTRICT_RENDER_ON"
			layout.operator("cameras.set_view", text = "", icon = view, emboss=False).cam = obj.name

			layout.prop(obj, "name", text="", emboss=False, icon= "CAMERA_DATA")

			if obj in context.selected_objects or obj == context.object:
				selecticon = "RESTRICT_SELECT_OFF"
			else:
				selecticon = "RESTRICT_SELECT_ON"
			layout.operator("object.set_select", text = "", icon = selecticon, emboss=False).object = obj.name
			layout.operator("cameras.remove_list", text = "", icon = "X", emboss=False).cam = obj.name
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

		filtered_items = [o for o in bpy.context.scene.objects if o.type=='CAMERA']

		for i, item in enumerate(items):
			if not item in filtered_items:
				filtered[i] &= ~self.bitflag_filter_item

		return filtered,ordered

def draw_cams(self, context, box):
	scene = context.scene
	row = box.row()
	row.label(text = "Cameras Manager", icon = "CAMERA_DATA")
	row.operator("object.select_by_type", text = "", icon = "RESTRICT_SELECT_OFF", emboss=False).type = "CAMERA"

	cam = bpy.data.objects[scene.cam_index]
	row.operator("object.duplicate_list", text = "", icon = "DUPLICATE", emboss=False).object = cam.name

	row = box.row()
	row.template_list("CAMERAS", "", bpy.data, "objects", scene, "cam_index")

	if cam and cam.type == 'CAMERA':
		if scene.cam_quick == True:
			icon = "DOWNARROW_HLT"
		else:
			icon = "RIGHTARROW"
		box.prop(scene, "cam_quick", text = "Quick Camera", icon = icon, emboss=False)
		if scene.cam_quick == True:
			type = "list"
			cambox = box.box()
			draw_cam_data(context, cambox, cam, type)
			
		if scene.cam_shake == True:
			icon = "DOWNARROW_HLT"
		else:
			icon = "RIGHTARROW"
		box.prop(scene, "cam_shake", text = "Camera Shakify", icon = icon, emboss=False)
		if scene.cam_shake == True:
			draw_cam_shake(box, cam)

		if scene.cam_save == True:
			icon = "DOWNARROW_HLT"
		else:
			icon = "RIGHTARROW"
		box.prop(scene, "cam_save", text = "Camera Save List", icon = icon, emboss=False)
		if scene.cam_save == True:
			draw_save_cam(context, box)
	else:
		box.label(text = "No Selected Camera")

def draw_cam_data(context, box, cam, type):
	cam = cam.data
	box.prop(cam, "name", text = "")
	row = box.row()
	row.prop(cam, "clip_start", text = "Clip Start")
	row.prop(cam, "clip_end", text = "Clip End")
	row = box.row()
	row.prop(cam, "type", text = "Type")
	if cam.type == "PERSP":
		box.prop(cam, "lens", text = "Focal Length")
	elif cam.type == "ORTHO":
		box.prop(cam, "ortho_scale", text = "Orthographic Scale")
	elif cam.type == "PANO":
		if context.scene.render.engine in ["CYCLES"]:
			row.prop(cam.cycles, "panorama_type", text = "")
			if cam.cycles.panorama_type == 'FISHEYE_LENS_POLYNOMIAL':
				box.prop(cam.cycles, "fisheye_fov", text = "Field of View")
				box.prop(cam.cycles, "fisheye_polynomial_k0", text = "K0")
				box.prop(cam.cycles, "fisheye_polynomial_k1", text = "K1")
				box.prop(cam.cycles, "fisheye_polynomial_k2", text = "K2")
				box.prop(cam.cycles, "fisheye_polynomial_k3", text = "K3")
				box.prop(cam.cycles, "fisheye_polynomial_k4", text = "K4")

	box.prop(cam, "sensor_width", text = "Size")
	box.label(text = "Depth of Field")
	box.prop(cam.dof, "use_dof", text = "Depth of Field", toggle = True)
	if cam.dof.use_dof == True:
		box.prop(cam.dof, "focus_object", text = "Focus Object")
		if cam.dof.focus_object:
			if cam.dof.focus_object.type == 'ARMATURE':
				box.prop(cam.dof, "focus_subtarget", text = "Focus Bone")
		box.prop(cam.dof, "focus_distance", text = "Distance")
		if type == "obj":
			text = "Show Focus Plane" if context.scene.cam == False else "Hide Focus Plane"
			icon = "NORMALS_FACE" if context.scene.cam == False else "CANCEL"
			box.prop(context.scene, "cam", text = text, toggle = True, icon = icon)
		elif type == "list":
			text = "Show Focus Plane" if context.scene.cam == False else "Hide Focus Plane"
			icon = "NORMALS_FACE" if context.scene.cam == False else "CANCEL"
			box.prop(context.scene, "camlist", text = text, toggle = True, icon = icon)
		box.prop(cam.dof, "aperture_fstop", text = "F-Stop")
		box.prop(cam.dof, "aperture_blades", text = "Blades")
		box.prop(cam.dof, "aperture_rotation", text = "Rotation")
		box.prop(cam.dof, "aperture_ratio", text = "Ratio")
	box.label(text = "Viewport Display")
	box.prop(cam, "show_composition_thirds", text = "Thirds", toggle = True)
	box.prop(cam, "passepartout_alpha", text = "Passepartout")

def draw_save_cam(context, box):
	props = context.scene.save_cam_other

	row = box.row(align=True)
	rows = row.row(align=True)
	rows.scale_x = 1.2
	rows.operator("savecams.cam_add", icon='ADD', text="")
	row.separator()
	row.operator("savecams.add_from_view", icon = "ZOOM_IN", text = "")

	row.label(text="Name",icon="NONE")

	row.prop(props,"toggle_type",text="Type")
	row.prop(props,"toggle_lens",text="Lens")
	row.prop(props,"toggle_resolution",text="Reso")

	row = box.row()
	col = row.column()
	col.template_list("SAVECAMS_UL_cam_collection", "", context.scene, "save_cam_collection", context.scene, "save_cam_collection_index")

	col = row.column()

	sub = col.column(align=True)
	sub.operator("savecams.list_up", icon="TRIA_UP", text='')
	sub.operator("savecams.list_down", icon="TRIA_DOWN", text='')

def draw_cam_shake(box, cam):
	row = box.row()
	row.template_list(
		listtype_name="OBJECT_UL_camera_shake_items",
		list_id="Camera Shakes",
		dataptr=cam,
		propname="camera_shakes",
		active_dataptr=cam,
		active_propname="camera_shakes_active_index",
	)
	col = row.column()
	col.operator("object.camera_shake_add", text="", icon='ADD').camera = cam.name
	col.operator("object.camera_shake_remove", text="", icon='REMOVE').camera = cam.name
	if len(cam.camera_shakes) > 1:
		cam_shake_up = col.operator("object.camera_shake_move", text="", icon='TRIA_UP')
		cam_shake_up.camera = cam.name
		cam_shake_up.type = 'UP'
		cam_shake_down = col.operator("object.camera_shake_move", text="", icon='TRIA_DOWN')
		cam_shake_down.camera = cam.name
		cam_shake_down.type = 'DOWN'

	row = box.row()
	row.operator("object.camera_shakes_fix_global")
	if cam.camera_shakes_active_index < len(cam.camera_shakes):
		shake = cam.camera_shakes[cam.camera_shakes_active_index]
		row = box.row()
		row.prop(shake, "shake_type", text="")
		row = box.row()
		row.prop(shake, "influence", slider=True)
		row = box.row()
		row.prop(shake, "scale")
		row = box.row()
		row.prop(shake, "use_manual_timing")
		if shake.use_manual_timing:
			row = box.row()
			row.prop(shake, "time")
		else:
			row = box.row()
			row.prop(shake, "speed")
			row = box.row()
			row.prop(shake, "offset")

bpy.types.Scene.cam_save = bpy.props.BoolProperty(
	name="Enable Camera Save List",
	description="Enable Camera Save List",
	default= True
)
bpy.types.Scene.cam_shake = bpy.props.BoolProperty(
	name="Enable Camera Shakify",
	description="Enable Camera Shakify",
	default= True
)
bpy.types.Scene.cam_quick = bpy.props.BoolProperty(
	name="Enable Quick Camera",
	description="Enable Quick Camera",
	default= True
)
bpy.types.Scene.cam_index = bpy.props.IntProperty(
	name="camera_index",
	description="camera_index",
)
bpy.types.Scene.cam = bpy.props.BoolProperty(
	name="Cam Focus",
	default=False,
	update = assetsDefs.update_cam_focus
)
bpy.types.Scene.camlist = bpy.props.BoolProperty(
	name="Cam Focus List",
	default=False,
	update = assetsDefs.update_cam_focus_list
)

classes = (
			Cameras_List_Remove,
			Cameras_Set_View,
			CAMERAS,
		  )

def register(): 
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
  
def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)