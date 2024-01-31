import bpy
import os
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, OperatorFileListElement
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty
from .. import assetsDefs

class Images_List_Remove(bpy.types.Operator):
	bl_idname = "images.remove_list"
	bl_label = "Images Remove in List"
	bl_options = {'REGISTER', 'UNDO'}

	img: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		img_data = bpy.data.images[self.img]
		if img_data.packed_files:
			img_data.unpack(method='USE_ORIGINAL')
		bpy.data.images.remove(img_data)
		context.scene.image_index = context.scene.image_index - 1
		self.report({"INFO"}, "Image has been removed.")
		return {"FINISHED"}

class Images_List_Pack(bpy.types.Operator):
	bl_idname = "images.pack_list"
	bl_label = "Images Pack in List"
	bl_options = {'REGISTER', 'UNDO'}

	img: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		img_data = bpy.data.images[self.img]
		if img_data.packed_files:
			img_data.unpack(method='USE_ORIGINAL')
			self.report({"INFO"}, "Image has been unpacked.")
		else:
			img_data.pack()
			self.report({"INFO"}, "Image has been packed.")
		return {"FINISHED"}

class Images_Reload_All(bpy.types.Operator):
	bl_idname = "images.reload_all"
	bl_label = "Reload All Images"
	bl_options = {'REGISTER', 'UNDO'}

	img: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		for img in bpy.data.images:
			img.reload
		self.report({"INFO"}, "Reload all images.")
		return {"FINISHED"}


class IMAGES(bpy.types.UIList):
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
		img = item

		# draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
		if self.layout_type in {'DEFAULT'}:
			# You should always start your row layout by a label (icon + text), or a non-embossed text field,
			# this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
			# We use icon_value of label, as our given icon is an integer value, not an enum ID.
			# Note "data" names should never be translated!

			layout.prop(img, "name", text="", emboss=False, icon_value=icon)

			if item.source == 'MOVIE':
				layout.label(text="",icon="FILE_MOVIE")
			elif item.source == 'SEQUENCE':
				layout.label(text="",icon="RENDERLAYERS")
				
			row = layout.row()
			row.scale_x = 0.2
			row.label(text = str(img.users))

			if img.packed_files:
				packicon = "PACKAGE"
			else:
				packicon = "UGLYPACKAGE"

			layout.operator("images.pack_list", text="", icon = packicon, emboss=False).img = str(img.name)
			layout.operator("image.reload", text = "", icon = "FILE_REFRESH", emboss=False)
			if not img.has_data:
				layout.label(text="", icon="ERROR")
			else:
				layout.prop(img,"use_fake_user", text = "", emboss=False)
			if img.use_fake_user == False:
				layout.operator("images.remove_list", text = "", icon = "X", emboss=False).img = str(img.name)
		# 'GRID' layout type should be as compact as possible (typically a single icon!).
		elif self.layout_type == 'GRID':
			layout.alignment = 'CENTER'
			layout.label(text="", icon_value=icon)
		return

	def filter_items(self,context,data,propname):
		filtered = []
		ordered = []
		items = getattr(data, propname)
		helper_funcs = bpy.types.UI_UL_list

		filtered = [self.bitflag_filter_item] * len(items)

		ordered = helper_funcs.sort_items_by_name(items, "name")

		filtered_items = [o for o in bpy.data.images if o.name !='Render Result' and o.name != 'Viewer Node']

		for i, item in enumerate(items):
			if not item in filtered_items:
				filtered[i] &= ~self.bitflag_filter_item

		return filtered,ordered

def draw_images(scene, box):
	row = box.row()
	imgnum = len(bpy.data.images)-2
	row.scale_x = 1.75
	if scene.imagepreview == True:
		previewicon = "SEQ_PREVIEW"
	else:
		previewicon = "SEQ_SPLITVIEW"
	row.prop(scene, "imagepreview", icon = previewicon, text = "", emboss=False)
	row.label(text = "Image Resources: Total "+str(imgnum))
	img_data = bpy.data.images[scene.image_index]
	row.operator("image.open", icon = "FILE_NEW", text = "", emboss=False)
	if scene.img_fake_use == True:
		icon = "FAKE_USER_ON"
	else:
		icon = "FAKE_USER_OFF"
	row.operator("images.reload_all", text = "", icon = "FILE_REFRESH", emboss = False)
	row.prop(scene, "img_fake_use", text = "", icon = icon, emboss = False)
	row.scale_x = 0.75
	row.operator("images.clean_resources", icon = "BRUSH_DATA", text = "Clean")
	 
	if scene.imagepreview == True:
		row = box.row()
		size = f"{img_data.size[0]} x {img_data.size[1]}"
		row.label(text=f"Image Size: {size}")
		row = box.row()
		row.template_icon(icon_value=img_data.preview.icon_id,scale=5)
	row = box.row()
	row.template_list("IMAGES", "", bpy.data, "images", scene, "image_index")
	row = box.row()

	row.prop(img_data, "filepath", text="", icon_value=img_data.preview.icon_id)

	row.scale_x = 0.05
	row.label(text = str(img_data.users))

	row.scale_x = 1
	if img_data.packed_files:
		packicon = "PACKAGE"
	else:
		packicon = "UGLYPACKAGE"
	row.operator("images.pack_list", text="", icon = packicon, emboss=False).img = str(img_data.name)

	row.operator("image.reload", text = "", icon = "FILE_REFRESH", emboss=False)
	row.prop(img_data,"use_fake_user", text = "", emboss=False)
	row.operator("images.remove_list", text = "", icon = "X", emboss=False).img = str(img_data.name)
	row = box.row()
	row.prop(img_data, "source", text = "")
	row.prop(img_data.colorspace_settings, "name", text = "")

bpy.types.Scene.img_fake_use = bpy.props.BoolProperty(
	name="Toggle Images Fake_User",
	description="Toggle Images Fake_User",
	update = assetsDefs.update_img_fake_use
)
bpy.types.Scene.image_index = bpy.props.IntProperty(
	name="Image_index",
	description="image_index",
)
bpy.types.Scene.imagepreview = bpy.props.BoolProperty(
	name="Show Image Preview",
	default=True,
)

classes = (
			Images_List_Remove,
			Images_List_Pack,
			Images_Reload_All,
			IMAGES,
		  )

def register(): 
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
  
def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)