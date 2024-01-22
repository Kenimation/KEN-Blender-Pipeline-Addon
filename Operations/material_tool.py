import bpy
from .. import addonPreferences
from bpy.types import Operator, OperatorFileListElement, Panel
from bl_ui.properties_material import EEVEE_MATERIAL_PT_context_material as original_EEVEE_MATERIAL_PT_context_material
from cycles.ui import CYCLES_PT_context_material as original_CYCLES_PT_context_material
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty

n_map_node_loc= (-1100,-350)
n_node_loc = (-800,-350)
ramp_node_h_loc = (-650,-125)
h_node_loc = (-200,-250)
tex_node_loc = (-1100, 350)

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
                    ramp_node_r.color_ramp.elements[0].color = (1, 1, 1, 1)
                    ramp_node_r.color_ramp.elements[1].color = (0, 0, 0, 1)
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
                        ramp_node_r.color_ramp.elements[0].color = (1, 1, 1, 1)
                        ramp_node_r.color_ramp.elements[1].color = (0, 0, 0, 1)
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
        if ob.type == "MESH":
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
            fixmaterial(mat)
            return {"FINISHED"}

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
                if obj.type == "MESH":
                    actmat = context.object.active_material_index
                    matnum = len(context.active_object.data.materials)
                    for count in range(matnum):
                        context.object.active_material_index = count
                        mat = obj.active_material
                        try:
                            fixmaterial(mat)
                            if self.ramp == True:
                                fixRamp(mat)
                            if self.bump == True:
                                fixBump(mat)
                            if self.nomral == True:
                                fixnormal(mat)
                            if self.SSS == True:
                                fixSSS(mat, 1)
                            else:
                                fixSSS(mat, 0)
                        except:
                            continue
                                
                        context.object.active_material_index = actmat

        if self.type == "index":
            mat = mat_data
            fixmaterial(mat)
            if self.ramp == True:
                fixRamp(mat)
            if self.bump == True:
                fixBump(mat)
            if self.nomral == True:
                fixnormal(mat)
            if self.SSS == True:
                fixSSS(mat, 1)
            else:
                fixSSS(mat, 0)

        if self.type == "scene":
            for mat in bpy.data.materials:
                try:
                    fixmaterial(mat)
                    if self.ramp == True:
                        fixRamp(mat)
                    if self.bump == True:
                        fixBump(mat)
                    if self.nomral == True:
                        fixnormal(mat)
                    if self.SSS == True:
                        fixSSS(mat, 1)
                    else:
                        fixSSS(mat, 0)
                except:
                    continue
        return {'FINISHED'}

class Select_Material(bpy.types.Operator):
    bl_idname = "select.material"
    bl_label = "Select Material"
    bl_options = {'REGISTER', 'UNDO'}

    mat: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):
        mat_data = bpy.data.materials[self.mat]
        obj = bpy.data.objects
        for ob in obj:
            if ob.type == 'MESH':
                try:
                    for m in ob.material_slots:
                        if m.material == mat_data:
                            ob.select_set(True)
                except:
                    continue

        return {'FINISHED'}
    
class MaterialButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        mat = context.material
        return mat and (context.engine in cls.COMPAT_ENGINES) and not mat.grease_pencil

class EEVEE_MATERIAL_PT_context_material(MaterialButtonsPanel, Panel):
    bl_label = ""
    bl_context = "material"
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'BLENDER_EEVEE_NEXT', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        mat = context.material

        if (ob and ob.type == 'GPENCIL') or (mat and mat.grease_pencil):
            return False

        return (ob or mat) and (context.engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        obj = context.view_layer.objects.active
        space = context.space_data
        scene = context.scene
        slot = context.material_slot
        row = layout.row()
        lrow = row.row()
        lrow.alignment = 'LEFT'
        matnum = len(bpy.data.materials)-1
        mat_list = []

        lrow.label(text = "Materials Library: Total "+str(matnum), icon = "MATERIAL")
		
        row = row.row()
        row.alignment = 'RIGHT'

        if obj:
            if obj.type == "MESH":
                if obj.mode == "OBJECT":
                    row.operator("object.material_slot_remove", text = "", icon = "REMOVE", emboss=False)
                    row.operator("object.material_slot_add", text = "", icon = "ADD", emboss=False)

        if scene.mat_fake_use == True:
            icon = "FAKE_USER_ON"
        else:
            icon = "FAKE_USER_OFF"
        row.prop(scene, "mat_fake_use", text = "", icon = icon, emboss = False)

        if obj:
            if scene.scene_mat == False:
                if obj.type == "MESH":
                    state = "Object Material"
                    mat = obj.active_material
                else:
                    state = "Scene Material: Object type does not have material."
                    for mat in bpy.data.materials:
                        mat_list.append(mat)
                    mat = mat_list[scene.mat_index]
            else:
                state = "Scene Material"
                for mat in bpy.data.materials:
                    mat_list.append(mat)
                mat = mat_list[scene.mat_index]
        else:
            state = "Scene Material"
            for mat in bpy.data.materials:
                mat_list.append(mat)
            mat = mat_list[scene.mat_index]

        delete = row.operator("data.blend", text = "", emboss = False, icon = "X")
        delete.type = "mat"
        delete.subtype = "del"

        box = layout.box()
        row = box.row(align = True)
        row.template_list("MATERIALS", "", obj, "material_slots", obj, "active_material_index")
        row.template_list("SCENEMATERIALS", "", bpy.data, "materials", scene, "mat_index")

        if obj.type == "MESH":
            try:
                for addmat in bpy.data.materials:
                    mat_list.append(addmat)
                addmat = mat_list[scene.mat_index]
                row = box.row()
                add = row.operator("data.blend", text = "Append")
                add.blend = addmat.name
                add.type = "mat"
                add.subtype = "append"
                append = row.operator("data.blend", text = "Replace")
                append.blend = addmat.name
                append.type = "mat"
                append.subtype = "replace"
            except:
                pass

        if obj:
            row = box.row()
            row.template_ID(obj, "active_material", new="material.new")

            if slot:
                icon_link = 'MESH_DATA' if slot.link == 'DATA' else 'OBJECT_DATA'
                if mat:
                    row.operator("select.material", icon = "RESTRICT_SELECT_OFF", emboss = False ,text = "").mat = mat.name
                row.prop(slot, "link", icon=icon_link, icon_only=True)

            if obj.mode == 'EDIT':
                row = box.row(align=True)
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

        elif mat:
            row.template_ID(space, "pin_id")

        if mat:
            box.label(text = "Fix Tools", icon = "TOOL_SETTINGS")
            if state == "Object Material":
                objmat = box.operator("fix.material", text = "Fix Materials")
                objmat.type = "obj"
            else:
                row = box.row()
                indexmat = row.operator("fix.material", text = "Fix Scene Material")
                indexmat.type = "index"
                indexmat.mat = mat.name
                allmat = row.operator("fix.material", text = "Fix All Materials")
                allmat.type = "scene"

class CyclesButtonsPanel:
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    COMPAT_ENGINES = {'CYCLES'}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

class CYCLES_PT_context_material(CyclesButtonsPanel, Panel):
    bl_label = ""
    bl_context = "material"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        if context.active_object and context.active_object.type == 'GPENCIL':
            return False
        else:
            return (context.material or context.object) and CyclesButtonsPanel.poll(context)

    def draw(self, context):
        layout = self.layout
        obj = context.view_layer.objects.active
        space = context.space_data
        scene = context.scene
        slot = context.material_slot
        row = layout.row()
        lrow = row.row()
        lrow.alignment = 'LEFT'
        matnum = len(bpy.data.materials)-1
        mat_list = []

        lrow.label(text = "Materials Library: Total "+str(matnum), icon = "MATERIAL")
		
        row = row.row()
        row.alignment = 'RIGHT'

        if obj:
            if obj.type == "MESH":
                if obj.mode == "OBJECT":
                    row.operator("object.material_slot_remove", text = "", icon = "REMOVE", emboss=False)
                    row.operator("object.material_slot_add", text = "", icon = "ADD", emboss=False)

        if scene.mat_fake_use == True:
            icon = "FAKE_USER_ON"
        else:
            icon = "FAKE_USER_OFF"
        row.prop(scene, "mat_fake_use", text = "", icon = icon, emboss = False)

        if obj:
            if scene.scene_mat == False:
                if obj.type == "MESH":
                    state = "Object Material"
                    mat = obj.active_material
                else:
                    state = "Scene Material: Object type does not have material."
                    for mat in bpy.data.materials:
                        mat_list.append(mat)
                    mat = mat_list[scene.mat_index]
            else:
                state = "Scene Material"
                for mat in bpy.data.materials:
                    mat_list.append(mat)
                mat = mat_list[scene.mat_index]
        else:
            state = "Scene Material"
            for mat in bpy.data.materials:
                mat_list.append(mat)
            mat = mat_list[scene.mat_index]

        delete = row.operator("data.blend", text = "", emboss = False, icon = "X")
        delete.type = "mat"
        delete.subtype = "del"

        box = layout.box()
        row = box.row(align = True)
        row.template_list("MATERIALS", "", obj, "material_slots", obj, "active_material_index")
        row.template_list("SCENEMATERIALS", "", bpy.data, "materials", scene, "mat_index")

        if obj.type == "MESH":
            try:
                for addmat in bpy.data.materials:
                    mat_list.append(addmat)
                addmat = mat_list[scene.mat_index]
                row = box.row()
                add = row.operator("data.blend", text = "Append")
                add.blend = addmat.name
                add.type = "mat"
                add.subtype = "append"
                append = row.operator("data.blend", text = "Replace")
                append.blend = addmat.name
                append.type = "mat"
                append.subtype = "replace"
            except:
                pass

        if obj:
            row = box.row()
            row.template_ID(obj, "active_material", new="material.new")

            if slot:
                icon_link = 'MESH_DATA' if slot.link == 'DATA' else 'OBJECT_DATA'
                if mat:
                    row.operator("select.material", icon = "RESTRICT_SELECT_OFF", emboss = False ,text = "").mat = mat.name
                row.prop(slot, "link", icon=icon_link, icon_only=True)

            if obj.mode == 'EDIT':
                row = box.row(align=True)
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

        elif mat:
            row.template_ID(space, "pin_id")

        if mat:
            box.label(text = "Fix Tools", icon = "TOOL_SETTINGS")
            if state == "Object Material":
                objmat = box.operator("fix.material", text = "Fix Materials")
                objmat.type = "obj"
            else:
                row = box.row()
                indexmat = row.operator("fix.material", text = "Fix Scene Material")
                indexmat.type = "index"
                indexmat.mat = mat.name
                allmat = row.operator("fix.material", text = "Fix All Materials")
                allmat.type = "scene"

def ken_material_panel(self, context):
    addon_prefs = addonPreferences.getAddonPreferences(context)
    use_material_panel = addon_prefs.use_material_panel

    from bpy.utils import register_class, unregister_class

    if use_material_panel:
        try:
            register_class(EEVEE_MATERIAL_PT_context_material)
            register_class(CYCLES_PT_context_material)
        except ValueError:
            unregister_class(EEVEE_MATERIAL_PT_context_material)
            unregister_class(CYCLES_PT_context_material)
            register_class(original_EEVEE_MATERIAL_PT_context_material)
            register_class(original_CYCLES_PT_context_material)
    else:
        try:
            unregister_class(EEVEE_MATERIAL_PT_context_material)
            unregister_class(CYCLES_PT_context_material)
            register_class(original_EEVEE_MATERIAL_PT_context_material)
            register_class(original_CYCLES_PT_context_material)
        except RuntimeError:
            pass

def menu_fixmaterial(self, context):
    if context.object.type == "MESH":
        if context.object.material_slots:
            for slot in context.object.material_slots:
                # Check if a material is assigned to the slot
                if slot.material is not None:
                    self.layout.separator()
                    self.layout.operator("fix.material", text = "Fix Material")
                    delete = self.layout.operator("data.blend", text = "Clear Material")
                    delete.type = "mat"
                    delete.subtype = "del"
        else:
            self.layout.separator()
            self.layout.operator("new.material", text = "New Material")

classes = (
            Add_Image,
            New_Material,
            Fix_Material,
            Select_Material,
          )

def register(): 
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.VIEW3D_MT_object_context_menu.append(menu_fixmaterial)

    addon_prefs = addonPreferences.getAddonPreferences(bpy.context)
    use_material_panel = addon_prefs.use_material_panel
    if use_material_panel:
        from bpy.utils import register_class

        try:
            register_class(EEVEE_MATERIAL_PT_context_material)
            register_class(CYCLES_PT_context_material)
        except ValueError:
            pass
  
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_fixmaterial)

    try:
        unregister_class(EEVEE_MATERIAL_PT_context_material)
        unregister_class(CYCLES_PT_context_material)
        register_class(original_EEVEE_MATERIAL_PT_context_material)
        register_class(original_CYCLES_PT_context_material)
    except RuntimeError:
        pass