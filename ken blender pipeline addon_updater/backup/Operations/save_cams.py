import bpy
from bpy.props import *
from bpy.types import PropertyGroup, UIList, Operator, AddonPreferences

def apply_cam_settings(context):

	cam = context.scene.save_cam_collection[obj.save_cam]

def update_index(self, context):
	bpy.ops.savecams.cam_assign(item=context.scene.save_cam_collection_index)

def display_toggle_callback(self, context):
	apply_cam_settings(context)

class SAVECAMS_property_other(PropertyGroup):
	toggle_lens : BoolProperty(default=False,name="Toggle Lens")
	toggle_type : BoolProperty(default=False,name="Toggle Type")
	toggle_resolution : BoolProperty(default=False,name="Toggle resolution")


class property_collection_save_cam(PropertyGroup):
	cindex  : IntProperty(name='Index')
	name    : StringProperty(name="Cam name", default="Cam")
	type : EnumProperty(default="ORTHO",name = "Cam Type",
	items= [
	("ORTHO","Orthographic",""),
	("PERSP","Perspective",""),
	("PANO","Panoramic",""),
	])

	camLocs : FloatVectorProperty(name = "Cam Location")
	camRots : FloatVectorProperty(name="Cam Rotation")
	flen    : FloatProperty(name='Focal Length')
	ortho   : FloatProperty(name='Orthographic Scale')
	res_x   : IntProperty(name='X Resolution')
	res_y   : IntProperty(name='Y Resolution')
	bpy.types.Scene.save_cam_collection_index = IntProperty(
		name = "Cam Scene Index",
		description = "***",
		default = 0,
		min = 0,update=update_index
		)


class SAVECAMS_UL_cam_collection(UIList):
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		props = context.scene.save_cam_other
		cam = item
		row = layout.row(align=True)

		row.label(text="",icon="CAMERA_DATA")
		row.separator()

		reassign = row.operator("savecams.cam_reassign",text="", icon="FILE_REFRESH", emboss=False)
		reassign.item= index

		row.prop(cam, "name", text="", icon_value=icon, emboss=False)
		if props.toggle_type:
			row.prop(cam, "type", text="", icon="NONE", emboss=False)
		if props.toggle_lens:
			if cam.type == "PERSP":
				row.prop(cam, "flen", text="", icon="NONE", emboss=False)
			elif cam.type == "ORTHO":
				row.prop(cam, "ortho", text="", icon="NONE", emboss=False)
		if props.toggle_resolution:
			row.prop(cam, "res_x", text="X", icon="NONE", emboss=False)
			row.prop(cam, "res_y", text="Y", icon="NONE", emboss=False)
			row.separator()

		remove = row.operator("savecams.cam_remove", text="", icon='X', emboss=False)
		remove.item= index

class SAVECAMS_OT_cam_add(Operator):
	bl_idname = "savecams.cam_add"
	bl_label = "Add"
	bl_description = "Add cam"

	def execute(self, context):
		if context.object.type=="CAMERA":
			obj = context.object
		else:
			obj = bpy.context.scene.camera

		item = context.scene.save_cam_collection.add()
		item.name = obj.name + " " + str(len(context.scene.save_cam_collection))
		item.type = obj.data.type
		item.camLocs = obj.location
		item.camRots = obj.rotation_euler
		item.flen = obj.data.lens
		item.ortho = obj.data.ortho_scale
		item.res_x = context.scene.render.resolution_x
		item.res_y = context.scene.render.resolution_y
		context.scene.save_cam_collection_index = len(context.scene.save_cam_collection)-1
		return{'FINISHED'}

class SAVECAMS_OT_cam_remove(Operator):
	bl_idname = "savecams.cam_remove"
	bl_label = "Remove"
	bl_description = "Remove cam"

	item : IntProperty(default=0,name="Item")

	@classmethod
	def poll(cls, context):
		return len(context.scene.save_cam_collection) > 0

	def execute(self, context):
		# index = context.scene.save_cam_collection_index
		index = self.item
		context.scene.save_cam_collection.remove(index)
		for cam in context.scene.save_cam_collection:
			if cam.cindex > index:
				cam.cindex = cam.cindex - 1
		if len(context.scene.save_cam_collection) == index:
			context.scene.save_cam_collection_index = index-1
		else:
			context.scene.save_cam_collection_index = index
		return{'FINISHED'}

class SAVECAMS_OT_cam_assign(Operator):
	bl_idname = "savecams.cam_assign"
	bl_label = "Assign"
	bl_description = "Assign cam"

	item : IntProperty(default=0,name="Item")

	@classmethod
	def poll(cls, context):
		return len(context.scene.save_cam_collection) > 0

	def execute(self, context):
		if context.object.type=="CAMERA":
			cam = context.object
		else:
			cam = bpy.context.scene.camera

		item = context.scene.save_cam_collection[self.item]
		cam.data.type = item.type
		cam.location = item.camLocs
		cam.rotation_euler = item.camRots
		cam.data.lens = item.flen
		cam.data.ortho_scale = item.ortho
		context.scene.render.resolution_x = item.res_x
		context.scene.render.resolution_y = item.res_y
		return{'FINISHED'}

class SAVECAMS_OT_cam_reassign(Operator):
	bl_idname = "savecams.cam_reassign"
	bl_label = "Reassign"
	bl_description = "Reassign selected cam"

	item : IntProperty(default=0,name="Item")

	@classmethod
	def poll(cls, context):
		return len(context.scene.save_cam_collection) > 0

	def execute(self, context):
		if context.object.type=="CAMERA":
			cam = context.object
		else:
			cam = bpy.context.scene.camera

		item = context.scene.save_cam_collection[self.item]
		item.camLocs = cam.location
		item.camRots = cam.rotation_euler
		item.flen = cam.data.lens
		item.ortho = cam.data.ortho_scale
		item.res_x = context.scene.render.resolution_x
		item.res_y = context.scene.render.resolution_y
		self.report({'INFO'}, "Updated by current camera")
		return{'FINISHED'}

class SAVECAMS_OT_cam_add_from_view(Operator):
	bl_idname = "savecams.add_from_view"
	bl_label = "Add from View"
	bl_description = "Add selected cam from view"

	@classmethod
	def poll(cls, context):
		for area in bpy.context.screen.areas:
			if area.type == 'VIEW_3D':
				return  area.spaces[0].region_3d.view_perspective != 'CAMERA'

	def execute(self, context):
		bpy.ops.view3d.camera_to_view()
		bpy.ops.savecams.cam_add()
		return{'FINISHED'}

class SAVECAMS_OT_cam_cycle_up(Operator):
	bl_idname = "savecams.list_up"
	bl_label = "Cycle Up"
	bl_description = "Cycle up through cam views"

	@classmethod
	def poll(cls, context):
		return len(context.scene.save_cam_collection) > 0

	def execute(self, context):
		if context.scene.save_cam_collection_index == 0:
			context.scene.save_cam_collection_index = len(context.scene.save_cam_collection) - 1
		else:
			context.scene.save_cam_collection_index -= 1
		bpy.ops.savecams.cam_assign(item=context.scene.save_cam_collection_index)
		return{'FINISHED'}

class SAVECAMS_OT_cam_cycle_down(Operator):
	bl_idname = "savecams.list_down"
	bl_label = "Cycle Down"
	bl_description = "Cycle down through cam views"

	@classmethod
	def poll(cls, context):
		return len(context.scene.save_cam_collection) > 0

	def execute(self, context):
		if context.scene.save_cam_collection_index == len(context.scene.save_cam_collection) - 1:
			context.scene.save_cam_collection_index = 0
		else:
			context.scene.save_cam_collection_index += 1
		bpy.ops.savecams.cam_assign(item=context.scene.save_cam_collection_index)
		return{'FINISHED'}



classes = (
		SAVECAMS_OT_cam_add_from_view,
		SAVECAMS_OT_cam_add,
		SAVECAMS_OT_cam_assign,
		SAVECAMS_OT_cam_cycle_down,
		SAVECAMS_OT_cam_cycle_up,
		SAVECAMS_OT_cam_reassign,
		SAVECAMS_OT_cam_remove,
		property_collection_save_cam,
		SAVECAMS_property_other,
		SAVECAMS_UL_cam_collection,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.save_cam_other = bpy.props.PointerProperty(type=SAVECAMS_property_other)
    bpy.types.Scene.save_cam_collection = \
		bpy.props.CollectionProperty(type=property_collection_save_cam)
	# Old Class Name : property_collection_save_cam

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.save_cam_other
    del bpy.types.Scene.save_cam_collection

if __name__ == "__main__":
	register()
