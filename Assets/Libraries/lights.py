import bpy

class Lights_List_Remove(bpy.types.Operator):
	bl_idname = "lights.remove_list"
	bl_label = "Lights Remove in List"
	bl_options = {'REGISTER', 'UNDO'}

	light: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		obj = bpy.data.objects.get(self.light)
			# Remove the object from the scene
		bpy.data.objects.remove(obj, do_unlink=True)
		self.report({"INFO"}, self.light + " has been removed.")
		return {"FINISHED"}

class Lights_Set_Power(bpy.types.Operator):
	bl_idname = "lights.set_power"
	bl_label = "Lights Remove in List"
	bl_options = {'REGISTER', 'UNDO'}

	light: bpy.props.StringProperty(options={'HIDDEN'})
	power: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		light = bpy.data.lights[self.light]
		if self.power == "+1":
			power = light.energy
			light.energy = power*2
		if self.power == "+0.5":
			power = light.energy
			light.energy = power*1.41421
		if self.power == "-1":
			power = light.energy
			light.energy = power*0.5
		if self.power == "-0.5":
			power = light.energy
			light.energy = power/1.41421

		self.report({"INFO"}, self.light + " Power Set " + self.power)
		return {"FINISHED"}

class Solo_Light(bpy.types.Operator):
    bl_idname = "lights.solo"
    bl_label = "Set Light Solo"
    bl_options = {'REGISTER', 'UNDO'}

    light: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        light = self.light
        list = []

        list.append(light)

        obj = bpy.data.objects[light]
        if obj.hide_viewport == True:
            obj.hide_viewport = False
        else:
            for light_data in bpy.data.objects:
                obj = bpy.data.objects[light_data.name]
                if obj.type == 'LIGHT':
                    if obj.name not in list:
                        obj.hide_viewport = True
                    else:
                        obj.hide_viewport = False

        return {"FINISHED"}

class LIGHT(bpy.types.UIList):
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
		lights = obj.data
		# draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
		if self.layout_type in {'DEFAULT'}:
			# You should always start your row layout by a label (icon + text), or a non-embossed text field,
			# this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
			# We use icon_value of label, as our given icon is an integer value, not an enum ID.
			# Note "data" names should never be translated!
			col = layout.column(align=False)
			row = col.row()

			# Adjust the height of each row using the "split" method
			row.prop(lights, "type", text="", icon="LIGHT_%s" % lights.type, icon_only=True)
			row.prop(obj, "name", text="", emboss=False)
			row.prop(lights, "color", text = "")
			row.prop(lights, "energy", text = "")

			main_col = row.column(align=False)
			intensity_row = main_col.row(align=True)
			exp_col = intensity_row.column(align=True)
			exp_col.scale_y = 0.5
			a1 = exp_col.operator("lights.set_power", text='', icon='TRIA_UP')
			a1.light = lights.name
			a1.power = "+0.5"
			s1 = exp_col.operator("lights.set_power", text='', icon='TRIA_DOWN')
			s1.light = lights.name
			s1.power = "-0.5"
			for obj in context.scene.objects:
				if obj.type == 'LIGHT' and obj.data.name == lights.name:
					row.operator("lights.solo", icon = "EVENT_S", text= "", emboss=False).light =obj.name
					if obj in context.selected_objects or obj == context.object:
						selecticon = "RESTRICT_SELECT_OFF"
					else:
						selecticon = "RESTRICT_SELECT_ON"
					if obj.hide_viewport == False:
						row.operator("object.set_select", text = "", icon = selecticon, emboss=False).object = obj.name
					row.prop(obj, "hide_viewport", text = "", icon = "HIDE_OFF", emboss=False)

			row.operator("lights.remove_list", text = "", icon = "X", emboss=False).light = lights.name

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

		filtered_items = [o for o in bpy.context.scene.objects if o.type=='LIGHT']

		for i, item in enumerate(items):
			if not item in filtered_items:
				filtered[i] &= ~self.bitflag_filter_item

		return filtered,ordered

def draw_lights(self, context, box):
	scene = context.scene
	obj = context.object
	row = box.row()
	row.label(text = "Lights Mixer", icon = "LIGHT_DATA")

	try:

		lights = bpy.data.objects[scene.light_index]
		row.operator("object.duplicate_list", text = "", icon = "DUPLICATE", emboss=False).object = lights.name

		if scene.hide == True:
			hideicon = "HIDE_ON"
		else:
			hideicon = "HIDE_OFF"
		if scene.hide == False:
			row.operator("object.select_by_type", text = "", icon = "RESTRICT_SELECT_OFF", emboss=False).type = "LIGHT"
		row.prop(scene, "hide", text = "", icon = hideicon, emboss=False)
		row.operator("object.remove_all_by_type", text = "", icon = "X", emboss=False).type = "LIGHT"
		box.template_list("LIGHT", "", bpy.data, "objects", scene, "light_index")

		row = box.row()
		row.prop(scene, "light_type", icon = "RESTRICT_SELECT_OFF", text = "")
		if scene.light_type == True:
			if obj.type == 'LIGHT':
				text = "Selected Object Light Data"
				lights = obj
			else:
				text = "Selected List Light Data"
				lights = lights
		else:
			text = "List Light Data"
			lights = lights
		row.label(text = text)
		draw_light_data(box, lights.data)
		if scene.render.engine in ["CYCLES"]:
			row = box.row()
			row.label(text = "Shading Linking", icon = "LINKED")
			light_linking_box = box.box()

			view_layer = context.view_layer
			row = light_linking_box.row(align=True)
			row.use_property_decorate = False

			sub = row.column(align=True)
			sub.prop_search(lights, "lightgroup", view_layer, "lightgroups", text="Light Group", results_are_suggestions=True)

			sub = row.column(align=True)
			sub.enabled = bool(lights.lightgroup) and not any(lg.name == lights.lightgroup for lg in view_layer.lightgroups)
			sub.operator("scene.view_layer_add_lightgroup", icon='ADD', text="").name = lights.lightgroup
			
			draw_light_linking(scene, light_linking_box, lights)
	except:
		box.label(text = "No Selected Light")

	draw_world(context, box)

def draw_light_data(box, light):
	lightbox = box.box()
	row = lightbox.row()
	row.prop(light, "type", expand = True)
	lightbox.prop(light, "color", text = "Color")
	lightbox.prop(light, "energy", text = "Power")
	row = lightbox.row(align = True)
	s1 = row.operator("lights.set_power", text = "-1")
	s1.light = light.name
	s1.power = "-1"
	s05 = row.operator("lights.set_power", text = "-0.5")
	s05.light = light.name
	s05.power = "-0.5"
	a05 = row.operator("lights.set_power", text = "+0.5")
	a05.light = light.name
	a05.power = "+0.5"
	a1 = row.operator("lights.set_power", text = "+1")
	a1.light = light.name
	a1.power = "+1"
	row = lightbox.row()
	if light.type == "POINT":
		lightbox.prop(light, "shadow_soft_size", text = "Size")
	if light.type == "SPOT":
		lightbox.prop(light, "shadow_soft_size", text = "Size")
		lightbox.label(text = "Beam Shape")
		lightbox.prop(light, "spot_size", text = "Size")
		lightbox.prop(light, "spot_blend", text = "Blend")
	if light.type == "SUN":
		lightbox.prop(light, "angle", text = "Angle")
	if light.type == "AREA":
		lightbox.prop(light, "shape")
		if light.shape == "SQUARE" or light.shape == "DISK":
			lightbox.prop(light, "size", text = "Size")
		if light.shape == "RECTANGLE" or light.shape == "ELLIPSE": 
			lightbox.prop(light, "size", text = "Size X")
			lightbox.prop(light, "size_y", text = "Size Y")
		lightbox.prop(light, "spread", text = "Spread")
	if bpy.context.scene.render.engine == 'CYCLES':
		lightbox.prop(light, "use_shadow", text = "Shadow")

def draw_light_linking(scene, box, obj):
	light_linking = obj.light_linking
	if scene.light_linking == True:
			icon = "DOWNARROW_HLT"
	else:
		icon = "RIGHTARROW"
	box.prop(scene, "light_linking", text = "Light Linking", icon = icon, emboss=False)
	if scene.light_linking == True:
		light_linking_box = box.box()

		col = light_linking_box.column()

		col.template_ID(
			light_linking,
			"receiver_collection",
			new="object.light_linking_receiver_collection_new")

		if light_linking.receiver_collection:

			row = light_linking_box.row()
			col = row.column()
			col.template_light_linking_collection(row, light_linking, "receiver_collection")

			col = row.column()
			sub = col.column(align=True)
			prop = sub.operator("object.light_linking_receivers_link", icon='ADD', text="")
			prop.link_state = 'INCLUDE'
			sub.operator("object.light_linking_unlink_from_collection", icon='REMOVE', text="")
			sub = col.column()
			sub.menu("CYCLES_OBJECT_MT_light_linking_context_menu", icon='DOWNARROW_HLT', text="")

	if scene.shadow_linking == True:
			icon = "DOWNARROW_HLT"
	else:
		icon = "RIGHTARROW"
	box.prop(scene, "shadow_linking", text = "Shadow Linking", icon = icon, emboss=False)
	if scene.shadow_linking == True:
		shadow_linking_box = box.box()

		col = shadow_linking_box.column()

		col.template_ID(
			light_linking,
			"blocker_collection",
			new="object.light_linking_blocker_collection_new")

		if light_linking.blocker_collection:

			row = shadow_linking_box.row()
			col = row.column()
			col.template_light_linking_collection(row, light_linking, "blocker_collection")

			col = row.column()
			sub = col.column(align=True)
			prop = sub.operator("object.light_linking_blockers_link", icon='ADD', text="")
			prop.link_state = 'INCLUDE'
			sub.operator("object.light_linking_unlink_from_collection", icon='REMOVE', text="")
			sub = col.column()
			sub.menu("CYCLES_OBJECT_MT_shadow_linking_context_menu", icon='DOWNARROW_HLT', text="")

def draw_world(context, box):
	scene = context.scene
	box.label(text = "World Data", icon = "WORLD")
	box = box.box()
	box.template_ID(scene, "world", new="world.new")
	world = context.scene.world

	box.prop(world, "use_nodes", icon='NODETREE')
	box.separator()

	box.use_property_split = True

	if world.use_nodes:
		ntree = world.node_tree
		node = ntree.get_output_node('EEVEE')

		if node:
			input = find_node_input(node, "Surface")
			if input:
				box.template_node_view(ntree, node, input)
			else:
				box.label(text="Incompatible output node")
		else:
			box.label(text="No output node")
	else:
		box.prop(world, "color")

def find_node_input(node, input_name):
	for input in node.inputs:
		if input.name == input_name:
			return input
	return None

bpy.types.Scene.light_type = bpy.props.BoolProperty(
	name="Light Data Type",
	description="Light Data Type",
	default=False,
)         
bpy.types.Scene.light_group = bpy.props.BoolProperty(
	name="Light Group",
	description="Light Group",
)

bpy.types.Scene.light_linking = bpy.props.BoolProperty(
	name="Light Linking",
	description="Light Linking",
)

bpy.types.Scene.shadow_linking = bpy.props.BoolProperty(
	name="Shadow Linking",
	description="Shadow Linking",
)

bpy.types.Scene.light_index = bpy.props.IntProperty(
	name="light_index",
	description="light_index",
	default=2,
)

classes = (
			Lights_List_Remove,
			Lights_Set_Power,
			Solo_Light,
			LIGHT,
		  )

def register(): 
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
  
def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)