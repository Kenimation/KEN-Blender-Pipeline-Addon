import bpy

def update_mat_fake_use(self, context):
    if self.mat_fake_use == True:
        for mat in bpy.data.materials:
            mat.use_fake_user = True
    else:
        for mat in bpy.data.materials:
            mat.use_fake_user = False

def update_img_fake_use(self, context):
    if self.img_fake_use == True:
        for img in bpy.data.images:
            if img.has_data:
                img.use_fake_user = True
    else:
        for img in bpy.data.images:
            if img.has_data:
                img.use_fake_user = False

def update_hideoverlay(self, context):
    if self.hideoverlay == True:
        context.space_data.overlay.show_extras = True
        context.space_data.overlay.show_bones = True
    else:
        context.space_data.overlay.show_extras = False
        context.space_data.overlay.show_bones = False

def update_rendermodifier(self, context):
    obj = context.view_layer.objects.active
    modifiers = obj.modifiers
    if self.rendermodifier == True:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_render = False
    else:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_render = True

def update_editmodifier(self, context):
    obj = context.view_layer.objects.active
    modifiers = obj.modifiers
    if self.editmodifier == True:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_in_editmode = True
    else:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_in_editmode = False

def update_cagemodifier(self, context):
    obj = context.view_layer.objects.active
    modifiers = obj.modifiers
    if self.cagemodifier == True:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_on_cage = True
    else:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_on_cage = False

def update_hideconstraints(self, context):
    obj = context.object
    bones = context.active_pose_bone
    if obj.mode != 'POSE':
        con = obj.constraints
    if obj.mode == 'POSE':
        con = bones.constraints
    if self.hideconstraints == True:
        for id in con[:]:
            con[id.name].enabled = False
    else:
        for id in con[:]:
            con[id.name].enabled = True

def update_hidemodifier(self, context):
    obj = context.view_layer.objects.active
    modifiers = obj.modifiers
    if self.hidemodifier == True:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_viewport = False
    else:
        for id in obj.modifiers[:]:
            modifiers[id.name].show_viewport = True

def update_hide(self, context):
    for ob in context.scene.objects:
        if ob.type == 'LIGHT':
            if self.hide == True:
                ob.hide_viewport = True
            else:
                ob.hide_viewport = False

def update_cam_focus_list(self, context):
    cam_list = []
    for cam in bpy.data.objects:
        cam_list.append(cam)
    cam = cam_list[context.scene.cam_index]
    if self.camlist == True:
        bpy.ops.photographer.create_focus_plane(camera=cam.name)
    else:
        bpy.ops.photographer.delete_focus_plane(camera=cam.name)
    return

def update_cam_focus(self, context):
    cam = context.view_layer.objects.active.name
    if self.cam == True:
        bpy.ops.photographer.create_focus_plane(camera=cam)
    else:
        bpy.ops.photographer.delete_focus_plane(camera=cam)
    return

def update_hide_coll(self, context):
    if self.hide_coll == True:
        for coll in bpy.data.collections:
            coll.hide_viewport = True
    else:
        for coll in bpy.data.collections:
            coll.hide_viewport = False

def update_select_coll(self, context):
    if self.select_coll == True:
        for coll in bpy.data.collections:
            coll.hide_select = True
    else:
        for coll in bpy.data.collections:
            coll.hide_select = False
