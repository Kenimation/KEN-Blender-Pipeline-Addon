import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty

n_map_node_loc= (-1100,-350)
n_node_loc = (-800,-350)
ramp_node_h_loc = (-650,-125)
h_node_loc = (-200,-250)
tex_node_loc = (-1100, 350)

def prep_material(mat):
	node_tree = mat.node_tree
	for node in node_tree.nodes:
		if node.type == "BSDF_PRINCIPLED":
			node.subsurface_method = 'BURLEY'
		if node.type == "TEX_IMAGE":
			node.interpolation = 'Closest'
			node_tree.links.new(node_tree.nodes["Principled BSDF"].inputs['Alpha'], node_tree.nodes["Image Texture"].outputs['Alpha'])
	mat.blend_method = 'HASHED'

def prep_SSS(mat, type):
	if type == 1:
		node_tree = mat.node_tree
		num = len(node_tree.nodes)
		for number in range(num):
			if number == 0:
				bsdf = node_tree.nodes["Principled BSDF"]
				bsdf.subsurface_method = 'BURLEY'
				bsdf.inputs[7].default_value = 1
				if node_tree.nodes.get("Image Texture", None):
					i_node_get = node_tree.nodes.get("Image Texture", None)
					i_node = node_tree.nodes["Image Texture"]
					node_tree.links.new(bsdf.inputs[0], i_node.outputs['Color'])
			else:
				try:
					id = str(number)
					node_tree.nodes["Principled BSDF.00"+id].subsurface_method = 'BURLEY'
					node_tree.nodes["Principled BSDF.00"+id].inputs[7].default_value = 1
					if node_tree.nodes.get("Image Texture.00"+id, None):
						i_node_get = node_tree.nodes.get("Image Texture.00"+id, None)
						i_node = node_tree.nodes["Image Texture.00"+id]
						if i_node_get is not None:
							node_tree.links.new(node_tree.nodes["Principled BSDF.00"+id].inputs[0], i_node.outputs['Color'])
				except:
					print("No More Tex Node Found!!!")

	if type == 0:
		node_tree = mat.node_tree
		num = len(node_tree.nodes)
		for number in range(num):
			if number == 0:
				if node_tree.name == "Principled BSDF":
					bsdf = node_tree.nodes["Principled BSDF"]
					bsdf.inputs[7].default_value = 0
			else:
				try: 
					id = str(number)
					if node_tree.name == "Principled BSDF.00"+id:
						bsdf = node_tree.nodes["Principled BSDF.00"+id]
						bsdf.inputs[7].default_value = 0
				except:
					print("No More Tex Node Found!!!")

def prep_normal(mat):
	node_tree = mat.node_tree
	bsdf = node_tree.nodes["Principled BSDF"]
	try:
		matname = node_tree.nodes["Image Texture"].image.filepath
		str_1 = str(matname)
		str_list = list(str_1)
		nPos = str_list.index('.')
		str_list.insert(nPos, '_n')
		n_path = "".join(str_list)
		n_image = bpy.data.images.load(filepath=n_path, check_existing=True)
		n_map_node = node_tree.nodes.get("Normal Map Node", None)
		get_node_h = node_tree.nodes.get("Bump Map", None)

		if n_map_node is None:
			filename = node_tree.nodes["Image Texture"].image.name
			n_name = (filename.replace('.png', '') + "_n.png")
			n_map_node = node_tree.nodes.new('ShaderNodeTexImage')
			n_map_node.interpolation = 'Closest'
			n_map_node.name = "Normal Map Node"
			n_map_node.location = n_map_node_loc
			n_map_node.image = n_image
			bpy.data.images[n_name].colorspace_settings.name = 'Non-Color'
			n_node = node_tree.nodes.new('ShaderNodeNormalMap')
			n_node.name = "Normal Map"
			n_node.location = n_node_loc
			node_tree.links.new(n_node.inputs['Color'], n_map_node.outputs['Color'])
			if get_node_h is not None:
				h_node = node_tree.nodes["Bump Map"]
				node_tree.links.new(h_node.inputs['Normal'], n_node.outputs['Normal'])
				node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])
			else:
				node_tree.links.new(bsdf.inputs['Normal'], n_node.outputs['Normal'])
		else:
			n_node = node_tree.nodes["Normal Map"]
			if get_node_h is not None:
				h_node = node_tree.nodes["Bump Map"]
				node_tree.links.new(h_node.inputs['Normal'], n_node.outputs['Normal'])
				node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])
			else:
				node_tree.links.new(bsdf.inputs['Normal'], n_node.outputs['Normal'])
	except:
		print("Image Texture has no found")

def prep_Ramp(mat):
	node_tree = mat.node_tree
	bsdf = node_tree.nodes["Principled BSDF"]
	image_node = node_tree.nodes["Image Texture"]
	getramp_node_i = node_tree.nodes.get("Image Texture", None)
	getramp_node_s = node_tree.nodes.get("ColorRamp_Specular", None)
	getramp_node_r = node_tree.nodes.get("ColorRamp_Roughness", None)
	if getramp_node_i is not None:
		if getramp_node_s is None:
			ramp_node_s = node_tree.nodes.new('ShaderNodeValToRGB')
			ramp_node_s.location = (-400, 175)
			ramp_node_s.name = "ColorRamp_Specular"
			node_tree.links.new(ramp_node_s.inputs['Fac'], image_node.outputs['Color'])
			node_tree.links.new(bsdf.inputs[12], ramp_node_s.outputs['Color'])
		if getramp_node_r is None:
			ramp_node_r = node_tree.nodes.new('ShaderNodeValToRGB')
			ramp_node_r.location = (-400,-25)
			ramp_node_r.color_ramp.elements[0].color = (1, 1, 1, 1)
			ramp_node_r.color_ramp.elements[1].color = (0, 0, 0, 1)
			ramp_node_r.name = "ColorRamp_Roughness"
			node_tree.links.new(ramp_node_r.inputs['Fac'], image_node.outputs['Color'])
			node_tree.links.new(bsdf.inputs[2], ramp_node_r.outputs['Color'])

def prep_Bump(mat):
	node_tree = mat.node_tree

	bsdf = node_tree.nodes["Principled BSDF"]
	image_node = node_tree.nodes["Image Texture"]
	getramp_node_i = node_tree.nodes.get("Image Texture", None)
	get_node_n = node_tree.nodes.get("Normal Map", None)
	get_node_h = node_tree.nodes.get("Bump Map", None)
	get_rampnode_h = node_tree.nodes.get("ColorRamp_Bump", None)

	if getramp_node_i is not None:
		if get_node_h is None:
			if get_rampnode_h is None:
				ramp_node_h = node_tree.nodes.new('ShaderNodeValToRGB')
				h_node = node_tree.nodes.new('ShaderNodeBump')
				h_node.location = h_node_loc
				h_node.name = "Bump Map"
				ramp_node_h.location = ramp_node_h_loc
				ramp_node_h.name = "ColorRamp_Bump"
				node_tree.links.new(ramp_node_h.inputs['Fac'], image_node.outputs['Color'])
				node_tree.links.new(h_node.inputs['Height'], ramp_node_h.outputs['Color'])
				node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])
			else:
				ramp_node_h = node_tree.nodes["ColorRamp_Bump"]
				h_node = node_tree.nodes.new('ShaderNodeBump')
				h_node.location = h_node_loc
				h_node.name = "Bump Map"
				ramp_node_h.location = ramp_node_h_loc
				node_tree.links.new(ramp_node_h.inputs['Fac'], image_node.outputs['Color'])
				node_tree.links.new(h_node.inputs['Height'], ramp_node_h.outputs['Color'])
				node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])
		else:
			if get_rampnode_h is None:
				ramp_node_h = node_tree.nodes.new('ShaderNodeValToRGB')
				ramp_node_h.location = ramp_node_h_loc
				ramp_node_h.name = "ColorRamp_Bump"
				h_node = node_tree.nodes['Bump Map']
				node_tree.links.new(ramp_node_h.inputs['Fac'], image_node.outputs['Color'])
				node_tree.links.new(h_node.inputs['Height'], ramp_node_h.outputs['Color'])
				node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])
			else:
				h_node = node_tree.nodes['Bump Map']
				ramp_node_h = node_tree.nodes['ColorRamp_Bump']
				node_tree.links.new(ramp_node_h.inputs['Fac'], image_node.outputs['Color'])
				node_tree.links.new(h_node.inputs['Height'], ramp_node_h.outputs['Color'])
				node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])

		if get_node_n is not None:
			n_node = node_tree.nodes["Normal Map"]
			h_node = node_tree.nodes["Bump Map"]
			node_tree.links.new(h_node.inputs['Normal'], n_node.outputs['Normal'])

class Add_Image(bpy.types.Operator):
	bl_idname = "add.image"
	bl_label = "Add Image"
	bl_options = {'REGISTER', 'UNDO'}

	mat: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		mat = bpy.data.materials[self.mat]
		node_tree = mat.node_tree
		tex_node = node_tree.nodes.new('ShaderNodeTexImage')
		tex_node.interpolation = 'Closest'
		tex_node.location = tex_node_loc
		for node in mat.node_tree.nodes:
			if node.name == "Principled BSDF":
				bsdf = node
				node_tree.links.new(bsdf.inputs['Base Color'], tex_node.outputs['Color'])

		return {"FINISHED"}

class New_Material(bpy.types.Operator):
	bl_idname = "new.material"
	bl_label = "New Material"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		ob = context.active_object
		if ob and ob.type == "MESH":
			# Get material
			mat = bpy.data.materials.new(name="Material")
			mat.use_nodes = True

			# Assign it to object
			if ob.data.materials:
				# assign to 1st material slot
				slot = context.object.active_material_index
				ob.data.materials[slot] = mat
			else:
				# no slots
				ob.data.materials.append(mat)
			prep_material(mat)
		else:
			mat = bpy.data.materials.new(name="Material")
			mat.use_nodes = True
			prep_material(mat)

		context.scene.mat_index = context.scene.mat_index + 1
		return {"FINISHED"}

class Prep_Material(bpy.types.Operator):
	bl_idname = "materials.prep"
	bl_label = "Prep Material"
	bl_options = {'REGISTER', 'UNDO'}

	type: bpy.props.StringProperty(options={'HIDDEN'})
	mat: bpy.props.StringProperty(options={'HIDDEN'})

	ramp: BoolProperty(
		name="Specular/Roughness",
		description="Prep Specular/Roughness.",
		default=False,
	)

	bump: BoolProperty(
		name="Prep Bump",
		description="Prep Bump.",
		default=False,
	)

	nomral: BoolProperty(
		name="Prep Nomral",
		description="Prep Nomral.",
		default=False,
	)

	SSS: BoolProperty(
		name="Subsurface",
		description="Prep Subsurface.",
		default=False,
	)
	def draw(self, context):
		layout = self.layout
		layout.prop(self, "SSS", toggle = True)
		layout.prop(self, "ramp", toggle = True)
		layout.prop(self, "bump", toggle = True)
		layout.prop(self, "nomral", toggle = True)

	def execute(self, context):
		if self.type == "obj":
			for obj in context.selected_objects:
				context.view_layer.objects.active = obj
				if obj.type == "MESH":
					actmat = context.object.active_material_index
					matnum = len(context.active_object.data.materials)
					for count in range(matnum):
						context.object.active_material_index = count
						mat = obj.active_material
						try:
							prep_material(mat)
							if self.ramp == True:
								prep_Ramp(mat)
							if self.bump == True:
								prep_Bump(mat)
							if self.nomral == True:
								prep_normal(mat)
							if self.SSS == True:
								prep_SSS(mat, 1)
							else:
								prep_SSS(mat, 0)
						except:
							continue
								
						context.object.active_material_index = actmat

		if self.type == "index":
			mat = bpy.data.materials[self.mat]
			prep_material(mat)
			if self.ramp == True:
				prep_Ramp(mat)
			if self.bump == True:
				prep_Bump(mat)
			if self.nomral == True:
				prep_normal(mat)
			if self.SSS == True:
				prep_SSS(mat, 1)
			else:
				prep_SSS(mat, 0)

		if self.type == "scene":
			for mat in bpy.data.materials:
				try:
					prep_material(mat)
					if self.ramp == True:
						prep_Ramp(mat)
					if self.bump == True:
						prep_Bump(mat)
					if self.nomral == True:
						prep_normal(mat)
					if self.SSS == True:
						prep_SSS(mat, 1)
					else:
						prep_SSS(mat, 0)
				except:
					continue
		return {'FINISHED'}

class Materials_Select(bpy.types.Operator):
	bl_idname = "materials.select"
	bl_label = "Select Material Object"
	bl_options = {'REGISTER', 'UNDO'}

	mat: bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		mat_data = bpy.data.materials[self.mat]
		obj = bpy.data.objects
		count = 0
		for ob in obj:
			if ob.type == 'MESH':
				try:
					for m in ob.material_slots:
						if m.material == mat_data:
							ob.select_set(True)
							count += 1
				except:
					continue
		if count == 0:
			self.report({"INFO"}, "No Objects have " + self.mat)
		else:
			self.report({"INFO"}, str(count) + " Objects have " + self.mat)
		return {"FINISHED"}
	
classes = (
			Add_Image,
			New_Material,
			Prep_Material,
			Materials_Select,
		  )

def register(): 
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
  
def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)