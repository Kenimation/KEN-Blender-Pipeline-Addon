import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty

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
            scale_uv(self.factor)
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
                scale_uv(self.factor)
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.object.mode_set(mode = 'OBJECT')
            selectalpha(self.threshold)
            if self.delete_faces == True:
                bpy.ops.mesh.delete(type='FACE')

        except:
             print("Selected object can't not select uv.")

        return {'FINISHED'}

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
                    scale_uv(self.factor)
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.context.scene.tool_settings.uv_select_mode = 'FACE'
                bpy.ops.uv.select_all(action='SELECT')
                bpy.ops.object.mode_set(mode = 'OBJECT')
                selectalpha(self.threshold)
                bpy.ops.mesh.delete(type='FACE')
                bpy.ops.object.mode_set(mode = 'OBJECT')
        except:
            pass

        return {'FINISHED'}

classes = (
            ScaleUV,
            SelectalphaUV,
            Alpha_Delete,
          )        

register, unregister = bpy.utils.register_classes_factory(classes)