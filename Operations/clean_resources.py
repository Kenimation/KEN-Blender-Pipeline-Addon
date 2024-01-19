import bpy

class Clean_Resources(bpy.types.Operator):
    bl_idname = "clean.resources"
    bl_label = "clean Resources"
    bl_options = {'REGISTER', 'UNDO'}

    type: bpy.props.StringProperty(options={'HIDDEN'})

    def execute(self, context):

        if self.type == "img":
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

        elif self.type == "mat":
            mat_list = []

            for mat in bpy.data.materials:
                if mat.use_fake_user == False:
                    if mat.name == mat.name.split(".")[0]:
                        mat_list.append(mat.name)

            for obj in bpy.data.objects:
                if obj.type == "MESH" and obj.data.materials:
                    if obj.material_slots:
                        for mat_slot in obj.material_slots:
                            if mat_slot.material.name not in mat_list and mat_slot.material.use_fake_user == False:
                                try:
                                    mat_slot.material = bpy.data.materials[mat_slot.material.name.split(".")[0]]
                                except:
                                    mat_slot.material.name = mat_slot.material.name.split(".")[0]

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

        return {"FINISHED"}
    
classes = (
            Clean_Resources,
          )

def register(): 
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
  
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.PoseBone.extra_prop