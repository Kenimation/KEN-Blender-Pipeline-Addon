import bpy
import json
import os
import mathutils
import math
import shutil
from math import inf
import numpy as np

DIRECTIONS = np.array([
    "north",
    "east",
    "west",
    "south",
    "up",
    "down",
])

# normals for minecraft directions in BLENDER world space
# e.g. blender (-1, 0, 0) is minecraft north (0, 0, -1)
# shape (f,n,v) = (6,6,3)
#   f = 6: number of cuboid faces to test
#   n = 6: number of normal directions
#   v = 3: vector coordinates (x,y,z)
DIRECTION_NORMALS = np.array([
    [-1.,  0.,  0.],
    [ 0.,  1.,  0.],
    [ 0., -1.,  0.],
    [ 1.,  0.,  0.],
    [ 0.,  0.,  1.],
    [ 0.,  0., -1.],
])
DIRECTION_NORMALS = np.tile(DIRECTION_NORMALS[np.newaxis,...], (6,1,1))

n_map_node_loc= (-1100,-350)
n_node_loc = (-800,-350)
ramp_node_h_loc = (-650,-125)
h_node_loc = (-200,-250)
tex_node_loc = (-1100, 350)

def create_textured(mat_name, tex_path):
    """Create new material with `mat_name` and texture path `tex_path`
    """
    mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True
    node_tree = mat.node_tree
    nodes = node_tree.nodes
    bsdf = nodes.get("Principled BSDF") 

    # add texture node_tree
    if bsdf is not None:
        if "Base Color" in bsdf.inputs:
            tex_input = nodes.new(type="ShaderNodeTexImage")
            tex_input.interpolation = "Closest"
            # load image, if fail make a new image with filepath set to tex path
            try:
                img = bpy.data.images.load(tex_path, check_existing=True)
            except:
                print("FAILED TO LOAD IMAGE:", tex_path)
                img = bpy.data.images.new(os.path.split(tex_path)[-1], width=16, height=16)
                img.filepath = tex_path
        
            tex_input.image = img
            node_tree.links.new(tex_input.outputs[0], bsdf.inputs["Base Color"])
            bsdf.subsurface_method = 'BURLEY'
    
    mat.node_tree.links.new(mat.node_tree.nodes["Principled BSDF"].inputs['Alpha'], mat.node_tree.nodes["Image Texture"].outputs['Alpha'])
    matname = mat.node_tree.nodes["Image Texture"].image.name
    mat.name = matname.replace('.png', '')
    mat.blend_method = 'HASHED'

    return mat

def index_of(val, in_list):
    """Return index of value in in_list"""
    try:
        return in_list.index(val)
    except ValueError:
        return -1 

def merge_dict_properties(dict_original, d):
    """Merge inner dict properties"""
    for k in d:
        if k in dict_original and isinstance(dict_original[k], dict):
            dict_original[k].update(d[k])
        else:
            dict_original[k] = d[k]
    
    return dict_original

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

def min_bv(version, *, inclusive=True):
	if hasattr(bpy.app, "version"):
		if inclusive is False:
			return bpy.app.version > version
		return bpy.app.version >= version

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

def users_collection(obj):
	"""Returns the collections/group of an object"""
	if hasattr(obj, "users_collection"):
		return obj.users_collection
	elif hasattr(obj, "users_group"):
		return obj.users_group

def collections():
	"""Returns group or collection object for 2.7 and 2.8"""
	if hasattr(bpy.data, "collections"):
		return bpy.data.collections
	else:
		return bpy.data.groups

def move_to_collection(obj, collection):

	"""Move out of all collections and into this specified one. 2.8 only"""
	for col in obj.users_collection:
		col.objects.unlink(obj)
	collection.objects.link(obj)

def get_full_file_path(filepath_parts, path, merge_point=None):
    """"Typical path formats in json files are like:
            "parent": "block/cube",
            "textures": {
                "top": "block/top"
            }
    This checks in filepath_parts of the blender file,
    matches the base path, then merges the input path, e.g.
        path = "block/cube"
        merge_point = "models"
        filepath_parts = ["C:", "minecraft", "resources", "models", "block", "cobblestone.json"]
                                                             |
                                                     Matched merge point
        
        joined parts = ["C:", "minecraft", "resources", "models"] + ["block", "cube"]
    """
    path_chunks = os.path.split(path)

    # match base path
    if merge_point is not None:
        idx_base_path = index_of(merge_point, filepath_parts)
    else:
        idx_base_path = index_of(path_chunks[0], filepath_parts)

    if idx_base_path != -1:
        # system agnostic path join
        joined_path = os.path.join(os.sep, filepath_parts[0] + os.sep, *filepath_parts[1:idx_base_path+1], *path.split("/"))
        return joined_path
    else:
        return path # failed

def get_textures(material):
    """Extract the image datablocks for a given material (prefer cycles).
    """
    passes = {
        "diffuse": None}

    if not material:
        return passes

    # first try cycles materials, fall back to internal if not present
    if material.use_nodes is True:
        for node_tree in material.node_tree.nodes:
            if node_tree.type != "TEX_IMAGE":
                continue
            elif "Image Texture" in node_tree:
                passes["diffuse"] = node_tree.image
            else:
                if not passes["diffuse"]:
                    passes["diffuse"] = node_tree.image

    # look through internal, unless already found main diffuse pass
    # TODO: Consider checking more explicitly checking based on selected engine
    if hasattr(material, "texture_slots") and not passes["diffuse"]:
        for sl in material.texture_slots:
            if not (sl and sl.use and sl.texture is not None
                    and hasattr(sl.texture, "image")
                    and sl.texture.image is not None):
                continue
            if sl.use_map_color_diffuse and passes["diffuse"] is None:
                passes["diffuse"] = sl.texture.image
            elif sl.use_map_normal and passes["normal"] is None:
                passes["normal"] = sl.texture.image
            elif sl.use_map_specular and passes["specular"] is None:
                passes["specular"] = sl.texture.image
            elif sl.use_map_displacement and passes["displace"] is None:
                passes["displace"] = sl.texture.image

    return passes

def load(context,
         filepath,
         import_uvs = True,               # import face uvs
         import_textures = True,          # import textures into materials
         translate_origin_by_8 = False,   # shift model by (-8, -8, -8)
         recenter_to_origin = True,       # recenter model to origin, overrides translate origin
         **kwargs):
    """Main import function"""

    with open(filepath, "r") as f:
        data = json.load(f)
    
    # chunks of import file path, to get base directory
    filepath_parts = filepath.split(os.path.sep)
    
    # check if parent exists, need to merge data into parent
    if "parent" in data:
        # build stack of data dicts, then write backwards:
        # data_hierarchy = [this, parent1, parent2, ...]
        data_hierarchy = [data]
        curr_data = data
        
        # in case circular dependency...
        curr_level = 0
        MAX_PARENT_LEVEL = 10

        # find path models merge point:
        # - normal model location is "assets/models"
        # - if "models" does not exist, check for "model"
        path_models_merge_point = None
        for p in reversed(filepath_parts):
            if p == "models" or p == "model":
                path_models_merge_point = p
                break

        while True:
            # parent path without namespacing, e.g. "minecraft:block/cobblestone" -> "block/cobblestone"
            parent_path = curr_data["parent"].split(":")[-1]
            
            # get parent path
            filepath_parent = get_full_file_path(filepath_parts, parent_path, merge_point=path_models_merge_point) + ".json"

            if os.path.exists(filepath_parent):
                with open(filepath_parent, "r") as f:
                    data_parent = json.load(f)
                    data_hierarchy.append(data_parent)
                    curr_data = data_parent
            else:
                print("FAILED TO FIND PARENT:", filepath_parent)
                break

            curr_level += 1

            if "parent" not in curr_data or curr_level > MAX_PARENT_LEVEL:
                break
    
        # merge together data, need to specially merge inner dict values
        data = {}
        for d in reversed(data_hierarchy):
            data = merge_dict_properties(data, d)

    # main object elements
    try:
        elements = data["elements"]
    except:
         pass

    # check if groups in .json
    # not a minecraft .json spec, used by this exporter + Blockbench
    # as additional data to group models together
    if "groups" in data:
        groups = data["groups"]
    else:
        groups = {}
    
    # objects created
    objects = []

    # model bounding box vector
    model_v_min = np.array([inf, inf, inf])
    model_v_max = np.array([-inf, -inf, -inf])

    # minecraft coordinate system origin
    if translate_origin_by_8:
        minecraft_origin = np.array([8., 8., 8.])
    else:
        # ignore if not translating
        minecraft_origin = np.array([0., 0., 0.])

    # set scene collection as active
    scene_collection = bpy.context.view_layer.layer_collection
    bpy.context.view_layer.active_layer_collection = scene_collection
    
    # re-used buffers for every object
    v_world = np.zeros((3, 8))
    face_normals = np.zeros((6,1,3))

    # =============================================
    # import textures, create map of material name => material
    # =============================================
    """Note two type of texture formats:
        "textures:" {
            "down": "#bottom",                         # texture alias to another texture
            "bottom": "minecraft:block/cobblestone",   # actual texture image
        }

    Loading textures is two pass:
        1. load all actual texture images
        2. map aliases to loaded texture images
    """
    textures = {}
    if import_textures and "textures" in data:
        # get textures path for models, replace "model" or "models" with "textures"
        filepath_textures = filepath_parts
        idx = -1
        for i, p in enumerate(filepath_parts):
            if p == "models" or p == "model":
                idx = i
                break
        if idx != -1:
            filepath_textures[idx] = "textures"
        
        # load texture images
        for tex_name, tex_path in data["textures"].items():
            # skip aliases
            if tex_path[0] == "#":
                continue

            tex_path = tex_path.split(":")[-1] # strip out namespace, like "minecraft:block/name"
            filepath_tex = get_full_file_path(filepath_textures, tex_path, merge_point="textures") + ".png"
            textures[tex_name] = create_textured(tex_name, filepath_tex)

        # map texture aliases
        for tex_name, tex_path in data["textures"].items():
            if tex_path[0] == "#":
                tex_path = tex_path[1:]
                if tex_path in textures:
                    textures[tex_name] = textures[tex_path]

    # =============================================
    # import geometry, uvs
    # =============================================
    for i, e in enumerate(elements):
        # get cube min/max
        v_min = np.array([e["from"][2], e["from"][0], e["from"][1]])
        v_max = np.array([e["to"][2], e["to"][0], e["to"][1]])

        # get rotation + origin
        rot = e.get("rotation")
        if rot is not None:
            rot_axis = rot["axis"]
            rot_angle = rot["angle"] * math.pi / 180
            location = np.array([rot["origin"][2], rot["origin"][0], rot["origin"][1]]) - minecraft_origin
            
            if rot_axis == "x":
                rot_euler = (0.0, rot_angle, 0.0)
            if rot_axis == "y":
                rot_euler = (0.0, 0.0, rot_angle)
            if rot_axis == "z":
                rot_euler = (rot_angle, 0.0, 0.0)
        else:
            # default location to center of mass
            location = 0.5 * (v_min + v_max)
            rot_euler = (0.0, 0.0, 0.0)
        
        # create cube
        bpy.ops.mesh.primitive_cube_add(location=location, rotation=rot_euler)
        obj = bpy.context.active_object
        mesh = obj.data
        mesh_materials = {} # tex_name => material_index

        # center local mesh coordiantes
        v_min = v_min - minecraft_origin - location
        v_max = v_max - minecraft_origin - location
        
        # set vertices
        mesh.vertices[0].co[:] = v_min[0], v_min[1], v_min[2]
        mesh.vertices[1].co[:] = v_min[0], v_min[1], v_max[2]
        mesh.vertices[2].co[:] = v_min[0], v_max[1], v_min[2]
        mesh.vertices[3].co[:] = v_min[0], v_max[1], v_max[2]
        mesh.vertices[4].co[:] = v_max[0], v_min[1], v_min[2]
        mesh.vertices[5].co[:] = v_max[0], v_min[1], v_max[2]
        mesh.vertices[6].co[:] = v_max[0], v_max[1], v_min[2]
        mesh.vertices[7].co[:] = v_max[0], v_max[1], v_max[2]

        # set face uvs
        uv = e.get("faces")
        if uv is not None:
            if import_uvs:
                for i, face in enumerate(mesh.polygons):
                    face_normals[i,0,0:3] = face.normal
                
                # map face normal -> face name
                # NOTE: this process may not be necessary since new blender
                # objects are created with the same face normal order,
                # so could directly map index -> minecraft face name.
                # keeping this in case the order changes in future
                face_directions = np.argmax(np.sum(face_normals * DIRECTION_NORMALS, axis=2), axis=1)
                face_directions = DIRECTIONS[face_directions]

                # set uvs face order in blender loop, determined experimentally
                uv_layer = mesh.uv_layers.active.data
                for uv_direction, face in zip(face_directions, mesh.polygons):
                    face_uv = uv.get(uv_direction)
                    if face_uv is not None:
                        if "uv" in face_uv:
                            # unpack uv coords in minecraft coord space [xmin, ymin, xmax, ymax]
                            # transform from minecraft [0, 16] space +x,-y space to blender [0,1] +x,+y
                            face_uv_coords = face_uv["uv"]
                            xmin = face_uv_coords[0] / 16.0
                            ymin = 1.0 - face_uv_coords[3] / 16.0
                            xmax = face_uv_coords[2] / 16.0
                            ymax = 1.0 - face_uv_coords[1] / 16.0
                        else:
                            xmin = 0.0
                            ymin = 1.0
                            xmax = 1.0
                            ymax = 0.0
                        
                        # write uv coords based on rotation
                        k = face.loop_start
                        if "rotation" not in face_uv or face_uv["rotation"] == 0:
                            uv_layer[k].uv[0:2] = xmax, ymin
                            uv_layer[k+1].uv[0:2] = xmax, ymax
                            uv_layer[k+2].uv[0:2] = xmin, ymax
                            uv_layer[k+3].uv[0:2] = xmin, ymin

                        elif face_uv["rotation"] == 90:
                            uv_layer[k].uv[0:2] = xmax, ymax
                            uv_layer[k+1].uv[0:2] = xmin, ymax
                            uv_layer[k+2].uv[0:2] = xmin, ymin
                            uv_layer[k+3].uv[0:2] = xmax, ymin

                        elif face_uv["rotation"] == 180:
                            uv_layer[k].uv[0:2] = xmin, ymax
                            uv_layer[k+1].uv[0:2] = xmin, ymin
                            uv_layer[k+2].uv[0:2] = xmax, ymin
                            uv_layer[k+3].uv[0:2] = xmax, ymax

                        elif face_uv["rotation"] == 270:
                            uv_layer[k].uv[0:2] = xmin, ymin
                            uv_layer[k+1].uv[0:2] = xmax, ymin
                            uv_layer[k+2].uv[0:2] = xmax, ymax
                            uv_layer[k+3].uv[0:2] = xmin, ymax

                        else: # invalid rotation, should never occur... do default
                            uv_layer[k].uv[0:2] = xmax, ymin
                            uv_layer[k+1].uv[0:2] = xmax, ymax
                            uv_layer[k+2].uv[0:2] = xmin, ymax
                            uv_layer[k+3].uv[0:2] = xmin, ymin

                        # assign material
                        if "texture" in face_uv:
                            tex_name = face_uv["texture"][1:] # remove the "#" in start
                            if tex_name in mesh_materials:
                                face.material_index = mesh_materials[tex_name]
                            elif tex_name in textures: # need new mapping
                                idx = len(obj.data.materials)
                                obj.data.materials.append(textures[tex_name])
                                mesh_materials[tex_name] = idx
                                face.material_index = idx

        # set name (choose whatever is available or "cube" if no name or comment is given)
        obj.name = e.get("name") or e.get("__comment") or "cube"

        # save created object
        objects.append(obj)

        # ================================
        # update global model bounding box
        # ================================
        # get world coordinates
        mat_world = obj.matrix_world
        for i, v in enumerate(mesh.vertices):
            v_world[0:3,i] = mat_world @ v.co
        
        model_v_min = np.amin(np.append(v_world, model_v_min[...,np.newaxis], axis=1), axis=1)
        model_v_max = np.amax(np.append(v_world, model_v_max[...,np.newaxis], axis=1), axis=1)

    # model post-processing
    if recenter_to_origin:
        mean = 0.5 * (model_v_min + model_v_max)
        mean = mathutils.Vector((mean[0], mean[1], mean[2]))
        for o in objects:
            o.location = o.location - mean
    
    # import groups as collections
    for g in groups:
        try:
            name = g["name"]
            if name == "Master Collection":
                continue
            col = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(col)
            for index in g["children"]:
                col.objects.link(objects[index])
                bpy.context.scene.collection.objects.unlink(objects[index])
        except:
            pass
    
    # select newly imported objects
    mat = bpy.context.active_object.active_material
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    for obj in objects:
        obj.select_set(True)
    for obj in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = obj
        obj.name = mat.name
    bpy.ops.transform.resize(value=(0.1, 0.1, 0.1))
    bpy.ops.object.transform_apply(scale=True)
    
    return {"FINISHED"}

def centroid(vertexes):
    x_list = [vertex[0] for vertex in vertexes]
    y_list = [vertex[1] for vertex in vertexes]
    length = len(vertexes)
    x = sum(x_list) / length
    y = sum(y_list) / length
    return(mathutils.Vector((x, y)))

def copytransform(self, xyz):
    if bpy.context.object.mode == 'OBJECT':
        actobj = bpy.context.view_layer.objects.active
        if self == "loc":
            for obj in bpy.context.selected_objects:
                if xyz == "x":
                    obj.matrix_world.translation[0] = actobj.matrix_world.translation[0]
                if xyz == "y":
                    obj.matrix_world.translation[1] = actobj.matrix_world.translation[1]
                if xyz == "z":
                    obj.matrix_world.translation[2] = actobj.matrix_world.translation[2]
        if self == "rota":
            for obj in bpy.context.selected_objects:
                if xyz == "x":
                    obj.rotation_euler[0] = actobj.rotation_euler[0]
                if xyz == "y":
                    obj.rotation_euler[1] = actobj.rotation_euler[1]
                if xyz == "z":
                    obj.rotation_euler[2] = actobj.rotation_euler[2]
        if self == "size":
            for obj in bpy.context.selected_objects:
                if xyz == "x":
                    obj.scale[0] = actobj.scale[0]
                if xyz == "y":
                    obj.scale[1] = actobj.scale[1]
                if xyz == "z":
                    obj.scale[2] = actobj.scale[2]
    elif bpy.context.object.mode == 'POSE':
        actbones = bpy.context.active_pose_bone
        if self == "loc":
            for bones in bpy.context.selected_pose_bones:
                if xyz == "x":
                    bones.location[0] = actbones.location[0]
                if xyz == "y":
                    bones.location[1] = actbones.location[1]
                if xyz == "z":
                    bones.location[2] = actbones.location[2]
        if self == "rota":
            for bones in bpy.context.selected_pose_bones:
                if xyz == "x":
                    bones.rotation_euler[0] = actbones.rotation_euler[0]
                if xyz == "y":
                    bones.rotation_euler[1] = actbones.rotation_euler[1]
                if xyz == "z":
                    bones.rotation_euler[2] = actbones.rotation_euler[2]
        if self == "size":
            for bones in bpy.context.selected_pose_bones:
                if xyz == "x":
                    bones.scale[0] = actbones.scale[0]
                if xyz == "y":
                    bones.scale[1] = actbones.scale[1]
                if xyz == "z":
                    bones.scale[2] = actbones.scale[2]

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

def scale_uv(factor):
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
    bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.active_object.data
    uv = obj.uv_layers.active
    for f in obj.polygons:
        # Get uv polygon center
        x = y = n = 0  # x,y,number of verts in loop for average purpose
        for loop_ind in f.loop_indices:
            # a loop could be an edge or face
            # The vertex data that loop entry refers to:
            # v = ob.data.vertices[l.vertex_index]
            # isolate to specific UV already used
            x += uv.data[loop_ind].uv[0]
            y += uv.data[loop_ind].uv[1]
            n += 1
        for loop_ind in f.loop_indices:
            uv.data[loop_ind].uv[0] = uv.data[loop_ind].uv[0]*(1-factor)+x/n*(factor)
            uv.data[loop_ind].uv[1] = uv.data[loop_ind].uv[1]*(1-factor)+y/n*(factor)
    bpy.ops.object.mode_set(mode = 'EDIT')

def selectalpha(threshold):
    obj = bpy.context.active_object
    """Core function to select alpha faces based on active material/image."""
    if not obj.material_slots:
        print("No materials, skipping.")
        return "No materials"

        # pre-cache the materials and their respective images for comparing
    textures = []
    for index in range(len(obj.material_slots)):
        mat = obj.material_slots[index].material
        if not mat:
            textures.append(None)
            continue
        image = get_textures(mat)["diffuse"]
        if not image:
            textures.append(None)
            continue
        elif image.channels != 4:
            textures.append(None)  # no alpha channel anyways
            print({'WARNING'}, "No alpha channel for: " + image.name)
            continue
        textures.append(image)
    data = [None for tex in textures]

    uv = obj.data.uv_layers.active
    for f in obj.data.polygons:
        if len(f.loop_indices) < 3:
            continue  # don't select edges or vertices
        fnd = f.material_index
        image = textures[fnd]
        if not image:
            print("Could not get image from face's material")
            return "Could not get image from face's material"

        # lazy load alpha part of image to memory, hold for whole operator
        if not data[fnd]:
            data[fnd] = list(image.pixels)[3::4]

            # relate the polygon to the UV layer to the image coordinates
        shape = []
        for i in f.loop_indices:
            loop = obj.data.loops[i]
            x = uv.data[loop.index].uv[0] % 1  # TODO: fix this wraparound hack
            y = uv.data[loop.index].uv[1] % 1
            shape.append((x, y))

            # print("The shape coords:")
            # print(shape)
            # could just do "the closest" pixel... but better is weighted area
        if not shape:
            continue

        xlist, ylist = tuple([list(tup) for tup in zip(*shape)])
            # not sure if I actually want to +0.5 to the values to get middle..
        xmin = round(min(xlist) * image.size[0]) - 0.5
        xmax = round(max(xlist) * image.size[0]) - 0.5
        ymin = round(min(ylist) * image.size[1]) - 0.5
        ymax = round(max(ylist) * image.size[1]) - 0.5

            # assuming faces are roughly rectangular, sum pixels a face covers
        asum = 0
        acount = 0
        for row in range(image.size[1]):
            if row < ymin or row > ymax:
                continue
            for col in range(image.size[0]):
                if col >= xmin and col <= xmax:
                    try:
                        asum += data[fnd][image.size[0] * row + col]
                        acount += 1
                    except:
                        print("Index error while parsing col {}, row {}: {}")

        if acount == 0:
            acount = 1
        ratio = float(asum) / float(acount)
        if ratio < float(threshold):
            print("\t{} - Below threshold, select".format(ratio))
            f.select = True
        else:
            print("\t{} - above thresh, NO select".format(ratio))
            f.select = False
    bpy.ops.object.mode_set(mode = 'EDIT')

def fixmaterial(mat):
    node_tree = mat.node_tree
    for node in node_tree.nodes:
        if node.type == "BSDF_PRINCIPLED":
            node.subsurface_method = 'BURLEY'
        if node.type == "TEX_IMAGE":
            node.interpolation = 'Closest'
        try:
            node_tree.links.new(node_tree.nodes["Principled BSDF"].inputs['Alpha'], node_tree.nodes["Image Texture"].outputs['Alpha'])
        except:
            pass
    try:
        mat.blend_method = 'HASHED'
    except:
        print({'WARNING'}, "Active object has no material")

def fixSSS(mat, type):
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

def fixnormal(mat):
    node_tree = mat.node_tree
    num = len(node_tree.nodes)
    for number in range(num):
        if number == 0:
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
        else:
            try:
                id = str(number)
                bsdf = node_tree.nodes["Principled BSDF.00"+id]
                try:
                    matname = node_tree.nodes["Image Texture"].image.filepath
                    str_1 = str(matname)
                    str_list = list(str_1)
                    nPos = str_list.index('.')
                    str_list.insert(nPos, '_n')
                    n_path = "".join(str_list)
                    n_image = bpy.data.images.load(filepath=n_path, check_existing=True)
                    n_map_node = node_tree.nodes.get("Normal Map Node", None)
                except:
                    break
                if n_map_node is None:
                    bsdf = node_tree.nodes["Principled BSDF"]
                    filename = node_tree.nodes["Image Texture"].image.name
                    n_name = (filename.replace('.png', '') + "_n.png")
                    n_map_node = node_tree.new('ShaderNodeTexImage')
                    n_map_node.interpolation = 'Closest'
                    n_map_node.name = "Normal Map Node.00"+id
                    n_map_node.location = n_map_node_loc
                    n_map_node.image = n_image
                    bpy.data.images[n_name].colorspace_settings.name = 'Non-Color'
                    n_node = node_tree.nodes.new('ShaderNodeNormalMap')
                    n_node.name = "Normal Map.00"+id
                    n_node.location = n_node_loc
                    node_tree.links.new(n_node.inputs['Color'], n_map_node.outputs['Color'])
                    if get_node_h is not None:
                        h_node = node_tree.nodes["Bump Map.00"+id]
                        node_tree.links.new(h_node.inputs['Normal'], n_node.outputs['Normal'])
                        node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])
                    else:
                        node_tree.links.new(bsdf.inputs['Normal'], n_node.outputs['Normal'])
                else:
                    n_node = node_tree.nodes["Normal Map.00"+id]
                    if get_node_h is not None:
                        n_node = node_tree.nodes["Normal Map.00"+id]

                        node_tree.links.new(h_node.inputs['Normal'], n_node.outputs['Normal'])
                        node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])
                    else:
                        node_tree.links.new(bsdf.inputs['Normal'], n_node.outputs['Normal'])
            except:
                print("No More Mode Found.")

def fixRamp(mat):
    node_tree = mat.node_tree
    num = len(node_tree.nodes)
    for number in range(num):
        if number == 0:
            try:
                bsdf = node_tree.nodes["Principled BSDF"]
                image_node = node_tree.nodes["Image Texture"]
                getramp_node_i = node_tree.nodes.get("Image Texture", None)
                getramp_node_s = node_tree.nodes.get("ColorRamp_Specular", None)
                getramp_node_r = node_tree.nodes.get("ColorRamp_Roughness", None)
            except:
                return
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
                    ramp_node_r.color_ramp.elements[0].position = 1
                    ramp_node_r.color_ramp.elements[1].position = 0
                    ramp_node_r.name = "ColorRamp_Roughness"
                    node_tree.links.new(ramp_node_r.inputs['Fac'], image_node.outputs['Color'])
                    node_tree.links.new(bsdf.inputs[2], ramp_node_r.outputs['Color'])
        else:
            try:
                id = str(number)
                try:
                    bsdf = node_tree.nodes["Principled BSDF"]
                    image_node = node_tree.nodes["Image Texture"]
                    getramp_node_i = node_tree.nodes.get("Image Texture.00"+id, None)
                    getramp_node_s = node_tree.nodes.get("ColorRamp_Specular.00"+id, None)
                    getramp_node_r = node_tree.nodes.get("ColorRamp_Roughness.00"+id, None)
                except:
                    return
                if getramp_node_i == 1:
                    if getramp_node_s == 1:
                        ramp_node_s = node_tree.nodes.new('ShaderNodeValToRGB')
                        ramp_node_s.location = (-400, 175)
                        ramp_node_s.name = "ColorRamp_Specular.00"+id
                        node_tree.links.new(ramp_node_s.inputs['Fac'], image_node.outputs['Color'])
                        node_tree.links.new(bsdf.inputs[12], ramp_node_s.outputs['Color'])
                    if getramp_node_r == 1:
                        ramp_node_r = node_tree.nodes.new('ShaderNodeValToRGB')
                        ramp_node_r.location = (-400,-25)
                        ramp_node_r.color_ramp.elements[0].position = 1
                        ramp_node_r.color_ramp.elements[1].position = 0
                        ramp_node_r.name = "ColorRamp_Roughness.00"+id
                        node_tree.links.new(ramp_node_r.inputs['Fac'], image_node.outputs['Color'])
                        node_tree.links.new(bsdf.inputs[2], ramp_node_r.outputs['Color'])
            except:
                print("No More Mode Found.")

def fixBump(mat):
    node_tree = mat.node_tree
    num = len(node_tree.nodes)
    for number in range(num):
        if number == 0:
            try:
                bsdf = node_tree.nodes["Principled BSDF"]
                image_node = node_tree.nodes["Image Texture"]
                getramp_node_i = node_tree.nodes.get("Image Texture", None)
                get_node_n = node_tree.nodes.get("Normal Map", None)
                get_node_h = node_tree.nodes.get("Bump Map", None)
                get_rampnode_h = node_tree.nodes.get("ColorRamp_Bump", None)
            except:
                break
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
        else:
            try:
                id = str(number)    
                try:
                    bsdf = node_tree.nodes["Principled BSDF.00"+id]
                    image_node = node_tree.nodes["Image Texture.00"+id]
                    getramp_node_i = node_tree.nodes.get("Image Texture.00"+id, None)
                    get_node_n = node_tree.nodes.get("Normal Map.00"+id, None)
                    get_node_h = node_tree.nodes.get("Bump Map.00"+id, None)
                except:
                    break
                if getramp_node_i is not None:
                    if get_node_h is None:
                        if  get_rampnode_h is None:
                            ramp_node_h = node_tree.nodes.new('ShaderNodeValToRGB')
                            h_node = node_tree.nodes.new('ShaderNodeBump')
                            h_node.location = h_node_loc
                            h_node.name = "Bump Map.00"+id
                            ramp_node_h.location = ramp_node_h_loc
                            ramp_node_h.name = "ColorRamp_Bump.00"+id
                            node_tree.links.new(ramp_node_h.inputs['Fac'], image_node.outputs['Color'])
                            node_tree.links.new(h_node.inputs['Height'], ramp_node_h.outputs['Color'])
                            node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])
                        else:
                            ramp_node_h = node_tree.nodes["ColorRamp_Bump.00"+id]
                            h_node = node_tree.nodes.new('ShaderNodeBump')
                            h_node.location = h_node_loc
                            h_node.name = "Bump Map.00"+id
                            ramp_node_h.location = ramp_node_h_loc
                            node_tree.links.new(ramp_node_h.inputs['Fac'], image_node.outputs['Color'])
                            node_tree.links.new(h_node.inputs['Height'], ramp_node_h.outputs['Color'])
                            node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])
                    else:
                        if get_rampnode_h is None:
                            ramp_node_h = node_tree.nodes.new('ShaderNodeValToRGB')
                            ramp_node_h.location = ramp_node_h_loc
                            ramp_node_h.name = "ColorRamp_Bump.00"+id
                            h_node = node_tree.nodes['Bump Map.00'+id]
                            node_tree.links.new(ramp_node_h.inputs['Fac'], image_node.outputs['Color'])
                            node_tree.links.new(h_node.inputs['Height'], ramp_node_h.outputs['Color'])
                            node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])
                        else:
                            h_node = node_tree.nodes['Bump Map.00'+id]
                            ramp_node_h = node_tree.nodes['ColorRamp_Bump.00'+id]
                            node_tree.links.new(ramp_node_h.inputs['Fac'], image_node.outputs['Color'])
                            node_tree.links.new(h_node.inputs['Height'], ramp_node_h.outputs['Color'])
                            node_tree.links.new(bsdf.inputs['Normal'], h_node.outputs['Normal'])
                    if get_node_n is not None:
                        n_node = node_tree.nodes["Normal Map.00"+id]
                        h_node = node_tree.nodes["Bump Map.00"+id]
                        node_tree.links.new(h_node.inputs['Normal'], n_node.outputs['Normal'])
            except:
                print("No More Mode Found.")

def Solidify(thickness):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].offset = 0
    bpy.context.object.modifiers["Solidify"].use_even_offset = True
    bpy.context.object.modifiers["Solidify"].thickness = thickness/100
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')