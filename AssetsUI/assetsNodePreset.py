import bpy
import os
from .. import icons

class ADD_OT_kennode(bpy.types.Operator):
	bl_idname = 'add.kennode'
	bl_description = 'Add Node Setup'
	bl_category = 'Node'
	bl_label = 'Add Setup'

	choice: bpy.props.StringProperty()

	def execute(self, context):

		script_file = os.path.realpath(os.path.dirname(__file__))
		script_directory = os.path.dirname(script_file)
		script_directory = os.path.join(script_directory, "Assets")
		script_directory = os.path.normpath(script_directory)
		blendfile = os.path.join(script_directory, "KEN Node_Preset.blend")

		node_group_name = self.choice

		if context.space_data.tree_type == "ShaderNodeTree":

			with bpy.data.libraries.load(blendfile) as (data_from, data_to):
				data_to.node_groups = [name for name in data_from.node_groups if name == node_group_name]

			if node_group_name in bpy.data.node_groups:
				node_group = bpy.data.node_groups[node_group_name]

				# Create a new material or use an existing one
				if context.space_data.shader_type == "OBJECT":
					material = context.object.active_material

					# Set the cursor location in the material's Node Tree
					if material and material.use_nodes:
						tree = material.node_tree
						nodes = tree.nodes
						node = nodes.new("ShaderNodeGroup")
						node.name = node_group_name
						node.node_tree = node_group
						node.location = context.space_data.cursor_location
				elif context.space_data.shader_type == "WORLD":
					world = bpy.context.scene.world
					if world and world.use_nodes:
						tree = world.node_tree
						nodes = tree.nodes
						node = nodes.new("ShaderNodeGroup")
						node.node_tree = node_group
						node.location = context.space_data.cursor_location

		return {"FINISHED"}

class ADD_MT_kennode(bpy.types.Menu):
	bl_idname = 'NODE_MT_add_kennode'
	bl_label = 'KEN Node'

	def draw(self, context):
		script_file = os.path.realpath(__file__)
		script_file = os.path.dirname(script_file)

		pcoll = preview_collections["main"]
		ken_icon = pcoll["Kenimation"]

		layout = self.layout
		if context.space_data.tree_type == "ShaderNodeTree":
			layout.label(text = "Pattern")
			layout.operator(ADD_OT_kennode.bl_idname, text="Pattern").choice = "Pattern"
			layout.operator(ADD_OT_kennode.bl_idname, text="Sphere").choice = "Sphere"
			layout.operator(ADD_OT_kennode.bl_idname, text="Pixelize Noise").choice = "Pixelize Noise"
			layout.separator()
			layout.label(text = "Input")
			layout.operator(ADD_OT_kennode.bl_idname, text="Scene Time").choice = "Scene Time"
			layout.operator(ADD_OT_kennode.bl_idname, text="Simple Particles Info").choice = "Simple Particles Info"
			layout.separator()
			layout.label(text = "Vector")
			layout.operator(ADD_OT_kennode.bl_idname, text="Texture_Sheet").choice = "Texture_Sheet"
			layout.operator(ADD_OT_kennode.bl_idname, text="Texture_Sheet.Separated").choice = "Texture_Sheet.Separated"
			layout.operator(ADD_OT_kennode.bl_idname, text="Animated_Texture").choice = "Animated_Texture"
			layout.separator()
			layout.label(text = "Convertor")
			layout.operator(ADD_OT_kennode.bl_idname, text="ColorRampFac").choice = "ColorRampFac"
			layout.operator(ADD_OT_kennode.bl_idname, text="ColorRampFac_Clamp").choice = "ColorRampFac_Clamp"
			layout.operator(ADD_OT_kennode.bl_idname, text="Color Mask(RGB)").choice = "Color Mask(RGB)"
			layout.operator(ADD_OT_kennode.bl_idname, text="Color Mask(HSV)").choice = "Color Mask(HSV)"
			layout.operator(ADD_OT_kennode.bl_idname, text="Switch Color").choice = "Switch Color"
			layout.operator(ADD_OT_kennode.bl_idname, text="Switch Shader").choice = "Switch Shader"
			layout.operator(ADD_OT_kennode.bl_idname, text="Combine Nomral Map").choice = "Combine Nomral Map"
			layout.separator()
			layout.label(text = "Filter")
			layout.operator(ADD_OT_kennode.bl_idname, text="Enchanted Node").choice = "Enchanted Node"
			layout.operator(ADD_OT_kennode.bl_idname, text="LED Filter").choice = "LED Filter"
			layout.operator(ADD_OT_kennode.bl_idname, text="Pixelized").choice = "Pixelized"
			layout.operator(ADD_OT_kennode.bl_idname, text="Blur").choice = "Blur"
			layout.operator(ADD_OT_kennode.bl_idname, text="Blur (Radial)").choice = "Blur (Radial)"
			layout.separator()
			layout.label(text = "Material")
			layout.operator(ADD_OT_kennode.bl_idname, text="Glass_Dispersion").choice = "Glass_Dispersion"
			layout.operator(ADD_OT_kennode.bl_idname, text="Emission Object").choice = "Emission Object"
			layout.operator(ADD_OT_kennode.bl_idname, text="Illumination Object").choice = "Illumination Object"
			layout.operator(ADD_OT_kennode.bl_idname, text="Volume Scatter").choice = "Volume Scatter"
			layout.operator(ADD_OT_kennode.bl_idname, text="Volume Emission").choice = "Volume Emission"
			layout.separator()
			layout.label(text = "Shader")
			layout.operator(ADD_OT_kennode.bl_idname, text="Light Pass").choice = "Light Pass"
			layout.operator(ADD_OT_kennode.bl_idname, text="Transparent Fac").choice = "Transparent Fac"
			layout.operator(ADD_OT_kennode.bl_idname, text="CastShadowMap").choice = "CastShadowMap"
			if context.space_data.shader_type == "WORLD":
				layout.separator()
				layout.label(text = "World")
				layout.operator(ADD_OT_kennode.bl_idname, text="World Environment").choice = "World Environment"
				layout.operator(ADD_OT_kennode.bl_idname, text="Sky Gradient.Color").choice = "Sky Gradient.Color"
				layout.operator(ADD_OT_kennode.bl_idname, text="Sky Gradient").choice = "Sky Gradient"


def kennode_menu(self, context):
	pcoll = preview_collections["main"]
	ken_icon = pcoll["Kenimation"]
	if context.space_data.tree_type == "ShaderNodeTree":
		self.layout.menu(ADD_MT_kennode.bl_idname, icon_value = ken_icon.icon_id)

preview_collections = {}

classes=(ADD_OT_kennode,ADD_MT_kennode)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
 
	icon = icons.icons("icons")
	pcoll = icon.getColl()
	icon.load(pcoll)
	preview_collections["main"] = pcoll

	bpy.types.NODE_MT_add.append(kennode_menu)

def unregister():
	from bpy.utils import unregister_class
	for cls in classes:
		unregister_class(cls)

	bpy.types.NODE_MT_add.remove(kennode_menu)
