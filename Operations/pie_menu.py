import bpy
from .. import addonPreferences
from ..Anime import AnimeProperties

from bpy.types import (
    Menu,
    Operator
)

class VIEW3D_OT_ClassObject(Operator):
    bl_idname = "class.object"
    bl_label = "Class Object"
    bl_description = "Edit/Object Mode Switch"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="EDIT")
        else:
            bpy.ops.object.mode_set(mode="OBJECT")
        return {'FINISHED'}

class VIEW3D_OT_ClassTexturePaint(Operator):
    bl_idname = "class.pietexturepaint"
    bl_label = "Class Texture Paint"
    bl_description = "Texture Paint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.paint.texture_paint_toggle()
        else:
            bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}

class VIEW3D_OT_ClassWeightPaint(Operator):
    bl_idname = "class.pieweightpaint"
    bl_label = "Class Weight Paint"
    bl_description = "Weight Paint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.paint.weight_paint_toggle()
        else:
            bpy.ops.paint.weight_paint_toggle()
        return {'FINISHED'}

class VIEW3D_OT_ClassVertexPaint(Operator):
    bl_idname = "class.pievertexpaint"
    bl_label = "Class Vertex Paint"
    bl_description = "Vertex Paint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.paint.vertex_paint_toggle()
        else:
            bpy.ops.paint.vertex_paint_toggle()
        return {'FINISHED'}

class VIEW3D_OT_ClassParticleEdit(Operator):
    bl_idname = "class.pieparticleedit"
    bl_label = "Class Particle Edit"
    bl_description = "Particle Edit (must have active particle system)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.particle.particle_edit_toggle()
        else:
            bpy.ops.particle.particle_edit_toggle()
        return {'FINISHED'}

# Set Mode Operator #
class VIEW3D_OT_SetObjectModePie(Operator):
    bl_idname = "object.set_object_mode_pie"
    bl_label = "Set the object interactive mode"
    bl_description = "I set the interactive mode of object"
    bl_options = {'REGISTER'}

    mode: bpy.props.StringProperty(name="Interactive mode", default="OBJECT")

    def execute(self, context):
        if (context.active_object):
            try:
                if context.active_object.mode == "POSE":
                    bpy.ops.object.mode_set(mode="OBJECT")
                else:
                    bpy.ops.object.mode_set(mode=self.mode)
            except TypeError:
                msg = context.active_object.name + " It is not possible to enter into the interactive mode"
                self.report(type={"WARNING"}, message=msg)
        else:
            self.report(type={"WARNING"}, message="There is no active object")
        return {'FINISHED'}

# Edit Selection Modes
class VIEW3D_OT_ClassVertex(Operator):
    bl_idname = "class.vertex"
    bl_label = "Class Vertex"
    bl_description = "Vert Select Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        if bpy.ops.mesh.select_mode != "EDGE, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            return {'FINISHED'}

class VIEW3D_OT_ClassEdge(Operator):
    bl_idname = "class.edge"
    bl_label = "Class Edge"
    bl_description = "Edge Select Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        if bpy.ops.mesh.select_mode != "VERT, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            return {'FINISHED'}

class VIEW3D_OT_ClassFace(Operator):
    bl_idname = "class.face"
    bl_label = "Class Face"
    bl_description = "Face Select Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        if bpy.ops.mesh.select_mode != "VERT, EDGE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            return {'FINISHED'}

class VIEW3D_OT_VertsEdgesFaces(Operator):
    bl_idname = "verts.edgesfaces"
    bl_label = "Verts Edges Faces"
    bl_description = "Vert/Edge/Face Select Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        if bpy.ops.mesh.select_mode != "VERT, EDGE, FACE":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            bpy.ops.mesh.select_mode(use_extend=True, use_expand=False, type='EDGE')
            bpy.ops.mesh.select_mode(use_extend=True, use_expand=False, type='FACE')
            return {'FINISHED'}

# Menus
class VIEW3D_MT_ObjectEditotherModes(Menu):
    """Edit/Object Others modes"""
    bl_idname = "MENU_MT_objecteditmodeothermodes"
    bl_label = "Edit Selection Modes"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        box = pie.split().column()

        box.operator("class.vertex", text="Vertex", icon='VERTEXSEL')
        box.operator("class.edge", text="Edge", icon='EDGESEL')
        box.operator("class.face", text="Face", icon='FACESEL')
        box.operator("verts.edgesfaces", text="Vertex/Edges/Faces", icon='OBJECT_DATAMODE')

class VIEW3D_MT_PIE_OBJECT(Menu):
    bl_idname = "VIEW3D_MT_PIE_OBJECT"
    bl_label = "Quick Object Tool"

    def draw(self, context):
        layout = self.layout
        ob = context.object
        # No Object Selected #
        if not ob or not ob.select_get():
            pie = layout.menu_pie()
            # 4 - LEFT
            pie.separator()
            # 6 - RIGHT
            pie.separator()
            # 2 - BOTTOM
            pie.operator("rest.cursor", text = "Rest Cursor", icon='CURSOR')
            # 8 - TOP
            if context.space_data.overlay.show_overlays == True:
                text_show_overlays = "Show Overlays"
            else:
                text_show_overlays = "Toggle Overlays"
            if context.space_data.overlay.show_bones == True:
                text_show_bones = "Show Bones Overlays"
            else:
                text_show_bones = "Toggle Bones Overlays"

            row = pie.row()
            row.prop(context.space_data.overlay, "show_bones", icon = "BONE_DATA", text = text_show_bones)
            row.prop(context.space_data.overlay, "show_overlays", icon = "OVERLAY", text = text_show_overlays)
            # 7 - TOP - LEFT
            pie.separator()
            # 9 - TOP - RIGHT
            pie.separator()
            # 1 - BOTTOM - LEFT
            pie.separator()
            # 3 - BOTTOM - RIGHT

        elif ob and ob.type == 'MESH' and ob.mode in {
                'OBJECT', 'SCULPT', 'VERTEX_PAINT',
                'WEIGHT_PAINT', 'TEXTURE_PAINT',
                'PARTICLE_EDIT', 'GPENCIL_EDIT',
        }:
            pie = layout.menu_pie()
            # 4 - LEFT
            pie.operator("class.pieweightpaint", text="Weight Paint", icon='WPAINT_HLT')
            # 6 - RIGHT
            pie.operator("class.pietexturepaint", text="Texture Paint", icon='TPAINT_HLT')
            # 2 - BOTTOM
            box = pie.split().column()
            row = box.row()
            row.label(text = "Copy Transforms")
            row = box.row()
            row.operator("copy.trans", text = "All Transform")
            row = box.row()
            col = row.column_flow(columns = 3)
            col.operator("copy.loc", text = "Location")
            col.operator("copy.rota", text = "Rotation")
            col.operator("copy.size", text = "Size")
            # 8 - TOP
            pie.operator("class.object", text="Object/Edit Toggle", icon='OBJECT_DATAMODE')
            # 7 - TOP - LEFT
            pie.operator("sculpt.sculptmode_toggle", text="Sculpt", icon='SCULPTMODE_HLT')
            # 9 - TOP - RIGHT
            pie.operator("class.pievertexpaint", text="Vertex Paint", icon='VPAINT_HLT')
            # 1 - BOTTOM - LEFT
            pie.menu("MENU_MT_objecteditmodeothermodes", text="Edit Modes", icon='EDITMODE_HLT')
            # 3 - BOTTOM - RIGHT
            if context.object.particle_systems:
                pie.operator("class.pieparticleedit", text="Particle Edit", icon='PARTICLEMODE')
            else:
                pie.separator()

        elif ob and ob.type == 'MESH' and ob.mode in {'EDIT'}:
            pie = layout.menu_pie()
            # 4 - LEFT
            pie.operator("class.pieweightpaint", text="Weight Paint", icon='WPAINT_HLT')
            # 6 - RIGHT
            pie.operator("class.pietexturepaint", text="Texture Paint", icon='TPAINT_HLT')
            # 2 - BOTTOM
            pie.menu("MENU_MT_objecteditmodeothermodes", text="Edit Modes", icon='EDITMODE_HLT')
            # 8 - TOP
            pie.operator("class.object", text="Edit/Object Toggle", icon='OBJECT_DATAMODE')
            # 7 - TOP - LEFT
            pie.operator("sculpt.sculptmode_toggle", text="Sculpt", icon='SCULPTMODE_HLT')
            # 9 - TOP - RIGHT
            pie.operator("class.pievertexpaint", text="Vertex Paint", icon='VPAINT_HLT')
            # 1 - BOTTOM - LEFT
            pie.separator()
            # 3 - BOTTOM - RIGHT
            if context.object.particle_systems:
                pie.operator("class.pieparticleedit", text="Particle Edit", icon='PARTICLEMODE')
            else:
                pie.separator()

        elif ob and ob.type == 'CURVE':
            pie = layout.menu_pie()
            # 4 - LEFT
            pie.separator()
            # 6 - RIGHT
            pie.separator()
            # 2 - BOTTOM
            pie.separator()
            # 8 - TOP
            pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')
            # 7 - TOP - LEFT
            pie.separator()
            # 9 - TOP - RIGHT
            pie.separator()
            # 1 - BOTTOM - LEFT
            pie.separator()
            # 3 - BOTTOM - RIGHT
            pie.separator()

        elif ob and ob.type == 'ARMATURE':
            pie = layout.menu_pie()
            # 4 - LEFT
            pie.operator(VIEW3D_OT_SetObjectModePie.bl_idname, text="Object", icon="OBJECT_DATAMODE").mode = "OBJECT"
            # 6 - RIGHT
            pie.operator(VIEW3D_OT_SetObjectModePie.bl_idname, text="Pose Mode Toggle", icon="POSE_HLT").mode = "POSE"
            # 2 - BOTTOM
            if ob.show_in_front == True:
                icon = "HIDE_OFF"
                text = "Toogle Bone In front"
            else:
                icon = "HIDE_ON"
                text = "Show Bone In front"
            pie.prop(ob ,"show_in_front", icon = icon, text = text)
            # 8 - TOP
            pie.operator("object.editmode_toggle", text="Edit Mode Toggle", icon='OBJECT_DATAMODE')
            # 7 - TOP - LEFT
            pie.separator()
            # 9 - TOP - RIGHT
            pie.separator()
            # 1 - BOTTOM - LEFT
            pie.separator()
            # 3 - BOTTOM - RIGHT
            pie.separator()

        elif ob and ob.type == 'FONT':
            pie = layout.menu_pie()
            pie.separator()
            pie.separator()
            pie.separator()
            pie.operator("object.editmode_toggle", text="Edit/Object Toggle", icon='OBJECT_DATAMODE')
            pie.separator()
            pie.separator()
            pie.separator()
            # 3 - BOTTOM - RIGHT
            pie.separator()

        elif ob and ob.type == 'SURFACE':
            pie = layout.menu_pie()
            pie.separator()
            pie.separator()
            pie.separator()
            pie.operator("object.editmode_toggle", text="Edit/Object Toggle", icon='OBJECT_DATAMODE')
            pie.separator()
            pie.separator()
            pie.separator()
            # 3 - BOTTOM - RIGHT
            pie.separator()

        elif ob and ob.type == 'META':
            pie = layout.menu_pie()
            pie.separator()
            pie.separator()
            pie.separator()
            pie.operator("object.editmode_toggle", text="Edit/Object Toggle", icon='OBJECT_DATAMODE')
            pie.separator()
            pie.separator()
            pie.separator()
            # 3 - BOTTOM - RIGHT
            pie.separator()

        elif ob and ob.type == 'LATTICE':
            pie = layout.menu_pie()
            pie.separator()
            pie.separator()
            pie.separator()
            pie.operator("object.editmode_toggle", text="Edit/Object Toggle", icon='OBJECT_DATAMODE')
            pie.separator()
            pie.separator()
            pie.separator()

        elif ob and ob.type == 'GPENCIL':
            pie = layout.menu_pie()
            # 4 - LEFT
            pie.operator(VIEW3D_OT_SetObjectModePie.bl_idname, text="Sculpt",
                         icon="SCULPTMODE_HLT").mode = "SCULPT_GPENCIL"
            # 6 - RIGHT
            pie.operator(VIEW3D_OT_SetObjectModePie.bl_idname, text="Draw", icon="GREASEPENCIL").mode = "PAINT_GPENCIL"
            # 2 - BOTTOM
            pie.operator(VIEW3D_OT_SetObjectModePie.bl_idname, text="Edit", icon="EDITMODE_HLT").mode = "EDIT_GPENCIL"
            # 8 - TOP
            pie.operator(VIEW3D_OT_SetObjectModePie.bl_idname, text="Object", icon="OBJECT_DATAMODE").mode = "OBJECT"
            # 7 - TOP - LEFT
            pie.separator()
            # 9 - TOP - RIGHT
            pie.separator()
            # 1 - BOTTOM - LEFT
            pie.separator()
            # 3 - BOTTOM - RIGHT
            pie.operator(
                VIEW3D_OT_SetObjectModePie.bl_idname,
                text="Weight Paint",
                icon="WPAINT_HLT").mode = "WEIGHT_GPENCIL"
            
        elif ob and ob.type == "LIGHT":
            light = context.object.data
            scene = context.scene

            pie = layout.menu_pie()

            light_linking = ob.light_linking

            pie_linking = pie.split().column()

            pie_linking.label(text = "Light Linking")
            pie_linking.template_ID(
                light_linking,
                "receiver_collection",
                new="object.light_linking_receiver_collection_new")

            if light_linking.receiver_collection:

                row = pie_linking.row()
                row.template_light_linking_collection(row, light_linking, "receiver_collection")
                col = row.column()
                sub = col.column(align=True)
                prop = sub.operator("object.light_linking_receivers_link", icon='ADD', text="")
                prop.link_state = 'INCLUDE'
                sub.operator("object.light_linking_unlink_from_collection", icon='REMOVE', text="")
                sub.menu("CYCLES_OBJECT_MT_light_linking_context_menu", icon='DOWNARROW_HLT', text="")

            pie_linking.label(text = "Shadow Linking")
            pie_linking.template_ID(
                light_linking,
                "blocker_collection",
                new="object.light_linking_blocker_collection_new")

            if light_linking.blocker_collection:

                row = pie_linking.row()
                row.template_light_linking_collection(row, light_linking, "blocker_collection")
                col = row.column()
                sub = col.column(align=True)
                prop = sub.operator("object.light_linking_blockers_link", icon='ADD', text="")
                prop.link_state = 'INCLUDE'
                sub.operator("object.light_linking_unlink_from_collection", icon='REMOVE', text="")
                sub.menu("CYCLES_OBJECT_MT_shadow_linking_context_menu", icon='DOWNARROW_HLT', text="")
            
            box = pie.split().column()
            # operator_enum will just spread all available options
            # for the type enum of the operator on the pie
            
            box.label(text = "Light Data")
            row = box.row()
            row.prop(light, "type", expand = True)
            box.prop(light, "color", text = "")
            box.prop(light, "energy", text = "Power")
            
            row = box.row()
            
            s1 = row.operator("bpy.ops", text = "-1")
            s1.id = "light-1"
            s1.object = light.name
            s05 = row.operator("bpy.ops", text = "-0.5")
            s05.id = "light-0.5"
            s05.object = light.name
            a05 = row.operator("bpy.ops", text = "+0.5")
            a05.id = "light+0.5"
            a05.object = light.name
            a1 = row.operator("bpy.ops", text = "+1")
            a1.id = "light+1"
            a1.object = light.name
            row = box.row()
            if light.type == "POINT":
                box.prop(light, "shadow_soft_size", text = "Size")
            if light.type == "SPOT":
                box.prop(light, "shadow_soft_size", text = "Size")
                box.label(text = "Beam Shape")
                box.prop(light, "spot_size", text = "Size")
                box.prop(light, "spot_blend", text = "Blend")
            if light.type == "SUN":
                box.prop(light, "angle", text = "Angle")
            if light.type == "AREA":
                box.prop(light, "shape")
                if light.shape == "SQUARE" or light.shape == "DISK":
                    box.prop(light, "size", text = "Size")
                if light.shape == "RECTANGLE" or light.shape == "ELLIPSE": 
                    box.prop(light, "size", text = "Size X")
                    box.prop(light, "size_y", text = "Size Y")
                box.prop(light, "spread", text = "Spread")

            box = pie.split().column()
            row = box.row()
            row.label(text = "Copy Transforms")
            row = box.row()
            row.operator("copy.trans", text = "All Transform")
            row = box.row()
            col = row.column_flow(columns = 3)
            col.operator("copy.loc", text = "Location")
            col.operator("copy.rota", text = "Rotation")
            col.operator("copy.size", text = "Size")


        elif ob and ob.type == "CAMERA":
            props = context.scene.save_cam_other

            pie = layout.menu_pie()

            box = pie.split().column()

            box.label(text = "Camera Save List")

            row = box.row(align=True)
            rows = row.row(align=True)
            rows.scale_x = 1.2
            rows.operator("savecams.cam_add", icon='ADD', text="")
            row.separator()
            row.operator("savecams.add_from_view", icon = "ZOOM_IN", text = "")


            row.label(text="Name",icon="NONE")

            row.prop(props,"toggle_type",text="Type")
            row.prop(props,"toggle_lens",text="Lens")
            row.prop(props,"toggle_resolution",text="Reso")

            row = box.row()
            col = row.column()
            col.template_list("SAVECAMS_UL_cam_collection", "", context.scene, "save_cam_collection", context.scene, "save_cam_collection_index")

            col = row.column()

            sub = col.column(align=True)
            sub.operator("savecams.list_up", icon="TRIA_UP", text='')
            sub.operator("savecams.list_down", icon="TRIA_DOWN", text='')

            box = pie.split().column()

            cam = ob.data
            row = box.row()
            row.label(text = cam.name + " Data")
            row = box.row()
            row.prop(cam, "name", text = "")
            row = box.row()
            row.prop(cam, "clip_start", text = "Clip Start")
            row.prop(cam, "clip_end", text = "Clip End")
            row = box.row()
            row.prop(cam, "type", text = "Type")
            if cam.type == "PERSP":
                box.prop(cam, "lens", text = "Focal Length")
            elif cam.type == "ORTHO":
                box.prop(cam, "ortho_scale", text = "Orthographic Scale")
            elif cam.type == "PANO":
                if context.scene.render.engine in ["CYCLES"]:
                    row.prop(cam.cycles, "panorama_type", text = "")
                    if cam.cycles.panorama_type == 'FISHEYE_LENS_POLYNOMIAL':
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_fov", text = "Field of View")
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_polynomial_k0", text = "K0")
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_polynomial_k1", text = "K1")
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_polynomial_k2", text = "K2")
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_polynomial_k3", text = "K3")
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_polynomial_k4", text = "K4")

            box.prop(cam, "sensor_width", text = "Size")
            box.label(text = "Depth of Field")
            box.prop(cam.dof, "use_dof", text = "Depth of Field", toggle = True)
            if cam.dof.use_dof == True:
                box.prop(cam.dof, "focus_object", text = "Focus Object")
                if cam.dof.focus_object:
                    if cam.dof.focus_object.type == 'ARMATURE':
                        box.prop(cam.dof, "focus_subtarget", text = "Focus Bone")
                box.prop(cam.dof, "focus_distance", text = "Distance")
                type = "obj"
                if type == "obj":
                    try:
                        text = "Show Focus Plane" if context.scene.cam == False else "Hide Focus Plane"
                        icon = "NORMALS_FACE" if context.scene.cam == False else "CANCEL"
                        box.prop(context.scene, "cam", text = text, toggle = True, icon = icon)
                    except:
                        pass
                elif type == "list":
                    try:
                        text = "Show Focus Plane" if context.scene.cam == False else "Hide Focus Plane"
                        icon = "NORMALS_FACE" if context.scene.cam == False else "CANCEL"
                        box.prop(context.scene, "camlist", text = text, toggle = True, icon = icon)
                    except:
                        pass
                box.prop(cam.dof, "aperture_fstop", text = "F-Stop")
                box.prop(cam.dof, "aperture_blades", text = "Blades")
                box.prop(cam.dof, "aperture_rotation", text = "Rotation")
                box.prop(cam.dof, "aperture_ratio", text = "Ratio")
            box.label(text = "Viewport Display")
            box.prop(cam, "show_composition_thirds", text = "Thirds", toggle = True)
            box.prop(cam, "passepartout_alpha", text = "Passepartout")

            box = pie.split().column()
            row = box.row()
            row.label(text = "Copy Transforms")
            row = box.row()
            row.operator("copy.trans", text = "All Transform")
            row = box.row()
            col = row.column_flow(columns = 3)
            col.operator("copy.loc", text = "Location")
            col.operator("copy.rota", text = "Rotation")
            col.operator("copy.size", text = "Size")

        elif ob and ob.type in {"EMPTY", "SPEAKER"}:
            message = "Active Object has only Object Mode available"
            pie = layout.menu_pie()
            pie.separator()
            pie.separator()
            pie.separator()
            box = pie.box()
            box.label(text=message, icon="INFO")

class VIEW3D_MT_PIE_OBJECT_LITE(Menu):
    bl_idname = "VIEW3D_MT_PIE_OBJECT_LITE"
    bl_label = "Quick Object Tool Lite"

    def draw(self, context):
        layout = self.layout
        ob = context.object
        # No Object Selected #

        if ob and ob.type == 'MESH' and ob.mode in {
                'OBJECT', 'SCULPT', 'VERTEX_PAINT',
                'WEIGHT_PAINT', 'TEXTURE_PAINT',
                'PARTICLE_EDIT', 'GPENCIL_EDIT',
        }:
            pie = layout.menu_pie()
            # 4 - LEFT
            pie.separator()
            # 6 - RIGHT
            pie.separator()
            # 2 - BOTTOM
            box = pie.split().column()
            row = box.row()
            row.label(text = "Copy Transforms")
            row = box.row()
            row.operator("copy.trans", text = "All Transform")
            row = box.row()
            col = row.column_flow(columns = 3)
            col.operator("copy.loc", text = "Location")
            col.operator("copy.rota", text = "Rotation")
            col.operator("copy.size", text = "Size")
            # 8 - TOP
            pie.separator()
            # 7 - TOP - LEFT
            pie.separator()
            # 9 - TOP - RIGHT
            pie.separator()
            # 1 - BOTTOM - LEFT
            pie.separator()
            # 3 - BOTTOM - RIGHT
            pie.separator()

        elif ob and ob.type == 'ARMATURE':
            pie = layout.menu_pie()
            # 4 - LEFT
            pie.operator(VIEW3D_OT_SetObjectModePie.bl_idname, text="Object", icon="OBJECT_DATAMODE").mode = "OBJECT"
            # 6 - RIGHT
            pie.operator(VIEW3D_OT_SetObjectModePie.bl_idname, text="Pose Mode Toggle", icon="POSE_HLT").mode = "POSE"
            # 2 - BOTTOM
            if ob.show_in_front == True:
                icon = "HIDE_OFF"
                text = "Toogle Bone In front"
            else:
                icon = "HIDE_ON"
                text = "Show Bone In front"
            pie.prop(ob ,"show_in_front", icon = icon, text = text)
            # 8 - TOP
            pie.operator("object.editmode_toggle", text="Edit Mode Toggle", icon='OBJECT_DATAMODE')
            # 7 - TOP - LEFT
            pie.separator()
            # 9 - TOP - RIGHT
            pie.separator()
            # 1 - BOTTOM - LEFT
            pie.separator()
            # 3 - BOTTOM - RIGHT
            pie.separator()
   
        elif ob and ob.type == "LIGHT":
            light = context.object.data
            scene = context.scene

            pie = layout.menu_pie()

            light_linking = ob.light_linking

            pie_linking = pie.split().column()

            pie_linking.label(text = "Light Linking")
            pie_linking.template_ID(
                light_linking,
                "receiver_collection",
                new="object.light_linking_receiver_collection_new")

            if light_linking.receiver_collection:

                row = pie_linking.row()
                row.template_light_linking_collection(row, light_linking, "receiver_collection")
                col = row.column()
                sub = col.column(align=True)
                prop = sub.operator("object.light_linking_receivers_link", icon='ADD', text="")
                prop.link_state = 'INCLUDE'
                sub.operator("object.light_linking_unlink_from_collection", icon='REMOVE', text="")
                sub.menu("CYCLES_OBJECT_MT_light_linking_context_menu", icon='DOWNARROW_HLT', text="")

            pie_linking.label(text = "Shadow Linking")
            pie_linking.template_ID(
                light_linking,
                "blocker_collection",
                new="object.light_linking_blocker_collection_new")

            if light_linking.blocker_collection:

                row = pie_linking.row()
                row.template_light_linking_collection(row, light_linking, "blocker_collection")
                col = row.column()
                sub = col.column(align=True)
                prop = sub.operator("object.light_linking_blockers_link", icon='ADD', text="")
                prop.link_state = 'INCLUDE'
                sub.operator("object.light_linking_unlink_from_collection", icon='REMOVE', text="")
                sub.menu("CYCLES_OBJECT_MT_shadow_linking_context_menu", icon='DOWNARROW_HLT', text="")
            
            box = pie.split().column()
            # operator_enum will just spread all available options
            # for the type enum of the operator on the pie
            
            box.label(text = "Light Data")
            row = box.row()
            row.prop(light, "type", expand = True)
            box.prop(light, "color", text = "")
            box.prop(light, "energy", text = "Power")
            
            row = box.row()
            
            s1 = row.operator("bpy.ops", text = "-1")
            s1.id = "light-1"
            s1.object = light.name
            s05 = row.operator("bpy.ops", text = "-0.5")
            s05.id = "light-0.5"
            s05.object = light.name
            a05 = row.operator("bpy.ops", text = "+0.5")
            a05.id = "light+0.5"
            a05.object = light.name
            a1 = row.operator("bpy.ops", text = "+1")
            a1.id = "light+1"
            a1.object = light.name
            row = box.row()
            if light.type == "POINT":
                box.prop(light, "shadow_soft_size", text = "Size")
            if light.type == "SPOT":
                box.prop(light, "shadow_soft_size", text = "Size")
                box.label(text = "Beam Shape")
                box.prop(light, "spot_size", text = "Size")
                box.prop(light, "spot_blend", text = "Blend")
            if light.type == "SUN":
                box.prop(light, "angle", text = "Angle")
            if light.type == "AREA":
                box.prop(light, "shape")
                if light.shape == "SQUARE" or light.shape == "DISK":
                    box.prop(light, "size", text = "Size")
                if light.shape == "RECTANGLE" or light.shape == "ELLIPSE": 
                    box.prop(light, "size", text = "Size X")
                    box.prop(light, "size_y", text = "Size Y")
                box.prop(light, "spread", text = "Spread")

            box = pie.split().column()
            row = box.row()
            row.label(text = "Copy Transforms")
            row = box.row()
            row.operator("copy.trans", text = "All Transform")
            row = box.row()
            col = row.column_flow(columns = 3)
            col.operator("copy.loc", text = "Location")
            col.operator("copy.rota", text = "Rotation")
            col.operator("copy.size", text = "Size")


        elif ob and ob.type == "CAMERA":
            props = context.scene.save_cam_other

            pie = layout.menu_pie()

            box = pie.split().column()

            box.label(text = "Camera Save List")

            row = box.row(align=True)
            rows = row.row(align=True)
            rows.scale_x = 1.2
            rows.operator("savecams.cam_add", icon='ADD', text="")
            row.separator()
            row.operator("savecams.add_from_view", icon = "ZOOM_IN", text = "")


            row.label(text="Name",icon="NONE")

            row.prop(props,"toggle_type",text="Type")
            row.prop(props,"toggle_lens",text="Lens")
            row.prop(props,"toggle_resolution",text="Reso")

            row = box.row()
            col = row.column()
            col.template_list("SAVECAMS_UL_cam_collection", "", context.scene, "save_cam_collection", context.scene, "save_cam_collection_index")

            col = row.column()

            sub = col.column(align=True)
            sub.operator("savecams.list_up", icon="TRIA_UP", text='')
            sub.operator("savecams.list_down", icon="TRIA_DOWN", text='')

            box = pie.split().column()

            cam = ob.data
            row = box.row()
            row.label(text = cam.name + " Data")
            row = box.row()
            row.prop(cam, "name", text = "")
            row = box.row()
            row.prop(cam, "clip_start", text = "Clip Start")
            row.prop(cam, "clip_end", text = "Clip End")
            row = box.row()
            row.prop(cam, "type", text = "Type")
            if cam.type == "PERSP":
                box.prop(cam, "lens", text = "Focal Length")
            elif cam.type == "ORTHO":
                box.prop(cam, "ortho_scale", text = "Orthographic Scale")
            elif cam.type == "PANO":
                if context.scene.render.engine in ["CYCLES"]:
                    row.prop(cam.cycles, "panorama_type", text = "")
                    if cam.cycles.panorama_type == 'FISHEYE_LENS_POLYNOMIAL':
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_fov", text = "Field of View")
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_polynomial_k0", text = "K0")
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_polynomial_k1", text = "K1")
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_polynomial_k2", text = "K2")
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_polynomial_k3", text = "K3")
                        row = box.row()
                        row.prop(cam.cycles, "fisheye_polynomial_k4", text = "K4")

            box.prop(cam, "sensor_width", text = "Size")
            box.label(text = "Depth of Field")
            box.prop(cam.dof, "use_dof", text = "Depth of Field", toggle = True)
            if cam.dof.use_dof == True:
                box.prop(cam.dof, "focus_object", text = "Focus Object")
                if cam.dof.focus_object:
                    if cam.dof.focus_object.type == 'ARMATURE':
                        box.prop(cam.dof, "focus_subtarget", text = "Focus Bone")
                box.prop(cam.dof, "focus_distance", text = "Distance")
                type = "obj"
                if type == "obj":
                    try:
                        text = "Show Focus Plane" if context.scene.cam == False else "Hide Focus Plane"
                        icon = "NORMALS_FACE" if context.scene.cam == False else "CANCEL"
                        box.prop(context.scene, "cam", text = text, toggle = True, icon = icon)
                    except:
                        pass
                elif type == "list":
                    try:
                        text = "Show Focus Plane" if context.scene.cam == False else "Hide Focus Plane"
                        icon = "NORMALS_FACE" if context.scene.cam == False else "CANCEL"
                        box.prop(context.scene, "camlist", text = text, toggle = True, icon = icon)
                    except:
                        pass
                box.prop(cam.dof, "aperture_fstop", text = "F-Stop")
                box.prop(cam.dof, "aperture_blades", text = "Blades")
                box.prop(cam.dof, "aperture_rotation", text = "Rotation")
                box.prop(cam.dof, "aperture_ratio", text = "Ratio")
            box.label(text = "Viewport Display")
            box.prop(cam, "show_composition_thirds", text = "Thirds", toggle = True)
            box.prop(cam, "passepartout_alpha", text = "Passepartout")

            box = pie.split().column()
            row = box.row()
            row.label(text = "Copy Transforms")
            row = box.row()
            row.operator("copy.trans", text = "All Transform")
            row = box.row()
            col = row.column_flow(columns = 3)
            col.operator("copy.loc", text = "Location")
            col.operator("copy.rota", text = "Rotation")
            col.operator("copy.size", text = "Size")

        elif ob and ob.type in {"EMPTY", "SPEAKER"}:
            message = "Active Object has only Object Mode available"
            pie = layout.menu_pie()
            pie.separator()
            pie.separator()
            pie.separator()
            box = pie.box()
            box.label(text=message, icon="INFO")

class VIEW3D_OT_Open_Object_PieMenu(Operator):
    bl_idname = "view3d.open_object_pie_menu"
    bl_label = "Quick Object Pie Menu"
    def execute(self, context):
        addon_prefs = addonPreferences.getAddonPreferences(context)
        i = 0
        for item in addon_prefs.registered_name:
            if item.registered_name == AnimeProperties.registered_name[0]:
                i = 1
        if addon_prefs.pie_menu:
            if i == 1:
                bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_OBJECT")
            else:
                bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_OBJECT_LITE")
        return {'FINISHED'}

classes = (
            VIEW3D_OT_ClassObject,
            VIEW3D_OT_ClassVertex,
            VIEW3D_OT_ClassEdge,
            VIEW3D_OT_ClassFace,
            VIEW3D_MT_ObjectEditotherModes,
            VIEW3D_OT_ClassTexturePaint,
            VIEW3D_OT_ClassWeightPaint,
            VIEW3D_OT_ClassVertexPaint,
            VIEW3D_OT_ClassParticleEdit,
            VIEW3D_OT_VertsEdgesFaces,
            VIEW3D_OT_SetObjectModePie,
            VIEW3D_MT_PIE_OBJECT,
            VIEW3D_MT_PIE_OBJECT_LITE,
            VIEW3D_OT_Open_Object_PieMenu,
)
        

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
