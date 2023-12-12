import bpy
import bmesh

import os
from . import assetsDefs, assetsProperties
from ..Anime import AnimeProperties
from .. import addonPreferences

def drawheader(scene, row, obj):
    if scene.myProps == 'one':
        row.prop(scene, "view", icon = "VIEW3D", text = "")
        if scene.advanced_option == True:
            if obj:
                if obj.type == 'MESH': 
                    row.prop(scene, "simulation", icon = "PHYSICS", text = "")
                    row.prop(scene, "particles_properties", icon = "PARTICLES", text = "")
        row.prop(scene, "advanced_option", icon = "OUTLINER", text = "")
        row.prop(scene, "tools", icon = "TOOL_SETTINGS", text = "")

    if scene.myProps == 'two':
        if scene.mytools == 'three':
            row.prop(scene, "camera", text = "Local Camera")
        if scene.mytools == 'one' or scene.mytools == 'four':
            row.scale_x = 0.25
            row.operator("outliner.orphans_purge", text = "Purge").do_recursive=True
            row.scale_x = 1

def draw_tools(scene, obj, self):
    layout = self.layout
    box = layout.box()
    row = box.row()
    row.label(text = "Tools", icon = "TOOL_SETTINGS")
    if obj.mode == 'OBJECT':
        row.prop(scene, "Object_Type", text = "")
        row.operator("bpy.ops", text = "", icon = "RESTRICT_SELECT_OFF", emboss=False).id = "emptyselect"
    row = box.row()
    if scene.QuickImport == True:
        icon = "DOWNARROW_HLT"
    else:
        icon = "RIGHTARROW"
    row.prop(scene, "QuickImport", text = "Quick Import", icon = icon, emboss=False)
    if scene.QuickImport == True:
        QuickImport = box.box()
        row = QuickImport.row()
        row.label(text = "Object Import")
        row = QuickImport.row()
        row.operator("world.import", text = "World Import")
        row = QuickImport.row()
        col = row.column_flow(columns = 2)
        col.operator("import.minecraftmodel", text = "Minecraft Obj")
        col.operator("minecraft.import_json", text = "Minecraft Json")
        row = QuickImport.row()
        row.label(text = "Image Import")
        row = QuickImport.row()
        row.operator("alpha.import", text = "Alpha Plane")
        row = QuickImport.row()
        row.operator("3d.item", text = "3D Item from file")


    if obj.type == 'MESH':
        row = box.row()
        if scene.EditingTools == True:
            icon = "DOWNARROW_HLT"
        else:
            icon = "RIGHTARROW"
        row.prop(scene, "EditingTools", text = "Editing Tools", icon = icon, emboss=False)
        if scene.EditingTools == True:
            EditingTools = box.box()
            row = EditingTools.row()
            row.label(text = "Editing Tools")
            row = EditingTools.row()
            col = EditingTools.column_flow(columns = 2)
            col.operator("select.alphauv", text = "Select Alpha")
            col.operator("scale.uv", text = "Scale Faces")
            row = EditingTools.row()
            row.operator("alpha.delete", text = "Delete Alpha")

        row = box.row()
        if scene.VertexGroupTool == True:
            icon = "DOWNARROW_HLT"
        else:
            icon = "RIGHTARROW"
        row.prop(scene, "VertexGroupTool", text = "Vertex Group Tool", icon = icon, emboss=False)
        if scene.VertexGroupTool == True:
            VertexGroupTool = box.box()
            row = VertexGroupTool.row()
            row.label(text = "Add Vertex Group")
            row = VertexGroupTool.row()
            row.prop(scene, "VertexGroupMenu", expand = True)
            row = VertexGroupTool.row()  
            if scene.VertexGroupMenu == 'one':
                row.prop(scene, "VertexGroupName", text = "")
            else:
                row = VertexGroupTool.row()
                row.prop(scene, "VertexGroupPart", text = "")
                row.prop(scene, "VertexGroupLR", expand = True)
                
            row = VertexGroupTool.row()
            row.prop(scene, "FixName", text = "")
            row.prop(scene, "FixNameType", expand = True)
            row = VertexGroupTool.row()
            row.operator("bpy.ops", text = "Add").id = "VertexGroupAdd"

            row = VertexGroupTool.row()
            row.label(text = "Add Vertex Group Loop")
            row = VertexGroupTool.row()
            row.prop(scene, "VertexGroupName", text = "Name")
            row.prop(scene, "VertexGroupCount", text = "")
            row.prop(scene, "VertexGroupMiiror", text = "", icon = "ARROW_LEFTRIGHT")
            row = VertexGroupTool.row()
            row.operator("bpy.ops", text = "Add Vertex Group Loop").id = "VertexGroupLoop"

    if obj.type == 'ARMATURE':
        if obj.mode == 'POSE':
            row = box.row()
            if scene.BoneTool == True:
                icon = "DOWNARROW_HLT"
            else:
                icon = "RIGHTARROW"
            row.prop(scene, "BoneTool", text = "Bone Tool", icon = icon, emboss=False)
            if scene.BoneTool == True:
                BoneTool = box.box()
                row = BoneTool.row()
                row.label(text = "Damped Track Loop")
                row = BoneTool.row()
                row.prop(scene, "Track_Prefix", text = "")
                row.operator("bpy.ops", text = "Add").id = "DampedTrackLoop"
                row = BoneTool.row()
                row.label(text = "Constraints Driver")
                row = BoneTool.row()
                row.prop(scene, "Constraints_Type", text = "")
                row.prop(scene, "Rig_Prop", text = "")
                row = BoneTool.row()
                row.operator("bpy.ops", text = "Add").id = "ConstraintsDriver"
                row.operator("bpy.ops", text = "Remove").id = "ConstraintsDriverRemove"

def draw_edit(scene, box):
    if scene.object_properties == False:
        row = box.row()
        row.label(text = "Copy Transforms")
        row = box.row()
        row.operator("copy.trans", text = "All Transform")
        row = box.row()
        col = row.column_flow(columns = 3)
        col.operator("copy.loc", text = "Location")
        col.operator("copy.rota", text = "Rotation")
        col.operator("copy.size", text = "Size")

def draw_transform(addon_prefs, context, box, obj):
    row = box.row()
    if obj.type == 'ARMATURE':
        if obj.mode == 'POSE':
            actobj = context.active_pose_bone
            row.label(text = "Pose Transforms", icon = "BONE_DATA")
            try:
                row.prop(actobj, "name", text = "")
            except:
                pass
            row.prop(context.object.pose, "use_auto_ik", icon = "CON_KINEMATIC", text = "")
            row.prop(context.object.pose, "use_mirror_x", icon = "MOD_MIRROR", text = "")
        else:
            actobj = context.view_layer.objects.active
            row.label(text = "Object Transforms", icon = "OBJECT_DATAMODE")
    elif obj.type != 'ARMATURE':
        actobj = context.view_layer.objects.active
        row.label(text = "Object Transforms", icon = "OBJECT_DATAMODE")

    if actobj:
        row = box.row()
        if addon_prefs.compact_panel == False:
            row.label(text = "Location")
            row = box.row()
        row.prop(actobj, "location", text = "")
        row = box.row()
        if addon_prefs.compact_panel == False:
            row.label(text = "Rotation")
        row.prop(actobj, "rotation_mode", text = "")
        row = box.row()
        if obj.rotation_mode == 'QUATERNION':
            row.prop(actobj, "rotation_quaternion", text = "")
        else:
            row.prop(actobj, "rotation_euler", text = "")
        row = box.row()
        if addon_prefs.compact_panel== False:
            row.label(text = "Scale")
            row = box.row()
        row.prop(actobj, "scale", text = "")
        if obj.type == "MESH" or obj.type == "ARMATURE" and obj.mode == "OBJECT":
            row = box.row()
            if addon_prefs.compact_panel== False:
                row.label(text = "Dimensions")
                row = box.row()
            row.prop(actobj, "dimensions", text = "")

def drawedit_transform(addon_prefs, context, box, obj):
    sel_mode = context.tool_settings.mesh_select_mode[:]
    if sel_mode[0]:
        edit_icon = 'VERTEXSEL'
    elif sel_mode[1]:
        edit_icon ='EDGESEL'
    elif sel_mode[2]:
        edit_icon ='FACESEL'

    
    if obj.type != 'ARMATURE':
        row = box.row()
        row.label(text = "Edit Transforms", icon = edit_icon)
        row = box.row()

        if addon_prefs.compact_panel == False:
            row.label(text = "Location")
            row = box.row()
        '''
        try:
            i = bmesh.from_edit_mesh(context.object.data).select_history[-1]
            assert isinstance(i, bmesh.types.BMVert)
            o = context.object.data.vertices[i.index]
            row.prop(o, "co", index=0, text='')
            row.prop(o, "co", index=1, text='')
            row.prop(o, "co", index=2, text='')

            #This is probably the issue. 
            #I can't use prop on bmesh objects so don't know any other way.
            i.co[0] = o.co[0]
            i.co[1] = o.co[1]
            i.co[2] = o.co[2]

            #Each one of these has slightly different behavior but does not work
            #i.to_mesh(context.object.data)
            bmesh.update_edit_mesh(context.object.data)
            #context.object.update_from_editmode()
        except:
            row.prop(context.object, "location", index=0, text='')
            row.prop(context.object, "location", index=1, text='')
            row.prop(context.object, "location", index=2, text='')
        '''
        row.prop(obj, "location", text = "")

        props  = context.scene.CAB_PG_Prop # Create reference to property group
        
        # sel_mode[0] or sel_mode[1] or sel_mode[2]

        if obj.mode == 'EDIT' and sel_mode[0]:
            if addon_prefs.compact_panel == False:
                row = box.row()
                row.label(text='Weight value')
            row = box.row()
            row.prop(props, "vert_bevelWeight")
            if addon_prefs.compact_panel == False:
                row = box.row()
                row.label(text='Crese value')
            row = box.row()
            row.prop(props, "vert_Crease")

            row = box.row()
            clear = row.operator("set.crease", text="Clear Crease")
            clear.mode = 1
            clear.type = 'clear'
            set = row.operator("set.crease", text="Set Crease")
            set.mode = 1
            set.type = 'set'
        
        # if Edge edit mode
        elif obj.mode == 'EDIT' and sel_mode[1] or sel_mode[2]:
            if addon_prefs.compact_panel == False:
                row = box.row()
                row.label(text='Weight value')
            row = box.row()
            row.prop(props, "edge_bevelWeight")
            if addon_prefs.compact_panel == False:
                row = box.row()
                row.label(text='Crese value')
            row = box.row()
            row.prop(props, "edge_Crease")

            row = box.row()
            clear = row.operator("set.crease", text="Clear Crease")
            clear.mode = 2
            clear.type = 'clear'
            set = row.operator("set.crease", text="Set Crease")
            set.mode = 2
            set.type = 'set'

    else:
        actobj = context.active_bone
        row = box.row()
        row.label(text = "Bone Transforms", icon = "BONE_DATA")
        row.prop(actobj, "name", text = "")
        row.prop(context.object.pose, "use_mirror_x", icon = "MOD_MIRROR", text = "")
        row = box.row()
        if addon_prefs.compact_panel== False:
            row.label(text = "Head")
            row = box.row()
        row.prop(actobj, "head", text = "")
        row = box.row()
        if addon_prefs.compact_panel== False:
            row.label(text = "Tail")
            row = box.row()
        row.prop(actobj, "tail", text = "")
        row = box.row()
        row.prop(actobj, "roll", text = "Roll")
        row = box.row()
        row.prop(actobj, "tail_radius", text = "Radius")
        row = box.row()
        row.prop(actobj, "length", text = "Length")
        row = box.row()
        row.prop(actobj, "envelope_distance", text = "Envelope")

def draw_properties(addon_prefs, context, row, obj, pcoll):
    scene = context.scene
    if obj.type == 'ARMATURE':
        row.label(text = "", icon = "OUTLINER_OB_ARMATURE")
        row.prop(obj, "name", text = "Name")

        if addon_prefs.registered_name in AnimeProperties.registered_name:
            if obj.mode != 'EDIT' and context.active_object.RIG_ID in AnimeProperties.kenriglist:
                if context.active_object.RIG_ID == AnimeProperties.kenriglist[2]:
                    ken_icon = pcoll["Dual"]
                    ken_icon02 = pcoll["Dual_02"]
                else:
                    ken_icon = pcoll["Minecraft"]
                    ken_icon02 = pcoll["Minecraft_02"]
                if scene.ken_rig == True:
                    rig_icon = ken_icon02
                else:
                    rig_icon = ken_icon
                row.prop(scene, "ken_rig", icon_value = rig_icon.icon_id, text = "", emboss=False)
        else:
            row.prop(scene, "object_properties", icon = "ARMATURE_DATA", text = "")
    else:
        if obj.type == 'MESH':
            objicon = "OUTLINER_OB_MESH"
        elif obj.type == 'LIGHT':
            objicon = "OUTLINER_OB_LIGHT"
        elif obj.type == 'CAMERA':
            objicon = "OUTLINER_OB_CAMERA"
        elif obj.type == 'EMPTY':
            objicon = "OUTLINER_OB_EMPTY"
        elif obj.type == 'CURVE':
            objicon = "OUTLINER_OB_CURVE"
        else:
            objicon = "OUTLINER_OB_MESH"
        row.label(icon = objicon)
        row.prop(obj, "name", text = "Name")
        if obj.type == 'MESH':
            row.prop(scene, "object_properties", icon = "OBJECT_DATAMODE", text = "")
            row.prop(scene, "mat", icon = "MATERIAL", text = "")

def drawbone_properties(box, context, obj):
    actobj = context.active_bone
    actpos = context.active_pose_bone
    row = box.row()
    row.prop(obj.data, "display_type", text = "Display As")
    row = box.row()
    row.prop(obj, "show_in_front", text = "In Front")
    row = box.row()
    row.prop(obj.data, "show_names", text = "Show Names")
    row = box.row()
    row.prop(obj.data, "show_axes", text = "Axes")
    row.prop(obj.data, "axes_position", text = "Position")
    row = box.row()
    row.prop(obj.data, "relation_line_position", text = "Relations", expand = True)
    row = box.row()
    row.label(text = "Bone Properties")
    if obj.mode == "EDIT":
        row = box.row()
        row.prop(actobj, "parent", text = "Parent")
        row = box.row()
        row.prop(actobj, "use_connect", text = "Connected")

    row = box.row()
    row.prop(actobj, "use_deform", text = "Deform")
    row = box.row()
    row.prop(actobj.color, "palette", text = "Bone Color")
    row.operator("armature.copy_bone_color_to_selected", text = "", icon = "UV_SYNC_SELECT").bone_type='EDIT'

    if obj.mode == "POSE":
        row = box.row()
        row.prop(actpos.color, "palette", text = "Pose Bone Color")
        row.operator("armature.copy_bone_color_to_selected", text = "", icon = "UV_SYNC_SELECT").bone_type='POSE'
        row = box.row()
        row.prop(actobj, "hide", toggle = False, icon = 'BLANK1')
        row = box.row()
        row.prop(actpos, "custom_shape", text = "Custom Shape")
        if actpos.custom_shape:
            row = box.row()
            row.prop(actpos, "custom_shape_translation", text = "")
            row = box.row()
            row.prop(actpos, "custom_shape_rotation_euler", text = "")
            row = box.row()
            row.prop(actpos, "custom_shape_scale_xyz", text = "")
            row = box.row()
            row.prop(actpos, "use_custom_shape_bone_size", text = "Scale to Bone Length")
            row = box.row()
            row.prop(actobj, "show_wire", text = "Wireframe")

    row = box.row()
    if obj.BonesCollection == True:
        icon = "DOWNARROW_HLT"
    else:
        icon = "RIGHTARROW"
    row.prop(obj, "BonesCollection", emboss=False , icon = icon)

    if obj.BonesCollection == True:

        row = box.row()

        rows = 1

        row.template_list(
            "DATA_UL_bone_collections",
            "collections",
            obj.data,
            "collections",
            obj.data.collections,
            "active_index",
            rows=rows,
        )

        col = row.column(align=True)
        col.operator("armature.collection_add", icon='ADD', text="")
        col.operator("armature.collection_remove", icon='REMOVE', text="")
        col.separator()
        col.operator("armature.collection_move", icon='TRIA_UP', text="").direction = 'UP'
        col.operator("armature.collection_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
        col.separator()

        col.menu("ARMATURE_MT_collection_context_menu", icon='DOWNARROW_HLT', text="")

        row = box.row()

        sub = row.row(align=True)
        sub.operator("armature.collection_assign", text="Assign")
        sub.operator("armature.collection_unassign", text="Remove")

        sub = row.row(align=True)
        sub.operator("armature.collection_select", text="Select")
        sub.operator("armature.collection_deselect", text="Deselect")

def drawmesh_properties(box, context, obj):
    row = box.row()
    row.prop(obj, "parent", text = "Parent")
    row = box.row()
    row.prop(obj, "color", text = "Color")
    row = box.row()
    row.prop(obj, "display_type", text = "Display As")
    row = box.row()
    row.prop(obj, "show_bounds", text = "Bounds")
    row = box.row()
    row.prop(obj, "show_in_front", text = "In Front")
    if obj.show_bounds == True or obj.display_type == 'BOUNDS':
        row.prop(obj, "display_bounds_type", text = "")
    if context.scene.render.engine in ["CYCLES"]:
        if obj.type == 'MESH':
            if context.scene.ray_visility == True:
                icon = "DOWNARROW_HLT"
            else:
                icon = "RIGHTARROW"
            box.prop(context.scene, "ray_visility", text = "Ray Visility", icon = icon, emboss=False) 
            if context.scene.ray_visility == True:
                raybox = box.box()
                raybox.prop(obj, "visible_camera", toggle = True, text = "Camera")
                raybox.prop(obj, "visible_diffuse", toggle = True, text = "Diffuse")
                raybox.prop(obj, "visible_glossy", toggle = True, text = "Glossy")
                raybox.prop(obj, "visible_transmission", toggle = True, text = "Transmission")
                raybox.prop(obj, "visible_volume_scatter", toggle = True, text = "Volume Scatter")
                raybox.prop(obj, "visible_shadow", toggle = True, text = "Shadow")

def drawobj_properties(self, context, obj):
    layout = self.layout
    box = layout.box()

    if obj.type == 'ARMATURE':
        row = box.row()
        row.label(text = "Armature Properties", icon = "OUTLINER")
        drawbone_properties(box, context, obj)

    if obj.type == 'MESH':
        row = box.row()
        row.label(text = "Object Properties", icon = "OUTLINER")
        drawmesh_properties(box, context, obj)

def draw_data(self, context, obj):
    scene = context.scene
    if obj.type != 'ARMATURE' and obj.type != 'MESH':
        layout = self.layout
        box = layout.box()

    if obj.type == 'EMPTY':
        box.label(text = "Quick Empty Data", icon = "EMPTY_DATA")
        box.prop(obj, "empty_display_type", text = "Display As")
        box.prop(obj, "empty_display_size", text = "Size")
    
    if obj.type == 'CURVE':
        box.label(text = "Quick Curve Data", icon = "CURVE_DATA")
        row = box.row()
        row.prop(obj.data, "dimensions", expand = True)
        box.prop(obj.data, "resolution_u", text = "Preview U")
        box.prop(obj.data, "render_resolution_u", text = "Render U")
        box.prop(obj.data, "extrude", text = "Extrude")
        row = box.row()
        row.prop(obj.data, "bevel_mode", expand = True)
        if not obj.data.bevel_mode == 'OBJECT':
            box.prop(obj.data, "bevel_depth", text = "Depth")
            box.prop(obj.data, "bevel_resolution", text = "Resolution")
        else:
            box.prop(obj.data, "bevel_object", text = "Object")
        box.prop(obj.data, "use_fill_caps", text = "Fill Caps")

    if obj.type == 'LIGHT':
        box.label(text = "Quick Light", icon = "LIGHT_DATA")
        light = context.object.data
        drawlight(box, light)
        
    if obj.type == 'CAMERA':
        box.label(text = "Quick Camera", icon = "CAMERA_DATA")
        cam = context.active_object
        type = "obj"
        drawcam(context, box, cam, type)
        if scene.cam_shake == True:
            icon = "DOWNARROW_HLT"
        else:
            icon = "RIGHTARROW"
        box.prop(context.scene, "cam_shake", text = "Camera Shakify", icon = icon, emboss=False)
        if context.scene.cam_shake == True:
            draw_cam_shake(box, cam)

        if scene.cam_save == True:
            icon = "DOWNARROW_HLT"
        else:
            icon = "RIGHTARROW"
        box.prop(context.scene, "cam_save", text = "Camera Save List", icon = icon, emboss=False)
        if context.scene.cam_save == True:
            draw_save_cam(context, box)
    
    if obj.type == 'MESH':  
        drawmodifiers(self, context)
        if scene.particles_properties == True:
            drawparticles(self, context)
        if scene.simulation == True:
            drawsimulation(self, context)

    drawconstraints(self, context)

def draw_view(addon_prefs, context, box, row, obj):
    scene = context.scene
    row.label(text = "View", icon = "VIEW3D")
    row.prop(scene, "hideoverlay", icon = "OVERLAY", text = "")
    row = box.row()
    row.prop(context.scene.render, "use_simplify", text = "Use Simplify", toggle = True)
    row.prop(context.scene.render, "simplify_subdivision", text = "Subdivision")
    box.prop(context.space_data, "lens", text = "Focal Length")
    row = box.row()
    row.prop(context.space_data, "clip_start", text = "Clip Start")
    row.prop(context.space_data, "clip_end", text = "Clip End")
    if obj:
        if obj.mode == "EDIT":
            row = box.row()
            row.label(text = "Nomrals", icon = "NORMALS_FACE")
            row = box.row()
            row.prop(context.space_data.overlay, "show_vertex_normals", text = "", icon = "NORMALS_VERTEX")
            row.prop(context.space_data.overlay, "show_split_normals", text = "", icon = "NORMALS_VERTEX_FACE")
            row.prop(context.space_data.overlay, "show_face_normals", text = "", icon = "NORMALS_FACE")
            row.prop(context.space_data.overlay, "normals_length", text = "Size")
    row = box.row()
    row.label(text = "Cursor", icon = "CURSOR")
    row = box.row()
    if addon_prefs.compact_panel == False:
        row.label(text = "Cursor Location")
        row = box.row()
    row.prop(scene.cursor, "location" ,text = "")
    row = box.row()
    row.operator("rest.cursor", text = "Rest Cursor")
       
def drawmaterial_properties(self, context):
    layout = self.layout
    box = layout.box()
    scene = context.scene
    obj = context.view_layer.objects.active
    row = box.row()
    row.label(text = "Quick Material", icon = "MATERIAL")
    box.template_list("MATERIALS", "", obj, "material_slots", obj, "active_material_index")
    i = 0
    if obj:
        try:
            if obj.data.materials:
                mat = obj.active_material
                row.label(icon_value=layout.icon(mat))
                row.prop(mat, "name", text ="")
                row.scale_x = 1
                if obj.mode == "OBJECT":
                    row.scale_x = 0.2
                    single = row.operator("data.blend", text = str(mat.users))
                    single.blend = mat.name
                    single.type = "mat"
                    single.subtype = "single"
                    row.scale_x = 1
                    duplicate = row.operator("data.blend", text = "", icon = "DUPLICATE", emboss=False)
                    duplicate.blend = mat.name
                    duplicate.type = "mat"
                    duplicate.subtype = "duplicate"

                if obj.mode == "EDIT":
                    row = box.row()
                    row.operator("object.material_slot_assign", text = "Assign")
                    row.operator("object.material_slot_select", text = "Select")

                drawnode_tree(scene, box, mat)
        except:
            pass
        if not obj.data.materials or not obj.active_material:
            box.label(text = "No Available Object")
            box.operator("new.material", text = "New Material", icon = "MATERIAL")

def drawmaterial(scene, box, row, obj, mat, state):
    if mat and mat.name != 'Dots Stroke':
        
        select = row.operator("data.blend", icon = "RESTRICT_SELECT_OFF", emboss = False ,text = "")
        select.type = "mat"
        select.subtype = "select"
        select.blend = mat.name
        if obj:
            if obj.type == "MESH" and scene.scene_mat == False:
                delete = row.operator("data.blend", text = "Clean All")
                delete.type = "mat"
                delete.subtype = "del"

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
            row = box.row()

        row = box.row()
        row.label(icon_value=row.icon(mat))
        row.prop(mat, "name", text = "")
        row.scale_x = 1
        row.prop(mat,"use_fake_user", text = "", emboss=False)

        if obj:
            if obj.type == "MESH":
                if obj.active_material:
                    if obj.mode == "OBJECT":
                        row.scale_x = 0.1
                        single = row.operator("data.blend", text = str(mat.users))
                        single.blend = mat.name
                        single.type = "mat"
                        single.subtype = "single"

                        row.scale_x = 1
                        duplicate = row.operator("data.blend", text = "", icon = "DUPLICATE", emboss=False)
                        duplicate.blend = mat.name
                        duplicate.type = "mat"
                        duplicate.subtype = "duplicate"

                        row.operator("object.material_slot_remove", text = "", icon = "X", emboss=False)
                    elif obj.mode == "EDIT":
                        row = box.row()
                        row.operator("object.material_slot_assign", text = "Assign")
                        row.operator("object.material_slot_select", text = "Select")

        drawnode_tree(scene, box, mat)

    if mat:
        if mat.name == 'Dots Stroke':
            box.label(text = "Scene has no Material")
            box.operator("new.material", text = "New Material", icon = "MATERIAL")
        
    else:
        if obj:
            if obj.type == "MESH":
                if not obj.data.materials:
                    box.label(text = "Object has no Material")
                    box.operator("new.material", text = "New Material", icon = "MATERIAL")
                else:
                    if not obj.active_material:
                        box.label(text = "Material Slot has no Material")
                        box.operator("new.material", text = "New Material", icon = "MATERIAL")

def drawnode_tree(scene, box, mat):
    ntree = mat.node_tree
    node = ntree.get_output_node('EEVEE')
    input = find_node_input(node, "Surface")
    if scene.mat_surface == True:
        icon = "DOWNARROW_HLT"
    else:
        icon = "RIGHTARROW"
    box.prop(scene, "mat_surface", text = "Materials Surface", icon = icon, emboss=False)
    if scene.mat_surface == True:
        node_view = box.box()
        node_view.template_node_view(ntree, node, input)
    for node in mat.node_tree.nodes:
        if node.name == 'Animated_Texture':
            box.label(text = node.name)
            box.prop(node.inputs[0], "default_value", text = "Frame Number")
            row = box.row()
            row.prop(node.inputs[2], "default_value", text = "Frame Muiltply")
        if node.name == 'ColorRamp_Specular':
            box.label(text = "Specular Color Ramp")
            box.template_color_ramp(node, "color_ramp", expand=True)
        if node.name == 'ColorRamp_Roughness':
            box.label(text = "Roughness Color Ramp")
            box.template_color_ramp(node, "color_ramp", expand=True)
        if node.name == 'ColorRamp_Bump':
            box.label(text = "Bump Color Ramp")
            box.template_color_ramp(node, "color_ramp", expand=True)
        if node.name == 'Combine Nomral Map':
            box.label(text = node.name)
            box.prop(node.inputs[3], "default_value", text = "Bump Strength")
            row = box.row()
            row.prop(node.inputs[1], "default_value", text = "Nomral Strength")
        if node.name == "Glass_Dispersion":
            box.label(text = node.name)
            for input in range(inputs):
                box.prop(node.inputs[input], "default_value", text = node.inputs[input].name)
        if node.name == "Emission Object":
            box.label(text = node.name)
            inputs = len(node.inputs)
            for input in range(inputs):
                box.prop(node.inputs[input], "default_value", text = node.inputs[input].name)
        if node.name == "Illumination Object":
            box.label(text = node.name)
            inputs = len(node.inputs)
            for input in range(inputs):
                box.prop(node.inputs[input], "default_value", text = node.inputs[input].name)

    box.label(text = "Material Settings")
    box.prop(mat, "blend_method")
    box.prop(mat, "shadow_method")
    row = box.row()
    row.prop(mat, "show_transparent_back", toggle = True)
    row.prop(mat, "use_screen_refraction", toggle = True)

def drawlight(box, light):
    lightbox = box.box()
    row = lightbox.row()
    row.prop(light, "type", expand = True)
    lightbox.prop(light, "color", text = "Color")
    lightbox.prop(light, "energy", text = "Power")
    row = lightbox.row()
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
    row = lightbox.row()
    if light.type == "POINT":
        lightbox.prop(light, "shadow_soft_size", text = "Size")
    if light.type == "SPOT":
        lightbox.prop(light, "shadow_soft_size", text = "Size")
        lightbox.label(text = "Beam Shape")
        lightbox.prop(light, "spot_size", text = "Size")
        lightbox.prop(light, "spot_blend", text = "Blend")
    if light.type == "SUN":
        lightbox.prop(light, "angle", text = "Angle")
    if light.type == "AREA":
        lightbox.prop(light, "shape")
    try:
        if light.type != "POINT":
            if light.shape == "SQUARE" or light.shape == "DISK":
                lightbox.prop(light, "size", text = "Size")
            if light.shape == "RECTANGLE" or light.shape == "ELLIPSE": 
                lightbox.prop(light, "size", text = "Size X")
                lightbox.prop(light, "size_y", text = "Size Y")
    except:
        pass
    if light.type == "AREA":
        lightbox.prop(light, "spread", text = "Spread")

def drawcam(context, box, cam, type):
    cam = cam.data
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

def draw_save_cam(context, box):
    props = context.scene.save_cam_other

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

def draw_cam_shake(box, cam):
    row = box.row()
    row.template_list(
        listtype_name="OBJECT_UL_camera_shake_items",
        list_id="Camera Shakes",
        dataptr=cam,
        propname="camera_shakes",
        active_dataptr=cam,
        active_propname="camera_shakes_active_index",
    )
    col = row.column()
    cam_shake_add = col.operator("object.camera_shake_add", text="", icon='ADD')
    cam_shake_add.camera = cam.name
    cam_shake_remove = col.operator("object.camera_shake_remove", text="", icon='REMOVE')
    cam_shake_remove.camera = cam.name
    cam_shake_up = col.operator("object.camera_shake_move", text="", icon='TRIA_UP')
    cam_shake_up.camera = cam.name
    cam_shake_up.type = 'UP'
    cam_shake_down = col.operator("object.camera_shake_move", text="", icon='TRIA_DOWN')
    cam_shake_down.camera = cam.name
    cam_shake_down.type = 'DOWN'

    row = box.row()
    row.operator("object.camera_shakes_fix_global")
    if cam.camera_shakes_active_index < len(cam.camera_shakes):
        shake = cam.camera_shakes[cam.camera_shakes_active_index]
        row = box.row()
        row.prop(shake, "shake_type", text="")
        row = box.row()
        row.prop(shake, "influence", slider=True)
        row = box.row()
        row.prop(shake, "scale")
        row = box.row()
        row.prop(shake, "use_manual_timing")
        if shake.use_manual_timing:
            row = box.row()
            row.prop(shake, "time")
        else:
            row = box.row()
            row.prop(shake, "speed")
            row = box.row()
            row.prop(shake, "offset")

def draw_mark(scene, box, row):
    row.template_list("MARKS", "", scene, "timeline_markers", scene, "mark_index")
    if scene.marker == True:
        try:
            mark_list = []
            for mark in scene.timeline_markers:
                mark_list.append(mark)
            mark = mark_list[scene.mark_index]
            row = box.row()
            box.label(text = "Quick Marker", icon = "PMARKER_ACT")
            row = box.row()
            row.prop(mark, "name", text = "Name")
            row.prop(mark, "camera", text = "")
            row.prop(mark, "frame", text = "Frame")
            delmark = row.operator("bpy.ops", text = "", icon = "X", emboss=False)
            delmark.object = str(mark.name)
            delmark.id = "del marker"
        except:
            row = box.row()
            box.label(text = "Scene has No Marker", icon = "PMARKER_ACT")
        row = box.row()
        box.label(text = "Add Marker", icon = "ADD")
        row = box.row()
        row.prop(scene, "marker_name", text = "Name")
        row.prop(scene, "frame_current", text = "Current Frame")
        addmark = row.operator("bpy.ops", text = "", icon = "ADD", emboss=False)
        addmark.object = scene.marker_name
        addmark.id = "new marker"
        row = box.row()

def drawparticles(self, context):

    scene = context.scene

    layout = self.layout
    box = layout.box()
    row = box.row()
    
    row.label(text = "Particles", icon = "PARTICLES")
    row.operator("object.particle_system_remove", icon = "REMOVE", text = "", emboss=False)
    row.operator("object.particle_system_add", icon = "ADD", text = "", emboss=False)
    row.operator("particle.duplicate_particle_system", icon = "DUPLICATE", text = "", emboss=False).use_duplicate_settings=True

    row = box.row()
    row.template_list("PARTICLES", "", context.active_object, "particle_systems", scene, "particles_index")


    if context.active_object.particle_systems:
        try:
            particles_list = []
            for particles in context.active_object.particle_systems:
                particles_list.append(particles)
            particles_system = particles_list[scene.particles_index]
            particles_data = particles_system.settings
        except:
            pass

        row = box.row()
        row.label(text="Name")
        row.prop(particles_system, "name", text="")
        row = box.row()
        row.label(text="- Emission -")
        row = box.row()
        row.prop(particles_data, "emit_from", text="Emit From")
        row = box.row()
        row.prop(particles_data, "distribution", text="Distribution")
        row = box.row()
        row.label(text="Number")
        row.prop(particles_data, "count", text="")
        row = box.row()
        row.label(text="Seed")
        row.prop(particles_system, "seed", text="")
        row = box.row()
        row.label(text="Frame Start")
        row.prop(particles_data, "frame_start", text="")
        row = box.row()
        row.label(text="Frame End")
        row.prop(particles_data, "frame_end", text="")
        row = box.row()
        row.label(text="Lifetime")
        row.prop(particles_data, "lifetime", text="")
        row = box.row()
        row.label(text="Lifetime Randomness")
        row.prop(particles_data, "lifetime_random", text="")
        row = box.row()
        row.label(text="Timestep")
        row.prop(particles_data, "timestep", text="")

        row = box.row()
        row.prop(particles_data, "normal_factor", text="Normal")
        row = box.row()
        row.prop(particles_data, "object_align_factor", text="")
        row = box.row()
        row.prop(particles_data, "object_factor", text="Object Factor")
        row = box.row()
        row.prop(particles_data, "factor_random", text="Randomness")

        row = box.row()
        row.prop(particles_data, "use_rotations", text="Rotation", toggle=True)
        if particles_data.use_rotations == True:
            row = box.row()
            row.prop(particles_data, "rotation_mode", text="Orientation Axis")
            row = box.row()
            row.prop(particles_data, "rotation_factor_random", text="Randomness")
            row = box.row()
            row.prop(particles_data, "phase_factor", text="Phase")
            row = box.row()
            row.prop(particles_data, "phase_factor_random", text="Phase Randomness")
            row = box.row()
            row.prop(particles_data, "use_dynamic_rotation", text="Dynamic")
            row = box.row()
            row.prop(particles_data, "angular_velocity_mode", text="Axis")
            row = box.row()
            row.prop(particles_data, "angular_velocity_factor", text="Amount")

        row = box.row()
        row.label(text="- Render -")
        row = box.row()
        row.label(text="Render As")
        row.prop(particles_data, "render_type", text="")
        if particles_data.render_type == 'OBJECT':
            row = box.row()
            row.label(text="Instance Object")
            row.prop(particles_data, "instance_object", text="")
        if particles_data.render_type == 'COLLECTION':
            row = box.row()
            row.label(text="Instance Collection")
            row.prop(particles_data, "instance_collection", text="")
        row = box.row()
        row.label(text="Scale")
        row.prop(particles_data, "particle_size", text="")
        row = box.row()
        row.label(text="Scale Randomness")
        row.prop(particles_data, "size_random", text="")
        row = box.row()
        row.prop(particles_data, "use_global_instance", text="Global Coordinates")
        row.prop(particles_data, "use_rotation_instance", text="Object Rotation")
        row.prop(particles_data, "use_scale_instance", text="Object Scale")
        if particles_data.render_type == 'COLLECTION':
            row = box.row()
            row.prop(particles_data, "use_whole_collection", text="Whole Collection") 
            row.prop(particles_data, "use_collection_pick_random", text="Pick Random")

        row = box.row()
        row.label(text="- Emittter -")
        row = box.row()
        row.prop(context.object, "show_instancer_for_viewport", text="Viewport")
        row.prop(context.object, "show_instancer_for_render", text="Render")

        row = box.row()
        row.operator("ptcache.bake_all", text = "Bake All Dynamics").bake=True
        row.operator("ptcache.free_bake_all", text = "Delete All Bakes")
    else:
        box.label(text = "Object has no Particles System")
        box.operator("object.particle_system_add", text = "New Particle", icon = "PARTICLES")

def drawimage(scene, box, row):
    row.operator("open.imagefile", icon = "FILE_NEW", text = "", emboss=False)
    if scene.imagepreview == True:
        previewicon = "SEQ_SPLITVIEW"
    else:
        previewicon = "SEQ_PREVIEW"
    row.prop(scene, "imagepreview", icon = previewicon, text = "", emboss=False)
    if scene.img_fake_use == True:
        icon = "FAKE_USER_ON"
    else:
        icon = "FAKE_USER_OFF"
    row.prop(scene, "img_fake_use", text = "", icon = icon, emboss = False)
    row.scale_x = 0.75
    clean = row.operator("data.blend", icon = "BRUSH_DATA", text = "Clean")
    clean.type = "img"
    clean.subtype = "clean"
    if scene.imagepreview == True:
        try:
            img_list = []
            for img in bpy.data.images:
                img_list.append(img)
            img_data = img_list[scene.image_index]
            row = box.row()
            size = f"{img_data.size[0]} x {img_data.size[1]}"
            row.label(text=f"Image Size: {size}")
            row = box.row()
            row.template_icon(icon_value=img_data.preview.icon_id,scale=5)
        except:
            pass
    row = box.row()
    row.template_list("IMAGES", "", bpy.data, "images", scene, "image_index")
    row = box.row()
    try:
        img_list = []
        for img in bpy.data.images:
            img_list.append(img)
        img_data = img_list[scene.image_index]
    except:
        pass
    row.prop(img_data, "filepath", text="", icon_value=img_data.preview.icon_id)

    row.scale_x = 0.05
    row.label(text = str(img_data.users))

    row.scale_x = 1
    if img_data.packed_files:
        packicon = "PACKAGE"
    else:
        packicon = "UGLYPACKAGE"
    pack = row.operator("data.blend", text="", icon = packicon, emboss=False)
    pack.type = "img"
    pack.subtype = "pack"
    pack.blend = str(img_data.name)

    reload = row.operator("data.blend", text = "", icon = "FILE_REFRESH", emboss=False)
    reload.type = "img"
    reload.subtype = "reload"
    reload.blend = str(img_data.name)
    row.prop(img,"use_fake_user", text = "", emboss=False)
    row = box.row()
    row.prop(img_data, "source", text = "")
    row.prop(img_data.colorspace_settings, "name", text = "")

def drawmodifiers(self, context):
    layout = self.layout
    box = layout.box()
    row = box.row()
    scene = context.scene
    if scene.showmodifier == True:
        icon = "MODIFIER"
        text = "Quick Modifier"
    else:
        icon = "MODIFIER_DATA"
        text = "Show Modifier"
    row.prop(scene, "showmodifier", text = text, icon = icon, emboss=False)
    obj = context.view_layer.objects.active
    if obj.modifiers:
        if scene.hidemodifier == True:
            hideicon = "RESTRICT_VIEW_ON"
        else:
            hideicon = "RESTRICT_VIEW_OFF"
            row.prop(scene, "cagemodifier", text = "", icon = "OUTLINER_DATA_MESH")
            row.prop(scene, "editmodifier", text = "", icon = "EDITMODE_HLT")
        row.prop(scene, "hidemodifier", text = "", icon = hideicon, emboss=False)
        if scene.rendermodifier == True:
            hideicon = "RESTRICT_RENDER_ON"
        else:
            hideicon = "RESTRICT_RENDER_OFF"
        row.prop(scene, "rendermodifier", text = "", icon = hideicon, emboss=False)
        row.operator("all.constraint", text = "", icon = "CHECKMARK", emboss=False).type = 2
        row.operator("all.constraint", text = "", icon = "PANEL_CLOSE", emboss=False).type = 0

    if scene.showmodifier == True:
        row = box.row()
        row.operator_menu_enum("object.modifier_add", "type")
        if obj.modifiers:
            modifiers = obj.modifiers
            for id in obj.modifiers[:]:
                if id.type == "ARMATURE": 
                    row = box.row()
                    row.operator("copy.constraint", text = "", icon = "MOD_ARMATURE", emboss=False).id = id.name
                    row.prop(modifiers[id.name], "name", text = "")
                    if modifiers[id.name].show_viewport == True:
                        row.prop(modifiers[id.name], "show_on_cage", text = "")
                        row.prop(modifiers[id.name], "show_in_editmode", text = "")
                    row.prop(modifiers[id.name], "show_viewport", text = "", emboss=False)
                    row.prop(modifiers[id.name], "show_render", text = "", emboss=False)
                    row.operator("apply.constraint", text = "", icon = "CHECKMARK", emboss=False).id = id.name
                    row.operator("delete.constraint", text = "", icon = "PANEL_CLOSE", emboss=False).id = id.name
                    box.prop(modifiers[id.name], "object", text = "Armature")
                if id.type == "SUBSURF":              
                    row = box.row()
                    row.operator("copy.constraint", text = "", icon = "MOD_SUBSURF", emboss=False).id = id.name
                    row.prop(modifiers[id.name], "name", text = "")
                    if modifiers[id.name].show_viewport == True:
                        row.prop(modifiers[id.name], "show_on_cage", text = "")
                        row.prop(modifiers[id.name], "show_in_editmode", text = "")
                    row.prop(modifiers[id.name], "show_viewport", text = "", emboss=False)
                    row.prop(modifiers[id.name], "show_render", text = "", emboss=False)
                    row.operator("apply.constraint", text = "", icon = "CHECKMARK", emboss=False).id = id.name
                    row.operator("delete.constraint", text = "", icon = "PANEL_CLOSE", emboss=False).id = id.name
                    row = box.row()
                    row.prop(modifiers[id.name], "subdivision_type", expand = True)
                    box.prop(modifiers[id.name], "levels", text = "Levels Viewport")
                    box.prop(modifiers[id.name], "render_levels", text = "Render")
                    box.prop(modifiers[id.name], "show_only_control_edges", text = "Optimal Display")
                if id.type == "SOLIDIFY":
                    row = box.row()
                    row.operator("copy.constraint", text = "", icon = "MOD_SOLIDIFY", emboss=False).id = id.name
                    row.prop(modifiers[id.name], "name", text = "")
                    if modifiers[id.name].show_viewport == True:
                        row.prop(modifiers[id.name], "show_on_cage", text = "")
                        row.prop(modifiers[id.name], "show_in_editmode", text = "")
                    row.prop(modifiers[id.name], "show_viewport", text = "", emboss=False)
                    row.prop(modifiers[id.name], "show_render", text = "", emboss=False)
                    row.operator("apply.constraint", text = "", icon = "CHECKMARK", emboss=False).id = id.name
                    row.operator("delete.constraint", text = "", icon = "PANEL_CLOSE", emboss=False).id = id.name
                    box.prop(modifiers[id.name], "thickness", text = "Thickness")
                    box.prop(modifiers[id.name], "offset", text = "Offset")
                    box.prop(modifiers[id.name], "use_even_offset", text = "Even Thickness")
                if id.type == "BEVEL":
                    row = box.row()
                    row.operator("copy.constraint", text = "", icon = "MOD_BEVEL", emboss=False).id = id.name
                    row.prop(modifiers[id.name], "name", text = "")
                    if modifiers[id.name].show_viewport == True:
                        row.prop(modifiers[id.name], "show_on_cage", text = "")
                        row.prop(modifiers[id.name], "show_in_editmode", text = "")
                    row.prop(modifiers[id.name], "show_viewport", text = "", emboss=False)
                    row.prop(modifiers[id.name], "show_render", text = "", emboss=False)
                    row.operator("apply.constraint", text = "", icon = "CHECKMARK", emboss=False).id = id.name
                    row.operator("delete.constraint", text = "", icon = "PANEL_CLOSE", emboss=False).id = id.name
                    row = box.row()
                    row.prop(modifiers[id.name], "affect", expand = True)
                    box.prop(modifiers[id.name], "width", text = "Amount")
                    box.prop(modifiers[id.name], "segments", text = "Segments")
                if id.type == "NODES":
                    try:
                        row = box.row()
                        row.operator("copy.constraint", text = "", icon = "GEOMETRY_NODES", emboss=False).id = id.name
                        row.prop(id.node_group, "name", text = "")
                        if modifiers[id.name].show_viewport == True:
                            row.prop(modifiers[id.name], "show_on_cage", text = "")
                            row.prop(modifiers[id.name], "show_in_editmode", text = "")
                        row.prop(modifiers[id.name], "show_viewport", text = "", emboss=False)
                        row.prop(modifiers[id.name], "show_render", text = "", emboss=False)
                        row.operator("apply.constraint", text = "", icon = "CHECKMARK", emboss=False).id = id.name
                        row.operator("delete.constraint", text = "", icon = "PANEL_CLOSE", emboss=False).id = id.name
                        row = box.row()
                        count = len(context.active_object.modifiers.get("GeometryNodes").node_group.inputs) 
                        for inputs in range(count):
                            inputid = inputs
                            inputs += 1
                            try:
                                if inputs > 1 :                    
                                    num = str(inputs)
                                    box.prop(modifiers[id.name], f'["Input_{num}"]', text = id.node_group.inputs[inputid].name)
                            except:
                                continue
                    except:
                        pass
    
    if not obj.modifiers:
        box.label(text = "No Available Modifiers")

def drawmodifiers1(self, context):
    layout = self.layout
    scene = context.scene
    obj = context.object
    box = layout.box()
    row = box.row()
    if scene.showmodifier == True:
        icon = "MODIFIER"
        text = "Quick Modifier"
    else:
        icon = "MODIFIER_DATA"
        text = "Show Modifier"
    row.prop(scene, "showmodifier", text = text, icon = icon, emboss=False)
    row = box.row()
    row.operator_menu_enum("object.modifier_add", "type")
    if obj.modifiers:
        row.template_modifiers()

def drawconstraints1(self, context):
    layout = self.layout
    box = layout.box()
    obj = context.object
    scene = context.scene
    row = box.row()
    if scene.showconstraints == True:
        if obj.mode != 'POSE':
            type = False
            icon = "CONSTRAINT"
        if obj.mode == 'POSE':
            type = True
            icon = "CONSTRAINT_BONE"
        text = "Quick Constraints"
    else:
        icon = "HIDE_OFF"
        text = "Show Constraints"

    row.prop(scene, "showconstraints", text = text, icon = icon, emboss=False)
    if scene.hideconstraints == True:
        hideicon = "HIDE_ON"
    else:
        hideicon = "HIDE_OFF"
    row.prop(scene, "hideconstraints", text = "", icon = hideicon, emboss=False)
    row.operator("all.constraint", text = "", icon = "CHECKMARK", emboss=False).type = 3
    row.operator("all.constraint", text = "", icon = "PANEL_CLOSE", emboss=False).type = 1
    if scene.showconstraints == True:
        row = box.row()
        row.operator_menu_enum("object.constraint_add", "type", text="Add Object Constraint")
        row = box.row()
        row.template_constraints(use_bone_constraints=False)

def drawconstraints(self, context):
    layout = self.layout
    box = layout.box()
    obj = context.object
    scene = context.scene
    bones = context.active_pose_bone
    try:
        row = box.row()
        if scene.showconstraints == True:
            if obj.mode != 'POSE':
                con = obj.constraints
                icon = "CONSTRAINT"
            if obj.mode == 'POSE':
                con = bones.constraints
                icon = "CONSTRAINT_BONE"
            text = "Quick Constraints"
        else:
            icon = "HIDE_OFF"
            text = "Show Constraints"

        row.prop(scene, "showconstraints", text = text, icon = icon, emboss=False)
        if scene.hideconstraints == True:
            hideicon = "HIDE_ON"
        else:
            hideicon = "HIDE_OFF"
        if con:
            row.prop(scene, "hideconstraints", text = "", icon = hideicon, emboss=False)
            row.operator("all.constraint", text = "", icon = "CHECKMARK", emboss=False).type = 3
            row.operator("all.constraint", text = "", icon = "PANEL_CLOSE", emboss=False).type = 1
        if scene.showconstraints == True:
            row = box.row()
            row.operator("add.constraints", text = "Child Of", icon = "CON_CHILDOF").type = "CHILD_OF"
            row.operator("add.constraints", text = "Damped Track", icon = "CON_TRACKTO").type = 'DAMPED_TRACK'
            row.operator("add.constraints", text = "Follow Path", icon = "CON_FOLLOWPATH").type = 'FOLLOW_PATH'
            for id in con[:]:
                if id.type == "CHILD_OF":
                    row = box.row()
                    row.operator("copy.constraint", text = "", icon = "CON_CHILDOF", emboss=False).id = id.name
                    row.prop(con[id.name], "name", text = "")
                    row.prop(con[id.name], "enabled", text = "", emboss=False)
                    row.operator("apply.constraint", text = "", icon = "CHECKMARK", emboss=False).id = id.name
                    row.operator("delete.constraint", text = "", icon = "PANEL_CLOSE", emboss=False).id = id.name
                    box.prop(con[id.name], "target", text = "Target")

                    if con[id.name].target:
                        if con[id.name].target.type == 'ARMATURE':
                            box.prop_search(con[id.name], "subtarget", con[id.name].target.data, "bones", text="Bone")

                            if con[id.name].subtarget and hasattr(con[id.name], "head_tail"):
                                row = box.row(align=True)
                                row.use_property_decorate = False
                                sub = box.row(align=True)
                                sub.prop(con[id.name], "head_tail")
                                # XXX icon, and only when bone has segments?
                                sub.prop(con[id.name], "use_bbone_shape", text="", icon='IPO_BEZIER')
                                sub.prop_decorator(con[id.name], "head_tail")
                        elif con[id.name].target.type in {'MESH', 'LATTICE'}:
                            box.prop_search(con[id.name], "subtarget", con[id.name].target, "vertex_groups", text="Vertex Group")
  
                    row = box.row()
                    row.operator("set.inverse", text = "Set Influence").id = id.name
                    row.operator("clear.inverse", text = "Clear Influence").id = id.name
                    row = box.row()
                    row.prop(con[id.name], "influence", text = "Influence")
                    row.operator("disable.constraint", text = "", icon = "CANCEL", emboss=False).id = id.name

                if id.type == "DAMPED_TRACK":
                    row = box.row()
                    row.operator("copy.constraint", text = "", icon = "CON_TRACKTO", emboss=False).id = id.name
                    row.prop(con[id.name], "name", text = "")
                    row.prop(con[id.name], "enabled", text = "", emboss=False)
                    row.operator("apply.constraint", text = "", icon = "CHECKMARK", emboss=False).id = id.name
                    row.operator("delete.constraint", text = "", icon = "PANEL_CLOSE", emboss=False).id = id.name
                    box.prop(con[id.name], "target", text = "Target")
                    
                    if con[id.name].target:
                        if con[id.name].target.type == 'ARMATURE':
                            box.prop_search(con[id.name], "subtarget", con[id.name].target.data, "bones", text="Bone")

                            if con[id.name].subtarget and hasattr(con[id.name], "head_tail"):
                                row = box.row(align=True)
                                row.use_property_decorate = False
                                sub = box.row(align=True)
                                sub.prop(con[id.name], "head_tail")
                                # XXX icon, and only when bone has segments?
                                sub.prop(con[id.name], "use_bbone_shape", text="", icon='IPO_BEZIER')
                                sub.prop_decorator(con[id.name], "head_tail")
                        elif con[id.name].target.type in {'MESH', 'LATTICE'}:
                            box.prop_search(con[id.name], "subtarget", con[id.name].target, "vertex_groups", text="Vertex Group")

                    row = box.row()
                    row.prop(con[id.name], "track_axis", expand=True)
                    row = box.row()
                    row.prop(con[id.name], "influence", text = "Influence")
                    row.operator("disable.constraint", text = "", icon = "CANCEL", emboss=False).id = id.name
                if id.type == "FOLLOW_PATH":
                    row = box.row()
                    row.operator("copy.constraint", text = "", icon = "CON_FOLLOWPATH", emboss=False).id = id.name
                    row.prop(con[id.name], "name", text = "")
                    row.prop(con[id.name], "enabled", text = "", emboss=False)
                    row.operator("apply.constraint", text = "", icon = "CHECKMARK", emboss=False).id = id.name
                    row.operator("delete.constraint", text = "", icon = "PANEL_CLOSE", emboss=False).id = id.name
                    box.prop(con[id.name], "target", text = "Target")
                    box.prop(con[id.name], "offset", text = "Offset")
                    row = box.row()
                    row.prop(con[id.name], "use_curve_follow", text = "Followe Curve", toggle = True)
                    row.prop(con[id.name], "use_curve_radius", text = "Curve Radius", toggle = True) 
                    row = box.row()
                    row.prop(con[id.name], "influence", text = "Influence")
                    row.operator("disable.constraint", text = "", icon = "CANCEL", emboss=False).id = id.name
    except:
        pass

def drawsimulation(self, context):
    obj = context.object

    layout = self.layout
    modifiers = obj.modifiers
    box = layout.box()
    row = box.row()
    row.label(text = "Simulation Cache", icon = "PHYSICS")
    row = box.row()
    try:
        modifiers["Cloth"]
        row.operator("object.modifier_remove", text = "Cloth", icon = "X").modifier="Cloth"
        row = box.row()
        row.label(text = "Cloth", icon = "MOD_CLOTH")
        jump = row.operator("bpy.ops", text = "", icon = "KEYFRAME_HLT", emboss=False)
        jump.object = str(modifiers["Cloth"].point_cache.frame_start)
        jump.id = "jump_frame"
        row.prop(modifiers["Cloth"], "show_viewport", text = "")
        row.prop(modifiers["Cloth"], "show_render", text = "")
        row = box.row()
        row.prop(modifiers["Cloth"].settings, "quality", text = "Quality Steps")
        row.prop(modifiers["Cloth"].settings, "time_scale", text = "Speed Multiplier")
        row = box.row()
        row.prop(modifiers["Cloth"].point_cache, "frame_start", text = "Start")
        row.prop(modifiers["Cloth"].point_cache, "frame_end", text = "End")
        row = box.row()
        row.prop(modifiers["Cloth"].settings, "vertex_group_mass", text = "Pin Group")
        row = box.row()
        row.label(text = "- Stiffness -")
        row = box.row()
        row.prop(modifiers["Cloth"].settings, "tension_stiffness", text = "Tension")
        row = box.row()
        row.prop(modifiers["Cloth"].settings, "compression_stiffness", text = "Compression")
        row = box.row()
        row.prop(modifiers["Cloth"].settings, "shear_stiffness", text = "Shear")
        row = box.row()
        row.prop(modifiers["Cloth"].settings, "bending_stiffness", text = "Bending")
        row = box.row()
        row.label(text = "- Damping -")
        row = box.row()
        row.prop(modifiers["Cloth"].settings, "tension_damping", text = "Tension")
        row = box.row()
        row.prop(modifiers["Cloth"].settings, "compression_damping", text = "Compression")
        row = box.row()
        row.prop(modifiers["Cloth"].settings, "shear_damping", text = "Shear")
        row = box.row()
        row.prop(modifiers["Cloth"].settings, "bending_damping", text = "Bending")
        row = box.row()
        row.prop(modifiers["Cloth"].collision_settings, "use_collision", text = "Object Collisions", toggle = True)
        if modifiers["Cloth"].collision_settings.use_collision == True:
            row.prop(modifiers["Cloth"].collision_settings, "use_self_collision", text = "Self Collisions", toggle = True)
            row = box.row()
            row.prop(modifiers["Cloth"].collision_settings, "collision_quality", text = "Quality")
            row.prop(modifiers["Cloth"].collision_settings, "distance_min", text = "Distance")
    except:
        row.operator("object.modifier_add", text = "Cloth", icon = "MOD_CLOTH").type='CLOTH'
    row = box.row()
    try:
        modifiers["Collision"]
        row.operator("object.modifier_remove", text = "Collision", icon = "X").modifier = 'Collision'
        row = box.row()
        row.label(text = "Collision", icon = "MOD_PHYSICS")
        if obj.collision.use == True:
            use = "HIDE_OFF"
        else:
            use = "HIDE_ON"
        row.prop(obj.collision, "use", text = "", toggle = True, icon = use, emboss = False)
        row = box.row()
        row.prop(obj.collision, "use_particle_kill", text = "Kill Particles", toggle = True)
        row = box.row()
        row.prop(obj.collision, "stickiness", text = "Stickiness")
        row = box.row()
        row.prop(obj.collision, "damping_factor", text = "Damping")
        row = box.row()
        row.prop(obj.collision, "damping_random", text = "Randomize")
        row = box.row()
        row.prop(obj.collision, "friction_factor", text = "Friction")
        row = box.row()
        row.prop(obj.collision, "friction_random", text = "Randomize")
    except:
        row.operator("object.modifier_add", text = "Collision", icon = "MOD_PHYSICS").type='COLLISION'

    row = box.row()
    row.operator("ptcache.bake_all", text = "Bake All Dynamics").bake=True
    row.operator("ptcache.free_bake_all", text = "Delete All Bakes")

def draw_world(context, box):
    scene = context.scene
    box.label(text = "World Data", icon = "WORLD")
    box = box.box()
    box.template_ID(scene, "world", new="world.new")
    world = context.scene.world

    box.prop(world, "use_nodes", icon='NODETREE')
    box.separator()

    box.use_property_split = True

    if world.use_nodes:
        ntree = world.node_tree
        node = ntree.get_output_node('EEVEE')

        if node:
            input = find_node_input(node, "Surface")
            if input:
                box.template_node_view(ntree, node, input)
            else:
                box.label(text="Incompatible output node")
        else:
            box.label(text="No output node")
    else:
        box.prop(world, "color")

def draw_cycles(scene, box):
    row = box.row()
    row.prop(scene.cycles, "device", text = "Device")
    row = box.row()
    row.prop(scene.cycles, "shading_system")
    row = box.row()
    row.label(text = "Samples")
    row = box.row()   
    row.prop(scene.cycles, "use_adaptive_sampling", text = "Noise Threshold")
    if scene.cycles.use_adaptive_sampling == True:
        row.prop(scene.cycles, "adaptive_threshold", text = "")
    row = box.row()
    row.prop(scene.cycles, "samples", text = "Max")
    if scene.cycles.use_adaptive_sampling == True:
        row.prop(scene.cycles, "adaptive_min_samples", text = "Min")
    row = box.row()   
    row.prop(scene.cycles, "time_limit", text = "Time Limit")
    row = box.row()
    row.prop(scene.cycles, "use_denoising", text = "Denoising")
    if scene.cycles.use_denoising == True:
        row.prop(scene.cycles, "denoiser", text = "")
        row = box.row()
        row.prop(scene.cycles, "denoising_input_passes", text = "")
        if scene.cycles.denoiser == "OPENIMAGEDENOISE":
            row.prop(scene.cycles, "denoising_prefilter", text = "")
    row = box.row()
    row.prop(scene.cycles, "use_light_tree", text = "Light Tree")
    if scene.cycles.use_light_tree == False:
        row.prop(scene.cycles, "light_sampling_threshold", text = "Light Threshold")
    row = box.row()
    if scene.lightpath == True:
        icon = "DOWNARROW_HLT"
    else:
        icon = "RIGHTARROW"
    row.prop(scene, "lightpath", text = "Light Path", icon = icon, emboss=False)
    if scene.lightpath == True:
        row = box.row()
        row.prop(scene.cycles, "max_bounces", text = "Total")
        row = box.row()
        row.prop(scene.cycles, "diffuse_bounces", text = "Diffuse")
        row = box.row()
        row.prop(scene.cycles, "glossy_bounces", text = "Glossy")
        row = box.row()
        row.prop(scene.cycles, "transmission_bounces", text = "Transmission")
        row = box.row()
        row.prop(scene.cycles, "volume_bounces", text = "Volume")
        row = box.row()
        row.prop(scene.cycles, "transparent_max_bounces", text = "Transparent")
        row = box.row()
        row.label(text = "Caustics")
        row = box.row()
        row.prop(scene.cycles, "caustics_reflective", toggle = True)
        row.prop(scene.cycles, "caustics_refractive", toggle = True)

def draw_eevee(scene, box):
    row = box.row()
    row.label(text = "Samples")
    row = box.row()
    row.prop(scene.eevee, "taa_render_samples", text = "Samples")
    row = box.row()
    row.prop(scene.eevee, "use_gtao", text = "Ambient Occlusion")
    if scene.eevee.use_gtao == True:
        row = box.row()
        row.prop(scene.eevee, "gtao_distance", text = "Distance")
        row = box.row()
        row.prop(scene.eevee, "gtao_factor", text = "Factor")
        row = box.row()
        row.prop(scene.eevee, "gtao_quality", text = "Trace Precision")
        row = box.row()
        row.prop(scene.eevee, "use_gtao_bent_normals", text = "Bent Normals")
        row.prop(scene.eevee, "use_gtao_bounce", text = "Bounce")
    row = box.row()
    row.prop(scene.eevee, "use_ssr", text = "Screen Space Reflection")
    if scene.eevee.use_ssr == True:
        row = box.row()
        row.prop(scene.eevee, "use_ssr_refraction", text = "Refraction")
        row.prop(scene.eevee, "use_ssr_halfres", text = "Half Res Trace")
        row = box.row()
        row.prop(scene.eevee, "ssr_quality", text = "Trace Precision")
        row = box.row()
        row.prop(scene.eevee, "ssr_max_roughness", text = "Max Roughness")
        row = box.row()
        row.prop(scene.eevee, "ssr_thickness", text = "Thickness")
        row = box.row()
        row.prop(scene.eevee, "ssr_border_fade", text = "Edge Fade")
        row = box.row()
        row.prop(scene.eevee, "ssr_firefly_fac", text = "Clamp")
    row = box.row()
    row.label(text = "Shadows")
    row = box.row()
    row.prop(scene.eevee, "shadow_cube_size", text = "Cube Size")
    row = box.row()
    row.prop(scene.eevee, "shadow_cascade_size", text = "Cascade Size")
    row = box.row()
    row.prop(scene.eevee, "use_shadow_high_bitdepth", text = "High Bit Depth")
    row.prop(scene.eevee, "use_soft_shadows", text = "Soft Shadows")
    row = box.row()
    row.prop(scene.eevee, "light_threshold", text = "Light Threshold")
    row = box.row()
    row.label(text = "Subsurface Scattering")
    row = box.row()
    row.prop(scene.eevee, "sss_samples", text = "Samples")
    row = box.row()
    row.prop(scene.eevee, "sss_jitter_threshold", text = "Jitter Threshol")
    row = box.row()
    row = box.row()
    row.label(text = "Volumetrics")
    row = box.row()
    row.prop(scene.eevee, "volumetric_start", text = "Start")
    row.prop(scene.eevee, "volumetric_end", text = "End")
    row = box.row()
    row.prop(scene.eevee, "volumetric_tile_size", text = "Tile Size")
    row = box.row()
    row.prop(scene.eevee, "volumetric_samples", text = "Samples")
    row = box.row()
    row.prop(scene.eevee, "use_volumetric_lights", text = "Volumetric Lights")
    if scene.eevee.use_volumetric_lights == True:
        row = box.row()
        row.prop(scene.eevee, "volumetric_light_clamp", text = "Light Clamping")
    row = box.row()
    row.prop(scene.eevee, "use_volumetric_shadows", text = "Volumetric Shadows")
    if scene.eevee.use_volumetric_shadows == True:
        row = box.row()
        row.prop(scene.eevee, "volumetric_shadow_samples", text = "Sample")
    row = box.row()
    row.prop(scene.eevee, "use_bloom", text = "Bloom")
    if scene.eevee.use_bloom == True:
        row = box.row()
        row.prop(scene.eevee, "bloom_color", text = "Color")
        row = box.row()
        row.prop(scene.eevee, "bloom_threshold", text = "Threshold")
        row = box.row()
        row.prop(scene.eevee, "bloom_intensity", text = "Intensity")
        row = box.row()
        row.prop(scene.eevee, "bloom_radius", text = "Radius")
        row = box.row()
        row.prop(scene.eevee, "bloom_knee", text = "Knee")
        row = box.row()
        row.prop(scene.eevee, "bloom_clamp", text = "Clamp")
    row = box.row()
    row.prop(scene.eevee, "use_motion_blur", text = "MotionBlur")
    if scene.eevee.use_motion_blur == True:
        row = box.row()
        row.prop(scene.eevee, "motion_blur_position", text = "Position")
        row = box.row()
        row.prop(scene.eevee, "motion_blur_shutter", text = "Shutter")
        row = box.row()
        row.prop(scene.eevee, "motion_blur_depth_scale", text = "Background Sepration")
        row = box.row()
        row.prop(scene.eevee, "motion_blur_max", text = "Max Blur")
        row = box.row()
        row.prop(scene.eevee, "motion_blur_steps", text = "Steps")

def drawfile_format(scene, box):
    row = box.row()
    if scene.render.image_settings.file_format != 'OPEN_EXR_MULTILAYER':
        row.prop(scene.render.image_settings, "color_mode", text = "Color", expand = True)
    if scene.render.image_settings.file_format == 'PNG':
        row.prop(scene.render.image_settings, "color_depth", text = "Color Depth", expand = True)
        row = box.row()
        row.prop(scene.render.image_settings, "compression", text = "Compression")
    if scene.render.image_settings.file_format == 'FFMPEG':
        row = box.row()
        row.prop(scene.render.ffmpeg, "format")
        row = box.row()
        row.prop(scene.render.ffmpeg, "codec")
    if scene.render.image_settings.file_format == 'OPEN_EXR_MULTILAYER':
        row = box.row()
        row.prop(scene.render.image_settings, "color_depth", expand = True)
        row = box.row()
        row.prop(scene.render.image_settings, "exr_codec")

def find_node_input(node, input_name):
    for input in node.inputs:
        if input.name == input_name:
            return input
    return None

def draw_scene_material(self, context):
    addon_prefs = addonPreferences.getAddonPreferences(context)
    if addon_prefs.scene_material_panel == True:
        layout = self.layout
        scene = context.scene
        layout.template_list("SCENEMATERIALS", "", bpy.data, "materials", scene, "mat_index")
        mat_list = []
        for mat in bpy.data.materials:
            mat_list.append(mat)
        mat = mat_list[scene.mat_index]
        row = layout.row()
        add = row.operator("data.blend", text = "Append")
        add.blend = mat.name
        add.type = "mat"
        add.subtype = "append"
        append = row.operator("data.blend", text = "Replace")
        append.blend = mat.name
        append.type = "mat"
        append.subtype = "replace"
        box = layout.box()
        row = box.row()
        box.label(text = "Fix Tools", icon = "TOOL_SETTINGS")
        row = box.row()
        indexmat = row.operator("fix.material", text = "Fix Scene Material")
        indexmat.type = "index"
        indexmat.mat = mat.name
        allmat = row.operator("fix.material", text = "Fix All Materials")
        allmat.type = "scene"
        if context.object.data.materials:
            row = box.row()
            objmat = row.operator("fix.material", text = "Fix Materials")
            objmat.type = "obj"

def register():
    bpy.types.EEVEE_MATERIAL_PT_context_material.append(draw_scene_material)

def unregister():
    bpy.types.EEVEE_MATERIAL_PT_context_material.remove(draw_scene_material)