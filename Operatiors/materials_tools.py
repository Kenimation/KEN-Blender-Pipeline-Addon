import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty

tex_node_loc = (-1100, 350)

def get_map_img(img, suffix):
	img_name = img.image.filepath
	str_1 = str(img_name)
	str_list = list(str_1)
	nPos = str_list.index('.')
	str_list.insert(nPos, suffix)
	map_path = "".join(str_list)
	return bpy.data.images.load(filepath=map_path, check_existing=True)

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
	try:
		bsdf = node_tree.nodes["Principled BSDF"]
		img = node_tree.nodes["Image Texture"]
		
		if node_tree.nodes.get("Normal Map Node", None):
			n_map = node_tree.nodes["Normal Map Node"]
		else:
			n_image = get_map_img(img, '_n')
			filename = img.image.name
			n_name = (filename.replace('.png', '') + "_n.png")
			n_map = node_tree.nodes.new('ShaderNodeTexImage')
			n_map.interpolation = 'Closest'
			n_map.name = "Normal Map Node"
			n_map.location = [img.location[0], img.location[1] - 350]
			n_map.image = n_image
			bpy.data.images[n_name].colorspace_settings.name = 'Non-Color'
		if node_tree.nodes.get("Combine Normal Map", None):
			n_node = node_tree.nodes["Combine Normal Map"]
		else:
			bpy.ops.node.append_ken_preset(choice = "Combine Normal Map", x = bsdf.location[0] - 350, y = bsdf.location[1] - 350)
			n_node = node_tree.nodes["Combine Normal Map"]

		node_tree.links.new(n_node.inputs[0], n_map.outputs['Color'])
		node_tree.links.new(bsdf.inputs["Normal"], n_node.outputs["Normal"])
	except:
		pass

def prep_bump(mat):
	node_tree = mat.node_tree
	bsdf = node_tree.nodes["Principled BSDF"]
	img = node_tree.nodes["Image Texture"]

	if node_tree.nodes.get("Combine Normal Map", None):
		n_node = node_tree.nodes["Combine Normal Map"]
	else:
		bpy.ops.node.append_ken_preset(choice = "Combine Normal Map", x = bsdf.location[0] - 350, y = bsdf.location[1] - 350)
		n_node = node_tree.nodes["Combine Normal Map"]

	if node_tree.nodes.get("ColorRamp_Bump", None):
		bump_ramp = node_tree.nodes["ColorRamp_Bump"]
	else:
		bump_ramp = node_tree.nodes.new('ShaderNodeValToRGB')
		bump_ramp.name = "ColorRamp_Bump"
		bump_ramp.location = (n_node.location[0] -350, n_node.location[1])
	node_tree.links.new(bump_ramp.inputs['Fac'], img.outputs['Color'])
	node_tree.links.new(n_node.inputs[2], bump_ramp.outputs['Color'])
	node_tree.links.new(bsdf.inputs["Normal"], n_node.outputs["Normal"])

def prep_emssion(mat):
	node_tree = mat.node_tree
	if node_tree.nodes["Image Texture"]:
		if node_tree.nodes["Principled BSDF"]:
			bsdf = node_tree.nodes["Principled BSDF"]
			img = node_tree.nodes["Image Texture"]
			e_image = get_map_img(img, '_e')
			e_map_node = node_tree.nodes.new('ShaderNodeTexImage')
			e_map_node.interpolation = 'Closest'
			e_map_node.name = "Normal Map Node"
			e_map_node.image = e_image
			e_map_node.location = [img.location[0], img.location[1] + 350]
			bpy.ops.node.append_ken_preset(choice = "Emission Object", x = bsdf.location[0], y = bsdf.location[1] - 350)
			e_node = node_tree.nodes["Emission Object"]
			mix_node = node_tree.nodes.new('ShaderNodeMixShader')
			mix_node.location = [bsdf.location[0] + 350, bsdf.location[1]]

			node_tree.links.new(e_node.inputs[0], img.outputs['Color'])
			node_tree.links.new(e_node.inputs[2], img.outputs['Color'])
			node_tree.links.new(mix_node.inputs[0], e_map_node.outputs['Color'])
			node_tree.links.new(mix_node.inputs[1], bsdf.outputs['BSDF'])
			node_tree.links.new(mix_node.inputs[2], e_node.outputs['Emission'])

			for node in node_tree.nodes:
				# Check if the node is not the BSDF node
				if node != bsdf and node != mix_node:
					# Iterate over the inputs of the node
					for input_socket in node.inputs:
						# Check if the input has any links
						if input_socket.links:
							# Iterate over the links of the input
							for link in input_socket.links:
								# Check if the link originates from the BSDF node
								if link.from_node == bsdf:

									target_node = node_tree.nodes[node.name]

									node_tree.links.new(target_node.inputs[input_socket.name], mix_node.outputs[0])

def prep_ramp(mat):
	node_tree = mat.node_tree
	bsdf = node_tree.nodes["Principled BSDF"]
	image_node = node_tree.nodes["Image Texture"]
	getramp_node_i = node_tree.nodes.get("Image Texture", None)
	getramp_node_s = node_tree.nodes.get("ColorRamp_Specular", None)
	getramp_node_r = node_tree.nodes.get("ColorRamp_Roughness", None)
	if getramp_node_i is not None:
		if getramp_node_s is None:
			ramp_node_s = node_tree.nodes.new('ShaderNodeValToRGB')
			ramp_node_s.location = [bsdf.location[0] - 350, bsdf.location[1] - 200]
			ramp_node_s.name = "ColorRamp_Specular"
			node_tree.links.new(ramp_node_s.inputs['Fac'], image_node.outputs['Color'])
			node_tree.links.new(bsdf.inputs[12], ramp_node_s.outputs['Color'])
		if getramp_node_r is None:
			ramp_node_r = node_tree.nodes.new('ShaderNodeValToRGB')
			ramp_node_r.location = [bsdf.location[0] - 350, bsdf.location[1]]
			ramp_node_r.color_ramp.elements[0].color = (1, 1, 1, 1)
			ramp_node_r.color_ramp.elements[1].color = (0, 0, 0, 1)
			ramp_node_r.name = "ColorRamp_Roughness"
			node_tree.links.new(ramp_node_r.inputs['Fac'], image_node.outputs['Color'])
			node_tree.links.new(bsdf.inputs[2], ramp_node_r.outputs['Color'])

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

	emission: BoolProperty(
		name="Prep Emission",
		description="Prep Emission.",
		default=False,
	)
	def draw(self, context):
		layout = self.layout
		layout.prop(self, "SSS", toggle = True)
		layout.prop(self, "ramp", toggle = True)
		layout.prop(self, "bump", toggle = True)
		layout.prop(self, "nomral", toggle = True)
		layout.prop(self, "emission", toggle = True)

	def execute(self, context):
		def prep(self, mat):
			prep_material(mat)
			report = "Finish Prep Materials"
			if self.ramp == True:
				prep_ramp(mat)
				report = "Finish Prep Ramp"
			if self.bump == True:
				prep_bump(mat)
				report = "Finish Prep Bump Map"
			if self.nomral == True:
				prep_normal(mat)
				report = "Finish Prep Nomral Map"
			if self.emission == True:
				prep_emssion(mat)
				report = "Finish Prep Emission Map"
			if self.SSS == True:
				prep_SSS(mat, 1)
				report = "Finish Prep SSS"
			else:
				prep_SSS(mat, 0)
			self.report({"INFO"}, report)

		if self.type == "obj":
			for obj in context.selected_objects:
				if obj.type == "MESH":
					if obj.data.materials:
						for mat in obj.data.materials:
							try:
								prep(self, mat)
							except:
								continue
								
		if self.type == "index":
			mat = bpy.data.materials[self.mat]
			prep(self, mat)

		if self.type == "scene":
			for mat in bpy.data.materials:
				try:
					prep(self, mat)
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