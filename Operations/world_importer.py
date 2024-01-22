import bpy
import os
import shutil
from pathlib import Path
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, OperatorFileListElement
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty
from ..AssetsUI import assetsDefs
from . import material_tool, editing

def duplicatedDatablock(name):
	"""Check if datablock is a duplicate or not, e.g. ending in .00# """
	try:
		if name[-4] != ".":
			return False
		int(name[-3:])  # Will force ValueError if not a number.
		return True
	except IndexError:
		return False
	except ValueError:
		return False

def get_user_preferences(context=None):
	"""Intermediate method for pre and post blender 2.8 grabbing preferences"""
	if not context:
		context = bpy.context
	prefs = None
	if hasattr(context, "user_preferences"):
		prefs = context.user_preferences.addons.get(__package__, None)
	elif hasattr(context, "preferences"):
		prefs = context.preferences.addons.get(__package__, None)
	if prefs:
		return prefs.preferences
	# To make the addon stable and non-exception prone, return None
	# raise Exception("Could not fetch user preferences")
	return None

def nameGeneralize(name):
	"""Get base name from datablock, accounts for duplicates and animated tex."""
	if duplicatedDatablock(name) is True:
		name = name[:-4]  # removes .001
	if name.endswith(".png"):
		name = name[:-4]

	# if name ends in _####, drop those numbers (for animated sequences)
	# noting it is specifically 4 numbers
	# could use regex, but some historical issues within including this lib
	# in certain blender builds
	nums = '0123456789'
	if len(name) < 5:
		return name
	any_nonnumbs = [1 if ltr in nums else 0 for ltr in name[-4:]]
	if sum(any_nonnumbs) == 4:  # all leters are numbers
		if name[-5] in ["-", "_", " "]:
			name = name[:-5]
		else:
			name = name[:-4]
	return name

def convert_mtl(filepath):
	"""Convert the MTL file if we're not using one of Blender's built in
	colorspaces

	Without this, Blender's OBJ importer will attempt to set non-color data to
	alpha maps and what not, which causes issues in ACES and whatnot where
	non-color data is not an option.

	This MTL conversion simply does the following:
	- Comment out lines that begin with map_d
	- Add a header at the end

	Returns:
		True if success or skipped, False if failed, or None if skipped
	"""
	mtl = filepath.rsplit(".", 1)[0] + '.mtl'
	lines = None
	copied_file = None
	with open(mtl, 'r') as mtl_file:
		lines = mtl_file.readlines()

	# This represents a new folder that'll backup the MTL filepath
	mcprep_header = (
		"# This section was created by MCprep's MTL conversion script\n",
		"# Please do not remove\n",
		"# Thanks c:\n"
	)

	# In this section, we go over each line
	# and check to see if it begins with map_d. If
	# it does, then we simply comment it out. Otherwise,
	# we can safely ignore it.
	try:
		with open(mtl, 'r') as mtl_file:
			for index, line in enumerate(lines):
				if line.startswith("map_d "):
					lines[index] = "# " + line
	except Exception as e:
		print(e)
		return False

	# This needs to be seperate since it involves writing
	try:
		with open(mtl, 'w') as mtl_file:
			mtl_file.writelines(lines)
			mtl_file.writelines(mcprep_header)

	# Recover the original file
	except Exception as e:
		print(e)
		shutil.copy2(copied_file, mtl)
		return False

	return True

def min_bv(version, *, inclusive=True):
	if hasattr(bpy.app, "version"):
		if inclusive is False:
			return bpy.app.version > version
		return bpy.app.version >= version

class World_Import(bpy.types.Operator, ImportHelper):
	"""Imports an obj file, and auto splits it by material"""
	bl_idname = "world.import"
	bl_label = "Import World"
	bl_options = {'REGISTER', 'UNDO'}
        
	filename_ext = '.obj'
    
	filter_glob: StringProperty(
        default='*.obj;*.mtl',
        options={'HIDDEN'}
    )
        
	fileselectparams = "use_filter_blender"
        
	skipUsage = BoolProperty(
		default=False,
		options={'HIDDEN'}
    )
        
	separate_material: BoolProperty(
        name="Separate Material",
        description="Separate the Material to different type blocks.",
        default=False,
    )
	set_ramp: BoolProperty(
        name="Set ColorRamp",
        description="Set Specular and Roughness ColorRamp.",
        default=False,
    )

	def draw(self, context):
		layout = self.layout
		layout.prop(self, "separate_material", toggle = True)
		layout.prop(self, "set_ramp", toggle = True)      

	def execute(self, context):
		# for consistency with the built in one, only import the active path
		if self.filepath.lower().endswith(".mtl"):
			filename = Path(self.filepath)
			new_filename = filename.with_suffix(".obj")
			# Auto change from MTL to OBJ, latet if's will check if existing.
			self.filepath = str(new_filename)
		if not self.filepath:
			self.report({"ERROR"}, "File not found, could not import obj")
			return {'CANCELLED'}
		if not os.path.isfile(self.filepath):
			self.report({"ERROR"}, "File not found, could not import obj")
			return {'CANCELLED'}
		if not self.filepath.lower().endswith(".obj"):
			self.report({"ERROR"}, "You must select a .obj file to import")
			return {'CANCELLED'}

		if "obj" not in dir(bpy.ops.import_scene):
			try:
				bpy.ops.preferences.addon_enable(module="io_scene_obj")
				self.report(
					{"INFO"},
					"FYI: had to enable OBJ imports in user preferences")
			except RuntimeError:
				self.report({"ERROR"}, "Built-in OBJ importer could not be enabled")
				return {'CANCELLED'}

		# There are a number of bug reports that come from the generic call
		# of obj importing. If this fails, should notify the user to try again
		# or try exporting again.
		# In order to not overly supress error messages, below we only capture
		# very tight specific errors possible, so that other errors still get
		# reported so it may be passed off to blender devs. It is understood the
		# below errors are not internationalized, so someone with another lang
		# set will get the raw bubbled up traceback.
		obj_import_err_msg = (
			"Blender's OBJ importer error, try re-exporting your world and "
			"import again.")
		obj_import_mem_msg = (
			"Memory error during OBJ import, try exporting a smaller world")

		# First let's convert the MTL if needed
		conv_res = convert_mtl(self.filepath)
		try:
			if conv_res is None:
				pass  # skipped, no issue anyways.
			elif conv_res is False:
				self.report({"WARNING"}, "MTL conversion failed!")

			res = None
			if min_bv((3, 5)):
				res = bpy.ops.wm.obj_import(
					filepath=self.filepath, use_split_groups=True)
			else:
				res = bpy.ops.wm.obj_import(
					filepath=self.filepath, use_split_groups=True)

		except MemoryError as err:
			print("Memory error during import OBJ:")
			print(err)
			self.report({"ERROR"}, obj_import_mem_msg)
			return {'CANCELLED'}
		except ValueError as err:
			if "could not convert string" in str(err):
				# Error such as:
				#   vec[:] = [float_func(v) for v in line_split[1:]]
				#   ValueError: could not convert string to float: b'6848/28'
				print(err)
				self.report({"ERROR"}, obj_import_err_msg)
				return {'CANCELLED'}
			elif "invalid literal for int() with base" in str(err):
				# Error such as:
				#   idx = int(obj_vert[0])
				#   ValueError: invalid literal for int() with base 10: b'4semtl'
				print(err)
				self.report({"ERROR"}, obj_import_err_msg)
				return {'CANCELLED'}
			else:
				raise err
		except IndexError as err:
			if "list index out of range" in str(err):
				# Error such as:
				#   verts_split.append(verts_loc[vert_idx])
				#   IndexError: list index out of range
				print(err)
				self.report({"ERROR"}, obj_import_err_msg)
				return {'CANCELLED'}
			else:
				raise err
		except UnicodeDecodeError as err:
			if "codec can't decode byte" in str(err):
				# Error such as:
				#   keywords["relpath"] = os.path.dirname(bpy.data.filepath)
				#   UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc4 in
				#     position 24: invalid continuation byte
				print(err)
				self.report({"ERROR"}, obj_import_err_msg)
				return {'CANCELLED'}
			else:
				raise err
		except TypeError as err:
			if "enum" in str(err) and "not found in" in str(err):
				# Error such as:
				#   enum "Non-Color" not found in ('AppleP3 Filmic Log Encoding',
				#  'AppleP3 sRGB OETF', ...
				print(err)
				self.report({"ERROR"}, obj_import_err_msg)
				return {'CANCELLED'}
			else:
				raise err
		except AttributeError as err:
			if "object has no attribute 'image'" in str(err):
				# Error such as:
				#   nodetex.image = image
				#   AttributeError: 'NoneType' object has no attribute 'image'
				print(err)
				self.report({"ERROR"}, obj_import_err_msg)
				return {'CANCELLED'}
			else:
				raise err
		except RuntimeError as err:
			# Possible this is the more broad error that even the abvoe
			# items are wrapped under. Generally just prompt user to re-export.
			print(err)
			self.report({"ERROR"}, obj_import_err_msg)
			return {'CANCELLED'}

		if res != {'FINISHED'}:
			self.report({"ERROR"}, "Issue encountered while importing world")
			return {'CANCELLED'}
		self.split_world_by_material(context)
		return {'FINISHED'}
        
	def obj_to_material(self, obj):
		"""Update an objects name based on its first material"""
		if not obj:
			return
		mat = obj.active_material
		if not mat and not obj.material_slots:
			return
		else:
			try:
				mat = obj.material_slots[0].material
				mat.node_tree.nodes["Principled BSDF"].subsurface_method = 'BURLEY'
				mat.node_tree.nodes["Image Texture"].interpolation = 'Closest'
				mat.node_tree.links.new(mat.node_tree.nodes["Principled BSDF"].inputs['Alpha'], mat.node_tree.nodes["Image Texture"].outputs['Alpha'])
				material_tool.fixmaterial(mat)
				matname = mat.node_tree.nodes["Image Texture"].image.filepath
				str_1 = str(matname)
				str_list = list(str_1)
				nPos = str_list.index('-')
				str_list.insert(nPos, '_n')
				n_path = "".join(str_list)
				n_img = (n_path.replace('RGB', "RGBA"))
				n_image = bpy.data.images.load(filepath=n_img, check_existing=True)
				bsdf = mat.node_tree.nodes["Principled BSDF"]
				filename = mat.node_tree.nodes["Image Texture"].image.name
				n_name = (filename.replace('-', "_n-"))
				n_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
				n_node.name = "Normal Map Node"
				n_node.location = (-500,-250)
				n_node.image = n_image
				mat.node_tree.nodes["Normal Map Node"].interpolation = 'Closest'
				bpy.data.images[n_name].colorspace_settings.name = 'Non-Color'
				n_map = mat.node_tree.nodes.new('ShaderNodeNormalMap')
				n_map.name = "Normal Map"
				n_map.location = (-250,-250)
				mat.node_tree.links.new(n_map.inputs['Color'], n_node.outputs['Color'])
				mat.node_tree.links.new(bsdf.inputs['Normal'], n_map.outputs['Normal'])
				mat.blend_method = 'HASHED'
				if self.set_ramp == True:
					material_tool.fixRamp(mat)
			except:
				pass
		if not mat:
			return
		obj.name = nameGeneralize(mat.name)
		bpy.ops.object.transform_apply(rotation=True)

	def split_world_by_material(self, context):
                
		"""2.8-only function, split combined object into parts by material"""
		world_name = os.path.basename(self.filepath)
		world_name = os.path.splitext(world_name)[0]

		# Create the new world collection
		name = world_name + "_Map"
		worldg = assetsDefs.collections().new(name=name)
		context.scene.collection.children.link(worldg)  # Add to outliner.

		for obj in context.selected_objects:
			assetsDefs.move_to_collection(obj, worldg)

		# Force renames based on material, as default names are not useful.
		for obj in worldg.objects:
			self.obj_to_material(obj)
		if self.separate_material == False:
			for obj in bpy.context.selected_objects:
				bpy.context.view_layer.objects.active = obj
			bpy.ops.object.make_links_data(type='MATERIAL')
			bpy.ops.outliner.orphans_purge()
			obj.active_material.name = name + "_Blocks"

classes = (
            World_Import,
          )        

register, unregister = bpy.utils.register_classes_factory(classes)