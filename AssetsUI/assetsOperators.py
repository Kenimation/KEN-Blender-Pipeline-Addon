import bpy
import os
from bpy_extras.io_utils import ImportHelper
from . import assetsUtil
import bmesh
from pathlib import Path
from bpy.types import Operator, OperatorFileListElement
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                      operators
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ScaleUV(bpy.types.Operator):
    bl_idname = "scale.uv"
    bl_label = "Scale UV"
    bl_options = {'REGISTER', 'UNDO'}

    factor: FloatProperty(
        name="Scale UV Faces Factor",
        description="Set Scale UV Faces Factor",
        default=0.25,
        min = 0,
        max = 1
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "factor", slider = True)

    def execute(self, context):
        try:
            assetsUtil.scale_uv(self.factor)
        except:
            print("Selected object can't not select uv.")
        return {'FINISHED'}
    
class SelectalphaUV(bpy.types.Operator):
    bl_idname = "select.alphauv"
    bl_label = "Select Alpha UV"
    bl_options = {'REGISTER', 'UNDO'}

    threshold: FloatProperty(
        name="Alpha threshold",
        description="Set alpha threshold",
        default=0.01,
        min = 0,
        max = 1
    )

    delete_faces: BoolProperty(
        name="Delete Faces",
        description="Delete Alpha Faces",
        default=False,
    )

    scale_uv: BoolProperty(
        name="Scale UV Faces",
        description="Scale UV Faces",
        default=False,
    )

    factor: FloatProperty(
        name="Scale UV Faces Factor",
        description="Set Scale UV Faces Factor",
        default=0.25,
        min = 0,
        max = 1
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "threshold", slider = True)
        layout.prop(self, "delete_faces")
        layout.prop(self, "scale_uv")
        if self.scale_uv == True:
            layout.prop(self, "factor", slider = True)

    def execute(self, context):
        try:
            if self.scale_uv == True:
                assetsUtil.scale_uv(self.factor)
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            assetsUtil.selectalpha(self.threshold)
            if self.delete_faces == True:
                bpy.ops.mesh.delete(type='FACE')

        except:
             print("Selected object can't not select uv.")

        return {'FINISHED'}

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
            for obj in bpy.context.selected_objects:
                bpy.context.view_layer.objects.active = obj
                mat = bpy.context.active_object.active_material
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
                    assetsUtil.fixmaterial(mat)
                    assetsUtil.fixnormal(mat)
            objg = assetsUtil.collections().new(name=colname)
            context.scene.collection.children.link(objg)  # Add to outliner.
            for obj in context.selected_objects:
                assetsUtil.move_to_collection(obj, objg)
        return {'FINISHED'}
    def draw(self, context):
        layout = self.layout
        layout.label(text = "Model Type")
        layout.prop(self, "type", expand = True)

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

            blendfile = os.path.join(script_directory, "Assets", "Asset.blend")
            section = "Object"
            blendfilename = "3D Plane"
            blendfilepath  = os.path.join(blendfile,section,blendfilename)
            blenddirectory = os.path.join(blendfile,section)
            bpy.ops.wm.append(filepath=blendfilepath,filename=blendfilename,directory=blenddirectory)
            for obj in bpy.context.selected_objects:
                bpy.context.view_layer.objects.active = obj
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
            obj = bpy.context.scene.objects.get(file_elem.name.replace('.png', ''))
            if obj: obj.select_set(True)
        objg = assetsUtil.collections().new(name="Item Imported Group")
        context.scene.collection.children.link(objg)  # Add to outliner.
        for obj in context.selected_objects:
            assetsUtil.move_to_collection(obj, objg)
            bpy.context.view_layer.objects.active = obj
            
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
            obj = bpy.context.view_layer.objects.active
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
                bpy.context.active_object.data.materials.append(material)
                tex_node = material.node_tree.nodes.new('ShaderNodeTexImage')
                tex_node.location = assetsUtil.tex_node_loc
                tex_node.image = image
                bsdf = material.node_tree.nodes["Principled BSDF"]
                if n_approve == 1:
                    n_name = (file.replace('.png', '') + "_n.png")
                    n_node = material.node_tree.nodes.new('ShaderNodeTexImage')
                    n_node.location = assetsUtil.n_map_node_loc
                    n_node.image = n_image
                    n_node.name = "Normal Map Node"
                    bpy.data.materials[name].node_tree.nodes["Normal Map Node"].interpolation = 'Closest'
                    bpy.data.images[n_name].colorspace_settings.name = 'Non-Color'
                    n_map = material.node_tree.nodes.new('ShaderNodeNormalMap')
                    n_map.name = "Normal Map"
                    n_map.location = assetsUtil.n_node_loc
                    material.node_tree.links.new(n_map.inputs['Color'], n_node.outputs['Color'])
                    material.node_tree.links.new(bsdf.inputs['Normal'], n_map.outputs['Normal'])
                bpy.data.materials[name].node_tree.nodes["Image Texture"].interpolation = 'Closest'
                material.node_tree.links.new(bsdf.inputs['Base Color'], tex_node.outputs['Color'])
                material.node_tree.links.new(bsdf.inputs['Alpha'], tex_node.outputs['Alpha'])
                bpy.data.materials[name].node_tree.nodes["Principled BSDF"].subsurface_method = 'BURLEY'
                material.blend_method = 'HASHED'
            else:
                bpy.context.active_object.data.materials.append(material)
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT') 
            if self.delete_faces == True:
                assetsUtil.scale_uv(0.75)
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.object.mode_set(mode = 'OBJECT')
                assetsUtil.selectalpha(0.01)
                bpy.ops.mesh.delete(type='FACE')
            if self.Solidify == True:
                assetsUtil.Solidify(self.thickness)
            bpy.ops.object.mode_set(mode = 'OBJECT')
        return {"FINISHED"}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "delete_faces", toggle = True)
        layout.prop(self, "Solidify", toggle = True)
        if self.Solidify == True:
            layout.prop(self, "thickness")

class Copyloc(bpy.types.Operator):
    bl_idname = "copy.loc"
    bl_label = "Copy Location"
    bl_options = {'REGISTER', 'UNDO'}
    
    x: BoolProperty(
        name="X",
        description="Copy X.",
        default=True,
    )
    y: BoolProperty(
        name="Y",
        description="Copy Y",
        default=True,
    )
    z: BoolProperty(
        name="Z",
        description="Copy Z.",
        default=True,
    )

    def execute(self, context):
        try:
            if self.x == True:
                assetsUtil.copytransform("loc", "x")
            if self.y == True:
                assetsUtil.copytransform("loc", "y")
            if self.z == True:
                assetsUtil.copytransform("loc", "z")
        except:
            self.report({"ERROR"}, "Cannot copy location!!!")
        return {'FINISHED'}
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.column_flow(columns = 3)
        row.prop(self, "x", toggle = True)
        row.prop(self, "y", toggle = True)
        row.prop(self, "z", toggle = True)
     
class Copyrota(bpy.types.Operator):
    bl_idname = "copy.rota"
    bl_label = "Copy Rotation"
    bl_options = {'REGISTER', 'UNDO'}
    
    x: BoolProperty(
        name="X",
        description="Copy X.",
        default=True,
    )
    y: BoolProperty(
        name="Y",
        description="Copy Y",
        default=True,
    )
    z: BoolProperty(
        name="Z",
        description="Copy Z.",
        default=True,
    )

    def execute(self, context):
        try:
            if self.x == True:
                assetsUtil.copytransform("rota", "x")
            if self.y == True:
                assetsUtil.copytransform("rota", "y")
            if self.z == True:
                assetsUtil.copytransform("rota", "z")
        except:
            self.report({"ERROR"}, "Cannot copy rotation!!!")
        return {'FINISHED'}
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.column_flow(columns = 3)
        row.prop(self, "x", toggle = True)
        row.prop(self, "y", toggle = True)
        row.prop(self, "z", toggle = True)
    
class Copysize(bpy.types.Operator):
    bl_idname = "copy.size"
    bl_label = "Copy Size"
    bl_options = {'REGISTER', 'UNDO'}
    
    x: BoolProperty(
        name="X",
        description="Copy X.",
        default=True,
    )
    y: BoolProperty(
        name="Y",
        description="Copy Y",
        default=True,
    )
    z: BoolProperty(
        name="Z",
        description="Copy Z.",
        default=True,
    )

    def execute(self, context):
        try:
            if self.x == True:
                assetsUtil.copytransform("size", "x")
            if self.y == True:
                assetsUtil.copytransform("size", "y")
            if self.z == True:
                assetsUtil.copytransform("size", "z")
        except:
            self.report({"ERROR"}, "Cannot copy size!!!")
        return {'FINISHED'}
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.column_flow(columns = 3)
        row.prop(self, "x", toggle = True)
        row.prop(self, "y", toggle = True)
        row.prop(self, "z", toggle = True)

class Copytransform(bpy.types.Operator):
    bl_idname = "copy.trans"
    bl_label = "Copy Transform"
    bl_options = {'REGISTER', 'UNDO'}
    
    copyloc: BoolProperty(
        name="Location",
        description="Copy Location.",
        default=True,
    )
    copyrota: BoolProperty(
        name="Rotation",
        description="Copy Rotation",
        default=True,
    )
    copysize: BoolProperty(
        name="Size",
        description="Copy Size.",
        default=True,
    )
    x: BoolProperty(
        name="X",
        description="Copy X.",
        default=True,
    )
    y: BoolProperty(
        name="Y",
        description="Copy Y",
        default=True,
    )
    z: BoolProperty(
        name="Z",
        description="Copy Z.",
        default=True,
    )

    def execute(self, context):
        try:
            if self.copyloc == True:
                if self.x == True:
                    assetsUtil.copytransform("loc", "x")
                if self.y == True:
                    assetsUtil.copytransform("loc", "y")
                if self.z == True:
                    assetsUtil.copytransform("loc", "z")
            if self.copyrota == True:
                if self.x == True:
                    assetsUtil.copytransform("rota", "x")
                if self.y == True:
                    assetsUtil.copytransform("rota", "y")
                if self.z == True:
                    assetsUtil.copytransform("rota", "z")
            if self.copysize == True:  
                if self.x == True:
                    assetsUtil.copytransform("size", "x")
                if self.y == True:
                    assetsUtil.copytransform("size", "y")
                if self.z == True:
                    assetsUtil.copytransform("size", "z")
        except:
            self.report({"ERROR"}, "Cannot copy transform!!!")
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.column_flow(columns = 3)
        row = box.row()
        row.prop(self, "copyloc", toggle = True)
        row.prop(self, "copyrota", toggle = True)
        row.prop(self, "copysize", toggle = True)
        row = box.row()
        row.prop(self, "x", toggle = True)
        row.prop(self, "y", toggle = True)
        row.prop(self, "z", toggle = True)

class RestCursor(bpy.types.Operator):
    bl_idname = "rest.cursor"
    bl_label = "Rest Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            bpy.context.scene.cursor.location[0] = 0
            bpy.context.scene.cursor.location[1] = 0
            bpy.context.scene.cursor.location[2] = 0
        except:
            self.report({"ERROR"}, "Cannot Rest Cursor!!!")
        return {'FINISHED'}
  
class Fix_Material(bpy.types.Operator):
    bl_idname = "fix.material"
    bl_label = "Fix Material"
    bl_options = {'REGISTER', 'UNDO'}

    type: bpy.props.StringProperty(options={'HIDDEN'})
    mat: bpy.props.StringProperty(options={'HIDDEN'})

    ramp: BoolProperty(
        name="Specular/Roughness",
        description="Fix Specular/Roughness.",
        default=False,
    )

    bump: BoolProperty(
        name="Fix Bump",
        description="Fix Bump.",
        default=False,
    )

    nomral: BoolProperty(
        name="Fix Nomral",
        description="Fix Nomral.",
        default=False,
    )

    SSS: BoolProperty(
        name="Subsurface",
        description="Fix Subsurface.",
        default=False,
    )
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "ramp", toggle = True)
        layout.prop(self, "bump", toggle = True)
        layout.prop(self, "nomral", toggle = True)
        layout.prop(self, "SSS", toggle = True)

    def execute(self, context):
        try:
            mat_data = bpy.data.materials[self.mat]
        except:
            mat_data = ""

        if self.type == "obj":
            for obj in context.selected_objects:
                context.view_layer.objects.active = obj
                actmat = context.object.active_material_index
                matnum = len(context.active_object.data.materials)
                for count in range(matnum):
                    context.object.active_material_index = count
                    mat = obj.active_material
                    try:
                        assetsUtil.fixmaterial(mat)
                        if self.ramp == True:
                            assetsUtil.fixRamp(mat)
                        if self.bump == True:
                            assetsUtil.fixBump(mat)
                        if self.nomral == True:
                            assetsUtil.fixnormal(mat)
                        if self.SSS == True:
                            assetsUtil.fixSSS(mat, 1)
                        else:
                            assetsUtil.fixSSS(mat, 0)
                    except:
                        continue
                        
                context.object.active_material_index = actmat

        if self.type == "index":
            mat = mat_data
            assetsUtil.fixmaterial(mat)
            if self.ramp == True:
                assetsUtil.fixRamp(mat)
            if self.bump == True:
                assetsUtil.fixBump(mat)
            if self.nomral == True:
                assetsUtil.fixnormal(mat)
            if self.SSS == True:
                assetsUtil.fixSSS(mat, 1)
            else:
                assetsUtil.fixSSS(mat, 0)

        if self.type == "scene":
            for mat in bpy.data.materials:
                try:
                    assetsUtil.fixmaterial(mat)
                    if self.ramp == True:
                        assetsUtil.fixRamp(mat)
                    if self.bump == True:
                        assetsUtil.fixBump(mat)
                    if self.nomral == True:
                        assetsUtil.fixnormal(mat)
                    if self.SSS == True:
                        assetsUtil.fixSSS(mat, 1)
                    else:
                        assetsUtil.fixSSS(mat, 0)
                except:
                    continue
        return {'FINISHED'}
    
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
		conv_res = assetsUtil.convert_mtl(self.filepath)
		try:
			if conv_res is None:
				pass  # skipped, no issue anyways.
			elif conv_res is False:
				self.report({"WARNING"}, "MTL conversion failed!")

			res = None
			if assetsUtil.min_bv((3, 5)):
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
				assetsUtil.fixmaterial(mat)
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
					assetsUtil.fixRamp(mat)
			except:
				pass
		if not mat:
			return
		obj.name = assetsUtil.nameGeneralize(mat.name)
		bpy.ops.object.transform_apply(rotation=True)

	def split_world_by_material(self, context):
                
		"""2.8-only function, split combined object into parts by material"""
		world_name = os.path.basename(self.filepath)
		world_name = os.path.splitext(world_name)[0]

		# Create the new world collection
		name = world_name + "_Map"
		worldg = assetsUtil.collections().new(name=name)
		context.scene.collection.children.link(worldg)  # Add to outliner.

		for obj in context.selected_objects:
			assetsUtil.move_to_collection(obj, worldg)

		# Force renames based on material, as default names are not useful.
		for obj in worldg.objects:
			self.obj_to_material(obj)
		if self.separate_material == False:
			for obj in bpy.context.selected_objects:
				bpy.context.view_layer.objects.active = obj
			bpy.ops.object.make_links_data(type='MATERIAL')
			bpy.ops.outliner.orphans_purge()
			obj.active_material.name = name + "_Blocks"

class Alpha_Delete(bpy.types.Operator):
    bl_idname = "alpha.delete"
    bl_label = "Alpha.delete"
    bl_options = {'REGISTER', 'UNDO'}
 
    threshold: FloatProperty(
        name="Alpha threshold",
        description="Set alpha threshold",
        default=0.01,
        min = 0,
        max = 1
    )

    scale_uv: BoolProperty(
        name="Scale UV Faces",
        description="Scale UV Faces",
        default=False,
    )

    factor: FloatProperty(
        name="Scale UV Faces Factor",
        description="Set Scale UV Faces Factor",
        default=0.25,
        min = 0,
        max = 1
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "threshold", slider = True)
        layout.prop(self, "delete_faces")
        layout.prop(self, "scale_uv")
        if self.scale_uv == True:
            layout.prop(self, "factor", slider = True)

    def execute(self, context):
        try:
            for obj in bpy.context.selected_objects:
                if self.scale_uv == True:
                    assetsUtil.scale_uv(self.factor)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.context.scene.tool_settings.uv_select_mode = 'FACE'
                bpy.ops.uv.select_all(action='SELECT')
                bpy.ops.object.mode_set(mode = 'OBJECT')
                assetsUtil.selectalpha(self.threshold)
                bpy.ops.mesh.delete(type='FACE')
                bpy.ops.object.mode_set(mode = 'OBJECT')
        except:
            pass

        return {'FINISHED'}

class ImportMinecraftJSON(Operator, ImportHelper):
    """Import Minecraft .json file"""
    bl_idname = "minecraft.import_json"
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
            return assetsUtil.load(context, **args)
        except:
            return self.report({"ERROR"}, "This json.format cannot be imported!!!")

class Open_Image(bpy.types.Operator, ImportHelper):
    bl_idname = "open.image"
    bl_label = "Open Image"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = '.png'

    filter_glob: StringProperty(
        default='*.png',
        options={'HIDDEN'},
    )

    directory: StringProperty(
            subtype='DIR_PATH',
    )

    img: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        (path, file) = os.path.split(self.filepath)
        image = bpy.data.images.load(filepath=self.filepath, check_existing=True)
        mat = bpy.context.active_object.active_material
        script_file = os.path.realpath(__file__)
        script_directory = os.path.dirname(script_file)
        script_directory = os.path.normpath(script_directory)
        mat.node_tree.nodes[self.img].image = image
        image.reload()
        return {"FINISHED"}

class Addconstraints(bpy.types.Operator):
    bl_idname = "add.constraints"
    bl_label = "Add Constraints"
    bl_options = {'REGISTER', 'UNDO'}

    type: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        try:
            if self.type == 'CHILD_OF':
                if bpy.context.object.mode == 'OBJECT':
                    bpy.ops.object.constraint_add(type='CHILD_OF')
                elif bpy.context.object.mode == 'POSE':
                    bpy.ops.pose.constraint_add(type='CHILD_OF')
            if self.type == 'DAMPED_TRACK':
                if bpy.context.object.mode == 'OBJECT':
                    bpy.ops.object.constraint_add(type='DAMPED_TRACK')
                elif bpy.context.object.mode == 'POSE':
                    bpy.ops.pose.constraint_add(type='DAMPED_TRACK')
            if self.type == 'FOLLOW_PATH':
                if bpy.context.object.mode == 'OBJECT':
                    bpy.ops.object.constraint_add(type='FOLLOW_PATH')
                elif bpy.context.object.mode == 'POSE':
                    bpy.ops.pose.constraint_add(type='FOLLOW_PATH')
        except:
            self.report({"ERROR"}, "Cannot add Child Of!!!")
        return {"FINISHED"}
    
class Set_inverse(bpy.types.Operator):
    bl_idname = "set.inverse"
    bl_label = "Set Inverse"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            bpy.ops.constraint.childof_set_inverse(constraint=self.id, owner='OBJECT')
        elif bpy.context.object.mode == 'POSE':
            bpy.ops.constraint.childof_set_inverse(constraint=self.id, owner='BONE')
        return {"FINISHED"}
 
class Clear_inverse(bpy.types.Operator):
    bl_idname = "clear.inverse"
    bl_label = "Clear Inverse"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            bpy.ops.constraint.childof_clear_inverse(constraint=self.id, owner='OBJECT')    
        elif bpy.context.object.mode == 'POSE':
            bpy.ops.constraint.childof_clear_inverse(constraint=self.id, owner='BONE')
        return {"FINISHED"}

class All_constraint(bpy.types.Operator):
    bl_idname = "all.constraint"
    bl_label = "All Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    type: bpy.props.IntProperty(options={'HIDDEN'})

    def execute(self, context):
        if self.type == 0:
            obj = context.view_layer.objects.active
            for id in obj.modifiers[:]:
                bpy.ops.object.modifier_remove(modifier=id.name)
        if self.type == 1:
            obj = context.object
            bones = context.active_pose_bone
            if obj.mode != 'POSE':
                con = obj.constraints
                for id in con[:]:
                    bpy.ops.constraint.delete(constraint=id.name)
            elif obj.mode == 'POSE':
                con = bones.constraints
                for id in con[:]:
                    bpy.ops.constraint.delete(constraint=id.name)
        if self.type == 2:
            obj = context.view_layer.objects.active
            for id in obj.modifiers[:]:
                bpy.ops.object.modifier_apply(modifier=id.name)
        if self.type == 3:
            obj = context.object
            bones = context.active_pose_bone
            if obj.mode != 'POSE':
                con = obj.constraints
                for id in con[:]:
                    bpy.ops.constraint.apply(constraint=id.name)
            elif obj.mode == 'POSE':
                con = bones.constraints
                for id in con[:]:
                    bpy.ops.constraint.apply(constraint=id.name)
        return {"FINISHED"}

class Delete_constraint(bpy.types.Operator):
    bl_idname = "delete.constraint"
    bl_label = "Delete Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            bpy.ops.constraint.delete(constraint=self.id, owner='OBJECT')
            bpy.ops.object.modifier_remove(modifier=self.id)
        elif bpy.context.object.mode == 'POSE':
            bpy.ops.constraint.delete(constraint=self.id, owner='BONE')
        return {"FINISHED"}

class Apply_constraint(bpy.types.Operator):
    bl_idname = "apply.constraint"
    bl_label = "Apply Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            bpy.ops.constraint.apply(constraint=self.id, owner='OBJECT')
            bpy.ops.object.modifier_apply(modifier=self.id)
        elif bpy.context.object.mode == 'POSE':
            bpy.ops.constraint.apply(constraint=self.id, owner='BONE')
        return {"FINISHED"}

class Copy_constraint(bpy.types.Operator):
    bl_idname = "copy.constraint"
    bl_label = "Copy Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            bpy.ops.constraint.copy(constraint=self.id, owner='OBJECT')
            bpy.ops.object.modifier_copy(modifier=self.id)
        elif bpy.context.object.mode == 'POSE':
            bpy.ops.constraint.copy(constraint=self.id, owner='BONE')
        return {"FINISHED"}

class Disable_constraint(bpy.types.Operator):
    bl_idname = "disable.constraint"
    bl_label = "Disable Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        if bpy.context.object.mode == 'OBJECT':
            ob = bpy.context.object
            constraint = ob.constraints.get(self.id)
            if constraint:
                mw = ob.matrix_world.copy()
                constraint.influence = 0
                ob.matrix_world = mw
        elif bpy.context.object.mode == 'POSE':
            bone = bpy.context.active_pose_bone
            constraint = bone.constraints.get(self.id)
            if constraint:
                mw = bone.matrix.copy()
                constraint.influence = 0
                bone.matrix = mw
        return {"FINISHED"}

class New_Material(bpy.types.Operator):
    bl_idname = "new.material"
    bl_label = "New Material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            ob = bpy.context.active_object
            # Get material
            mat = bpy.data.materials.new(name="Material")
            mat.use_nodes = True

            # Assign it to object
            if ob.data.materials:
                # assign to 1st material slot
                slot = bpy.context.object.active_material_index
                ob.data.materials[slot] = mat
            else:
                # no slots
                ob.data.materials.append(mat)
            assetsUtil.fixmaterial()
        except:
             pass
        return {"FINISHED"}

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
        tex_node.location = assetsUtil.tex_node_loc
        for node in mat.node_tree.nodes:
            if node.name == "Principled BSDF":
                bsdf = node
                node_tree.links.new(bsdf.inputs['Base Color'], tex_node.outputs['Color'])
                node_tree.links.new(bsdf.inputs['Subsurface Color'], tex_node.outputs['Color'])

        return {"FINISHED"}

class Operators(bpy.types.Operator):
    bl_idname = "bpy.ops"
    bl_label = "Bpy Operators"

    id: bpy.props.StringProperty(options={'HIDDEN'})
    object: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        scene = context.scene
        if self.id == "emptyselect":
            bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects

            for obj in bpy.context.scene.objects:
                if obj.type == scene.Object_Type:
                    obj.select_set(True)

        if self.id == "DampedTrackLoop":
            rig = context.active_object
            obj = context.selected_objects
            prefix = scene.Track_Prefix
            if rig.mode == 'POSE':
                selected_bones = context.selected_pose_bones
                for bone in selected_bones:
                    constraint = bone.constraints.new(type = 'DAMPED_TRACK')
                    for obj in context.selected_objects:
                        if obj != rig:
                            constraint.target = obj
                            constraint.subtarget = prefix + bone.name

        if self.id == "ConstraintsDriver":
            rig = bpy.context.active_object
            obj = bpy.context.selected_objects

            if rig.mode == 'POSE':                
                selected_bones = bpy.context.selected_pose_bones     
                for bone in selected_bones:
                    constraint = bone.constraints.get(scene.Constraints_Type)
                    if constraint is not None:
                        constraint = constraint.driver_add("influence")
                        constraint.driver.type="AVERAGE"
                        constraint.driver.variables.new()
                        constraint.driver.variables[0].targets[0].id = rig
                        constraint.driver.variables[0].targets[0].data_path = scene.Rig_Prop

        if self.id == "ConstraintsDriverRemove":
            rig = bpy.context.active_object
            obj = bpy.context.selected_objects

            if rig.mode == 'POSE':                
                selected_bones = bpy.context.selected_pose_bones     
                for bone in selected_bones:
                    constraint = bone.constraints.get(scene.Constraints_Type)
                    if constraint is not None:
                        constraint = constraint.driver_remove("influence")           
        
        if self.id == "VertexGroupAdd":

            if scene.VertexGroupMenu == 'one':
                Name = scene.VertexGroupName
            if scene.VertexGroupMenu == 'two':
                Part = ['Head', 'Body']
                if scene.VertexGroupPart in Part:
                    Name = str(scene.VertexGroupPart)
                else:
                    if scene.VertexGroupLR == 'one':
                        Name = 'L.'+str(scene.VertexGroupPart)
                    elif scene.VertexGroupLR == 'two':
                        Name = 'R.'+str(scene.VertexGroupPart)

            new_vertex_group = context.active_object.vertex_groups.new(name=Name)
            mesh = context.active_object.data
            vertices = mesh.vertices
            vertex_indices = [v.index for v in vertices]
            for index in vertex_indices:
                new_vertex_group.add([index], 1.0, 'ADD')


        if self.id == "VertexGroupLoop":
            Count = scene.VertexGroupCount
            Name = scene.VertexGroupName
            if scene.VertexGroupMiiror == True:
                for num in range(Count*2, 0, 2):
                    pair = [num, num + 1]
                    new_vertex_group = bpy.context.active_object.vertex_groups.new(name=Name)
                    vertex_group_data = pair
                    new_vertex_group.add(vertex_group_data, 1.0, 'ADD')
            else:
                for num in range(0, Count*2, 2):
                    pair = [num, num + 1]
                    new_vertex_group = bpy.context.active_object.vertex_groups.new(name=Name)
                    vertex_group_data = pair
                    new_vertex_group.add(vertex_group_data, 1.0, 'ADD')
             
        if self.id == "jump_frame":
            frame_number = self.object
            bpy.context.scene.frame_set(round(float(frame_number)))
            
        if self.id == "new_coll":
            collection = bpy.data.collections.new(self.object)
            bpy.context.scene.collection.children.link(collection)
        try:
            light = bpy.data.lights[self.object]
            if self.id == "light+1":
                power = light.energy
                light.energy = power*2
            if self.id == "light+0.5":
                power = light.energy
                light.energy = power*1.41421
            if self.id == "light-1":
                power = light.energy
                light.energy = power*0.5
            if self.id == "light-0.5":
                power = light.energy
                light.energy = power/1.41421
        except:
            pass
        if self.id == "new marker":
            if self.object == "":
                name = "None"
            else:
                name = self.object
            scene.timeline_markers.new(name, frame=scene.frame_current)
        if self.id == "del marker":
            m = scene.timeline_markers[self.object]
            scene.timeline_markers.remove(m)
        if self.id == "select":
            for item in context.scene.objects:
                item.select_set(False)
            bpy.context.view_layer.objects.active = bpy.data.objects[self.object]
            bpy.data.objects[self.object].select_set(state = True)
        if self.id == "select light":
            for ob in bpy.context.scene.objects:
                ob.select_set(ob.type == "LIGHT")
        if self.id == "select cam":
            for ob in bpy.context.scene.objects:
                ob.select_set(ob.type == "CAMERA")
        if self.id == "duplicate":
            obj = bpy.context.active_object


            new_obj = bpy.data.objects[self.object].copy()
            new_obj.data = bpy.data.objects[self.object].data.copy()
            try:
                if bpy.data.objects[self.object].animation_data is not None:
                    new_obj.animation_data_clear()
                    new_obj.animation_data_create()
                    new_obj.animation_data.action = bpy.data.objects[self.object].animation_data.action.copy()
            except:
                pass

            bpy.context.scene.collection.objects.link(new_obj)
            # Select the new object and make it the active object
            if obj:
                obj.select_set(False)
            bpy.context.view_layer.objects.active = new_obj
            new_obj.select_set(True)
        return {"FINISHED"}

class Solo_Light(bpy.types.Operator):
    bl_idname = "solo.light"
    bl_label = "Solo Light"
    bl_options = {'REGISTER', 'UNDO'}

    light: bpy.props.StringProperty(options={'HIDDEN'})
    solo: bpy.props.BoolProperty(options={'HIDDEN'})

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

class Data_Blend(bpy.types.Operator):
    bl_idname = "data.blend"
    bl_label = "Data blend"
    bl_options = {'REGISTER', 'UNDO'}

    blend: bpy.props.StringProperty(options={'HIDDEN'})
    type: bpy.props.StringProperty(options={'HIDDEN'})
    subtype: bpy.props.StringProperty(options={'HIDDEN'})
    toggle: bpy.props.BoolProperty(options={'HIDDEN'})

    def execute(self, context):
        if self.type == "img":
            try:
                img_data = bpy.data.images[self.blend]
            except:
                pass
            if self.subtype == "reload":
                img_data.reload
            if self.subtype == "pack":
                if img_data.packed_files:
                    img_data.unpack(method='USE_ORIGINAL')
                else:
                    img_data.pack()
            if self.subtype == "remove":
                bpy.data.images.remove(img_data)
            if self.subtype == "clean":
                img_list = []

                for img in bpy.data.images:
                    if img.use_fake_user == False:
                        img_name = img.name.removesuffix(".png" or ".jpg")
                        if img_name.split(".")[0] is not None:
                            img.name = img_name.split(".")[0]
                            img_list.append(img.name)
                        if img_name == img_name.split(".")[0]:
                            img_list.append(img.name)
                        
                for material in bpy.data.materials:
                    node_tree = material.node_tree
                    if node_tree:
                        for node in node_tree.nodes:
                            if node.type == "TEX_IMAGE" and node.image.name not in img_list:
                                node.image = bpy.data.images[node.image.name.split(".")[0]]

                for node_groups in bpy.data.node_groups:
                    for node in node_groups.nodes:
                        if node.type == "IMAGE_TEXTURE" and node.inputs[0].default_value.name not in img_list:
                            node.inputs[0].default_value = bpy.data.images[node.inputs[0].default_value.name.split(".")[0]]

                for img in bpy.data.images:
                    if img.use_fake_user == False:
                        if img.name not in img_list:
                            if img.name != img.name.split(".")[0]:
                                bpy.data.images.remove(img)

                img_list.clear()

        if self.type == "mat":
            try:
                obj = context.view_layer.objects.active
                mat_data = bpy.data.materials[self.blend]
            except:
                pass
            if self.subtype == "replace":
                # Assign it to object
                for obj in context.selected_objects:
                    try:
                        context.view_layer.objects.active = obj
                        if obj.data.materials:
                            # assign to 1st material slot
                            slot = context.object.active_material_index
                            obj.data.materials[slot] = mat_data
                        else:
                            # no slots
                            obj.data.materials.append(mat_data)
                    except:
                        continue
            if self.subtype == "append":
                for obj in context.selected_objects:
                    try:
                        context.view_layer.objects.active = obj
                        obj.data.materials.append(mat_data)
                    except:
                        continue
            if self.subtype == "del":
                selected_objects = context.selected_objects
                for obj in selected_objects:
                    # Set the object as the active object in the current view layer
                    context.view_layer.objects.active = obj

                    # Remove all material slots from the object
                    for i in reversed(range(len(obj.material_slots))):
                        bpy.ops.object.material_slot_remove()

            if self.subtype == "remove":
                bpy.data.materials.remove(mat_data)
            if self.subtype == "single":
                slot = obj.active_material_index

                new_mat = mat_data.copy()

                obj.data.materials[slot] = new_mat

            if self.subtype == "duplicate":
                new_mat = mat_data.copy()

                obj.data.materials.append(new_mat)

            if self.subtype == "select":   
                obj = bpy.data.objects
                for ob in obj:
                    if ob.type == 'MESH':
                        try:
                            for m in ob.material_slots:
                                if m.material == mat_data:
                                    ob.select_set(True)
                        except:
                            continue
                                
            if self.subtype == "clean":
                mat_list = []

                for mat in bpy.data.materials:
                    if mat.use_fake_user == False:
                        if mat.name == mat.name.split(".")[0]:
                            mat_list.append(mat.name)

                for obj in bpy.data.objects:
                    if obj.type == "MESH" and obj.data.materials:
                        try:
                            for mat_slot in obj.material_slots:
                                if mat_slot.material.name not in mat_list and mat_slot.material.use_fake_user == False:
                                    try:
                                        mat_slot.material = bpy.data.materials[mat_slot.material.name.split(".")[0]]
                                    except:
                                        mat_slot.material.name = mat_slot.material.name.split(".")[0]
                        except:
                            pass

                for node_groups in bpy.data.node_groups:
                    for node in node_groups.nodes:
                        if node.type == "SET_MATERIAL" and node.inputs[2].default_value not in mat_list:
                            try:
                                node.inputs[2].default_value = bpy.data.materials[node.inputs[2].default_value.name.split(".")[0]]
                            except:
                                node.inputs[2].default_value.name = node.inputs[2].default_value.name.split(".")[0]
                            
                for mat in bpy.data.materials:
                    if mat.use_fake_user == False:
                        if mat.name not in mat_list:
                            if mat.name != mat.name.split(".")[0]:
                                bpy.data.materials.remove(mat)
                mat_list.clear()

        if self.type == "light":
            if self.subtype == "remove":
                light_data = bpy.data.lights[self.blend]
                bpy.data.lights.remove(light_data)
            if self.subtype == "removeall":
                for light in bpy.data.lights:
                    bpy.data.lights.remove(light)

        if self.type == "cam":
            try:
                cam_data = bpy.data.cameras[self.blend]
            except:
                pass
            if self.subtype == "remove":
                bpy.data.cameras.remove(cam_data)
            if self.subtype == "view":
                context.scene.camera = bpy.data.objects[self.blend]
        
        if self.type == "coll":
            try:
                coll = bpy.data.collections[self.blend]
            except:
                pass
            if self.subtype == "remove":
                bpy.data.collections.remove(coll)
            if self.subtype == "removeall":
                for coll in bpy.data.collections:
                    bpy.data.collections.remove(coll)
            if self.subtype == "clean":
                for obj in coll.objects:
                    bpy.data.objects.remove(obj, do_unlink=True)

        return {"FINISHED"}

class Open_ImageFile(bpy.types.Operator, ImportHelper):
    bl_idname = "open.imagefile"
    bl_label = "Open Image File"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = '.png'

    filter_glob: StringProperty(
        default='*.png',
        options={'HIDDEN'},
    )

    directory: StringProperty(
            subtype='DIR_PATH',
    )

    id: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        (path, file) = os.path.split(self.filepath)
        try:
            bpy.data.images.load(filepath=self.filepath, check_existing=True)
            script_file = os.path.realpath(__file__)
            script_directory = os.path.dirname(script_file)
            script_directory = os.path.normpath(script_directory)
        except:
             pass
        return {"FINISHED"}

class Crease(bpy.types.Operator):
    bl_idname = "set.crease"
    bl_label = "Set Crease"
    bl_options = {'REGISTER', 'UNDO'}

    items = [
        ('All', 'All', ''),
        ('Selected Elements', 'Selected Elements', '')
    ]

    mode: bpy.props.IntProperty(options={'HIDDEN'})
    type: bpy.props.StringProperty(options={'HIDDEN'})

    whoToInfluence: bpy.props.EnumProperty(
        description = "Influence all / selection",
        name        = "whoToInfluence",
        items       = items,
        default     = 'Selected Elements'
    )

    def execute(self, context):
        o  = bpy.context.object
        d  = o.data
        bm = bmesh.from_edit_mesh(d)

        if self.type == 'set':
            type = 1
        elif self.type == 'clear':
            type = 0

        if self.mode == 1:

            creaseLayer = bm.verts.layers.crease.verify()

            if self.whoToInfluence == 'Selected Elements':
                selectedVerts = [v for v in bm.verts if v.select]
                for v in selectedVerts: v[creaseLayer] = type
            else:
                for v in bm.verts: v[creaseLayer] = type

            bmesh.update_edit_mesh(d)

        if self.mode == 2:

            creaseLayer = bm.edges.layers.crease.verify()

            if self.whoToInfluence == 'Selected Elements':
                selectedEdges = [e for e in bm.edges if e.select]
                for e in selectedEdges: e[creaseLayer] = type
            else:
                for e in bm.edges: e[creaseLayer] = type

            bmesh.update_edit_mesh(d)

        return {"FINISHED"}


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

classes = (
            Import_MinecraftModel,
            Import_item,
            Alpha_Import,
            Alpha_Delete,
            Fix_Material,
            Copyloc,
            Copyrota,
            Copysize,
            Copytransform,
            ScaleUV,
            SelectalphaUV,
            World_Import,
            ImportMinecraftJSON,
            Open_Image,
            RestCursor,
            Addconstraints,
            Copy_constraint,
            All_constraint,
            Set_inverse,
            Clear_inverse,
            Delete_constraint,
            Apply_constraint,
            Disable_constraint,
            New_Material,
            Add_Image,
            Operators,
            Data_Blend,
            Solo_Light,
            Open_ImageFile,
            Crease,
          )        

register, unregister = bpy.utils.register_classes_factory(classes)
