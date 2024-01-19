import bpy
import os
import json
import mathutils
import math
import numpy as np
from math import inf
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, OperatorFileListElement
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty
from ..AssetsUI import assetsDefs
from . import fix_material, editing

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

def Solidify(thickness):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].offset = 0
    bpy.context.object.modifiers["Solidify"].use_even_offset = True
    bpy.context.object.modifiers["Solidify"].thickness = thickness/100
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

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
    scene_collection = context.view_layer.layer_collection
    context.view_layer.active_layer_collection = scene_collection
    
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
        obj = context.active_object
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
            context.scene.collection.children.link(col)
            for index in g["children"]:
                col.objects.link(objects[index])
                context.scene.collection.objects.unlink(objects[index])
        except:
            pass
    
    # select newly imported objects
    mat = context.active_object.active_material
    for obj in context.selected_objects:
        obj.select_set(False)
    for obj in objects:
        obj.select_set(True)
    for obj in context.selected_objects:
        context.view_layer.objects.active = obj
        obj.name = mat.name
    bpy.ops.transform.resize(value=(0.1, 0.1, 0.1))
    bpy.ops.object.transform_apply(scale=True)
    
    return {"FINISHED"}

class Import_MinecraftModel(bpy.types.Operator, ImportHelper):
    bl_idname = "import.minecraftmodel"
    bl_label = "Import model"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = '.obj'
    
    filter_glob: StringProperty(
        default='*.obj',
        options={'HIDDEN'}
    )
    directory: StringProperty(
            subtype='DIR_PATH',
    )
    
    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
    )

    type: EnumProperty(
    default='one',
    items=[('one', 'Modelbench', ''),
            ('two', 'Blockbench', '')]
    )

    def execute(self, context):
        directory = self.directory
        for file_elem in self.files:
            filepath = os.path.join(directory, file_elem.name)
            bpy.ops.wm.obj_import(filepath=filepath, filter_glob='*.obj;*.mtl')
            colname = os.path.basename(filepath)
            colname = os.path.splitext(colname)[0]
            try:
                str_1 = str(filepath)
                str_list = list(str_1)
                nPos = str_list.index('.')
                str_list.insert(nPos, '_n')
                n_path = "".join(str_list)
                n_path = (n_path.replace('.obj', '.png'))
                n_image = bpy.data.images.load(filepath=n_path, check_existing=True)
                n_approve = 1
            except:
                n_approve = 0
            if self.type == 'one':
                bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')
                bpy.ops.object.transform_apply(rotation=True)
                bpy.ops.transform.resize(value=(0.8, 0.8, 0.8))
            elif self.type == 'two':
                bpy.ops.object.transform_apply(rotation=True)
                bpy.ops.transform.resize(value=(1.6, 1.6, 1.6))

            bpy.ops.object.transform_apply(scale=True) 
            for obj in context.selected_objects:
                context.view_layer.objects.active = obj
                mat = context.active_object.active_material
                obj.name = colname
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_smooth(use_auto_smooth=True)
            for obj in context.selected_objects:
                context.view_layer.objects.active = obj
                matnum = len(context.active_object.data.materials)
                for count in range(matnum):
                    context.object.active_material_index = count
                    mat = obj.active_material
                    fix_material.fixmaterial(mat)
                    fix_material.fixnormal(mat)
            objg = assetsDefs.collections().new(name=colname)
            context.scene.collection.children.link(objg)  # Add to outliner.
            for obj in context.selected_objects:
                assetsDefs.move_to_collection(obj, objg)
        return {'FINISHED'}
    def draw(self, context):
        layout = self.layout
        layout.label(text = "Model Type")
        layout.prop(self, "type", expand = True)

class ImportMinecraftJSON(Operator, ImportHelper):
    """Import Minecraft .json file"""
    bl_idname = "import.minecraftjson"
    bl_label = "Import JSON"
    bl_options = {"REGISTER", "UNDO"}

    # ImportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    import_uvs: BoolProperty(
        name="Import UVs",
        description="Import UVs",
        default=True,
    )

    # applies default shift from minecraft origin
    translate_origin_by_8: BoolProperty(
        name="Translate by (-8, -8, -8)",
        description="Recenter model with (-8, -8, -8) translation (Minecraft origin)",
        default=False,
    )

    recenter_to_origin: BoolProperty(
        name="Recenter to Origin",
        description="Recenter model median to origin",
        default=True,
    )

    def execute(self, context):
        args = self.as_keywords()
        try:
            return load(context, **args)
        except:
            return self.report({"ERROR"}, "This json.format cannot be imported!!!")

class Import_item(bpy.types.Operator, ImportHelper):
    bl_idname = "3d.item"
    bl_label = "Import image"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = '.png'
    
    filter_glob: StringProperty(
        default='*.png',
        options={'HIDDEN'}
    )
    directory: StringProperty(
            subtype='DIR_PATH',
    )
    
    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
    )
    
    x16: IntProperty(
        name="x16",
        min= 1,
        max= 8,
        default=1,
    )

    offset: BoolProperty(
        name="Item Offset",
        description="Set Item Offset",
        default=True,
    )

    def execute(self, context):
        directory = self.directory
        for file_elem in self.files:
            filepath = os.path.join(directory, file_elem.name)
            (path, file) = os.path.split(filepath)
            image = bpy.data.images.load(filepath=filepath, check_existing=True)
            script_file = os.path.realpath(__file__)
            script_directory = os.path.dirname(script_file)
            script_directory = os.path.normpath(script_directory)

            blendfile = os.path.join(script_directory, "Assets", "KEN_Assets.blend")
            section = "Object"
            blendfilename = "3D Plane"
            blendfilepath  = os.path.join(blendfile,section,blendfilename)
            blenddirectory = os.path.join(blendfile,section)
            bpy.ops.wm.append(filepath=blendfilepath,filename=blendfilename,directory=blenddirectory)
            for obj in context.selected_objects:
                context.view_layer.objects.active = obj
            obj.modifiers["3D Plane"]["Input_3"] = image
            width, height = image.size
            obj.modifiers["3D Plane"]["Input_11"] = self.x16
            if self.offset == True:
                obj.modifiers["3D Plane"]["Input_15"][0] = width*0.0275
                obj.modifiers["3D Plane"]["Input_15"][1] = height*0.0275
            str(file)
            obj.name = (file.replace('.png', ''))
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.object.delete()
        for file_elem in self.files:
            obj = context.scene.objects.get(file_elem.name.replace('.png', ''))
            if obj: obj.select_set(True)
        objg = assetsDefs.collections().new(name="Item Imported Group")
        context.scene.collection.children.link(objg)  # Add to outliner.
        for obj in context.selected_objects:
            assetsDefs.move_to_collection(obj, objg)
            context.view_layer.objects.active = obj
            
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "x16")
        layout.prop(self, "offset", toggle = True)

class Alpha_Import(bpy.types.Operator, ImportHelper):
    bl_idname = "alpha.import"
    bl_label = "Import image"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = '.png'

    filter_glob: StringProperty(
        default='*.png',
        options={'HIDDEN'},
    )

    directory: StringProperty(
            subtype='DIR_PATH',
    )
    
    files: CollectionProperty(
            type=bpy.types.OperatorFileListElement,
    )

    delete_faces: BoolProperty(
        name="Delete Faces",
        description="Delete Alpha Faces",
        default=False,
    )

    Solidify: BoolProperty(
        name="Add Solidify",
        description="Add Solidify",
        default=False,
    )
    thickness: FloatProperty(
        name="Solidify Thickness",
        description="Set Solidify Thickness",
        default=10,
    )

    def execute(self, context):
        directory = self.directory
        for file_elem in self.files:
            filepath = os.path.join(directory, file_elem.name)
            (path, file) = os.path.split(filepath)
            image = bpy.data.images.load(filepath=filepath, check_existing=True)
            try:
                str_1 = str(filepath)
                str_list = list(str_1)
                nPos = str_list.index('.')
                str_list.insert(nPos, '_n')
                n_path = "".join(str_list)
                n_image = bpy.data.images.load(filepath=n_path, check_existing=True)
                n_approve = 1
            except:
                n_approve = 0
                 
            width, height = image.size
                    
            script_file = os.path.realpath(__file__)
            script_directory = os.path.dirname(script_file)
            script_directory = os.path.normpath(script_directory)

            bpy.ops.mesh.primitive_plane_add(size=0.2, scale=(1, 1, 1))
            bpy.ops.transform.resize(value=(width/2, height/2, 1))
            bpy.ops.object.transform_apply(scale=True)
            obj = context.view_layer.objects.active
            str(file)
            name = (file.replace('.png', ''))
            obj.name = name
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.loopcut_slide(
                MESH_OT_loopcut = {
                    "number_cuts"           : width-1,
                    "smoothness"            : 0,     
                    "falloff"               : 'SMOOTH',  # Was 'INVERSE_SQUARE' that does not exist
                    "object_index"          : 0,
                    "edge_index"            : 1,
                    "mesh_select_mode_init" : (True, False, False)
                }
            )
            bpy.ops.mesh.loopcut_slide(
                MESH_OT_loopcut = {
                    "number_cuts"           : height-1,
                    "smoothness"            : 0,     
                    "falloff"               : 'SMOOTH',  # Was 'INVERSE_SQUARE' that does not exist
                    "object_index"          : 0,
                    "edge_index"            : 2,
                    "mesh_select_mode_init" : (True, False, False)
                }
            )
            bpy.ops.object.mode_set(mode = 'OBJECT')
            material = bpy.data.materials.get(name)
            if material is None:
                material = bpy.data.materials.new(name).use_nodes = True
                material = bpy.data.materials.get(name)
                context.active_object.data.materials.append(material)
                tex_node = material.node_tree.nodes.new('ShaderNodeTexImage')
                tex_node.location = assetsDefs.tex_node_loc
                tex_node.image = image
                bsdf = material.node_tree.nodes["Principled BSDF"]
                if n_approve == 1:
                    n_name = (file.replace('.png', '') + "_n.png")
                    n_node = material.node_tree.nodes.new('ShaderNodeTexImage')
                    n_node.location = assetsDefs.n_map_node_loc
                    n_node.image = n_image
                    n_node.name = "Normal Map Node"
                    bpy.data.materials[name].node_tree.nodes["Normal Map Node"].interpolation = 'Closest'
                    bpy.data.images[n_name].colorspace_settings.name = 'Non-Color'
                    n_map = material.node_tree.nodes.new('ShaderNodeNormalMap')
                    n_map.name = "Normal Map"
                    n_map.location = assetsDefs.n_node_loc
                    material.node_tree.links.new(n_map.inputs['Color'], n_node.outputs['Color'])
                    material.node_tree.links.new(bsdf.inputs['Normal'], n_map.outputs['Normal'])
                bpy.data.materials[name].node_tree.nodes["Image Texture"].interpolation = 'Closest'
                material.node_tree.links.new(bsdf.inputs['Base Color'], tex_node.outputs['Color'])
                material.node_tree.links.new(bsdf.inputs['Alpha'], tex_node.outputs['Alpha'])
                bpy.data.materials[name].node_tree.nodes["Principled BSDF"].subsurface_method = 'BURLEY'
                material.blend_method = 'HASHED'
            else:
                context.active_object.data.materials.append(material)
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT') 
            if self.delete_faces == True:
                editing.scale_uv(0.75)
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.object.mode_set(mode = 'OBJECT')
                editing.selectalpha(0.01)
                bpy.ops.mesh.delete(type='FACE')
            if self.Solidify == True:
                Solidify(self.thickness)
            bpy.ops.object.mode_set(mode = 'OBJECT')
        return {"FINISHED"}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "delete_faces", toggle = True)
        layout.prop(self, "Solidify", toggle = True)
        if self.Solidify == True:
            layout.prop(self, "thickness")

classes = (
            Import_MinecraftModel,
            ImportMinecraftJSON,
            Import_item,
            Alpha_Import,
          )        

register, unregister = bpy.utils.register_classes_factory(classes)