import bpy
from bpy.types import WindowManager, Operator, Panel, Menu, UIList, PropertyGroup
from bpy.props import EnumProperty, BoolProperty, StringProperty, FloatProperty, IntProperty, CollectionProperty
import os
import bmesh
from . import assetsDraw, assetsDefs
from ..Minecraft import minecraftUI
from ..Anime import AnimeProperties, AnimeUI
from .. import addonPreferences, addon_updater_ops, icons

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                      classes
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class CAB_PG_Prop(PropertyGroup):
    ## Update functions
    def update_edge_bevelWeight(self, context):
        ''' Update function for bevelWeight property '''

        o  = bpy.context.object
        d  = o.data
        bm = bmesh.from_edit_mesh(d)

        bevelWeightLayer = bm.edges.layers.bevel_weight.verify()

        if self.whoToInfluence == 'Selected Elements':
            selectedEdges = [e for e in bm.edges if e.select]
            for e in selectedEdges: e[bevelWeightLayer] = self.edge_bevelWeight
        else:
            for e in bm.edges: e[bevelWeightLayer] = self.edge_bevelWeight

        bmesh.update_edit_mesh(d)

    def update_vert_bevelWeight(self, context):
        ''' Update function for bevelWeight property '''

        o  = bpy.context.object
        d  = o.data
        bm = bmesh.from_edit_mesh(d)

        bevelWeightLayer = bm.verts.layers.bevel_weight.verify()

        if self.whoToInfluence == 'Selected Elements':
            selectedVerts = [v for v in bm.verts if v.select]
            for v in selectedVerts: v[bevelWeightLayer] = self.vert_bevelWeight
        else:
            for v in bm.edges: v[bevelWeightLayer] = self.vert_bevelWeight

        bmesh.update_edit_mesh(d)

    def update_edge_Crease(self, context):
        ''' Update function for edgeCrease property '''

        o  = bpy.context.object
        d  = o.data
        bm = bmesh.from_edit_mesh(d)

        creaseLayer = bm.edges.layers.crease.verify()

        if self.whoToInfluence == 'Selected Elements':
            selectedEdges = [e for e in bm.edges if e.select]
            for e in selectedEdges: e[creaseLayer] = self.edge_Crease
        else:
            for e in bm.edges: e[creaseLayer] = self.edge_Crease

        bmesh.update_edit_mesh(d)

    def update_vert_Crease(self, context):
        ''' Update function for edgeCrease property '''

        o  = bpy.context.object
        d  = o.data
        bm = bmesh.from_edit_mesh(d)

        creaseLayer = bm.verts.layers.crease.verify()

        if self.whoToInfluence == 'Selected Elements':
            selectedVerts = [v for v in bm.verts if v.select]
            for v in selectedVerts: v[creaseLayer] = self.vert_Crease
        else:
            for v in bm.verts: v[creaseLayer] = self.vert_Crease

        bmesh.update_edit_mesh(d)

    ## Properties
    items = [
        ('All', 'All', ''),
        ('Selected Elements', 'Selected Elements', '')
    ]

    whoToInfluence: bpy.props.EnumProperty(
        description = "Influence all / selection",
        name        = "whoToInfluence",
        items       = items,
        default     = 'Selected Elements'
    )

    edge_bevelWeight: bpy.props.FloatProperty(
        description = "Edge Bevel Weight",
        name        = "Set Bevel Weight",
        min         = 0.0,
        max         = 1.0,
        step        = 0.1,
        default     = 0,
        update      = update_edge_bevelWeight
    )

    vert_bevelWeight: bpy.props.FloatProperty(
        description = "Vertex Bevel Weight",
        name        = "Set Bevel Weight",
        min         = 0.0,
        max         = 1.0,
        step        = 0.1,
        default     = 0,
        update      = update_vert_bevelWeight
    )

    edge_Crease: bpy.props.FloatProperty(
        description = "Edge Crease",
        name        = "Set Edge Crease",
        min         = 0.0,
        max         = 1.0,
        step        = 0.1,
        default     = 0,
        update      = update_edge_Crease
    )    

    vert_Crease: bpy.props.FloatProperty(
        description = "Vertex Crease",
        name        = "Set Vertex Crease",
        min         = 0.0,
        max         = 1.0,
        step        = 0.1,
        default     = 0,
        update      = update_vert_Crease
    )

class MATERIALS(bpy.types.UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ma = item.material
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            if ma:
                layout.prop(ma, "name", text="", emboss=False, icon_value=icon)
            else:
                layout.label(text="", translate=False, icon_value=icon)
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class SCENEMATERIALS(bpy.types.UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ma = item
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            if ma:
                layout.prop(ma, "name", text="", emboss=False, icon_value=icon)
                row = layout.row()
                row.scale_x = 0.2
                row.label(text = str(ma.users))
                select = layout.operator("data.blend", icon = "RESTRICT_SELECT_OFF", emboss = False ,text = "")
                select.type = "mat"
                select.subtype = "select"
                select.blend = ma.name
                layout.prop(ma,"use_fake_user", text = "", emboss=False)
                if ma.use_fake_user == False:
                    remove = layout.operator("data.blend", text = "", icon = "X", emboss=False)
                    remove.type = "mat"
                    remove.subtype = "remove"
                    remove.blend = str(ma.name)
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

    def filter_items(self,context,data,propname):
        filtered = []
        ordered = []
        items = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        filtered = [self.bitflag_filter_item] * len(items)

        ordered = helper_funcs.sort_items_by_name(items, "name")

        filtered_items = [o for o in bpy.data.materials if o.name !='Dots Stroke']

        for i, item in enumerate(items):
            if not item in filtered_items:
                filtered[i] &= ~self.bitflag_filter_item
                
        return filtered,ordered

class IMAGES(bpy.types.UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        img = item

        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!

            layout.prop(img, "name", text="", emboss=False, icon_value=icon)

            if item.source == 'MOVIE':
                layout.label(text="",icon="FILE_MOVIE")
            elif item.source == 'SEQUENCE':
                layout.label(text="",icon="RENDERLAYERS")
                
            row = layout.row()
            row.scale_x = 0.2
            row.label(text = str(img.users))

            if img.packed_files:
                packicon = "PACKAGE"
            else:
                packicon = "UGLYPACKAGE"

            pack = layout.operator("data.blend", text="", icon = packicon, emboss=False)
            pack.type = "img"
            pack.subtype = "pack"
            pack.blend = str(img.name)

            reload = layout.operator("data.blend", text = "", icon = "FILE_REFRESH", emboss=False)

            reload.type = "img"
            reload.subtype = "reload"
            reload.blend = str(img.name)
            if not img.has_data:
                layout.label(text="", icon="ERROR")
            else:
                layout.prop(img,"use_fake_user", text = "", emboss=False)
            if img.use_fake_user == False:
                remove = layout.operator("data.blend", text = "", icon = "X", emboss=False)
                remove.type = "img"
                remove.subtype = "remove"
                remove.blend = str(img.name)
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)
        return

    def filter_items(self,context,data,propname):
        filtered = []
        ordered = []
        items = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        filtered = [self.bitflag_filter_item] * len(items)

        ordered = helper_funcs.sort_items_by_name(items, "name")

        filtered_items = [o for o in bpy.data.images if o.name !='Render Result']

        for i, item in enumerate(items):
            if not item in filtered_items:
                filtered[i] &= ~self.bitflag_filter_item

        return filtered,ordered

class LIGHT(bpy.types.UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        lights = bpy.data.objects[item.name].data
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            col = layout.column(align=False)
            row1 = col.row()

            # Adjust the height of each row using the "split" method
            row1.prop(lights, "type", text="", icon="LIGHT_%s" % lights.type, icon_only=True)
            for obj in bpy.context.scene.objects:
                if obj.type == 'LIGHT' and obj.data.name == lights.name:
                    row1.prop(obj, "name", text="", emboss=False)

            row1.prop(lights, "color", text = "")
            row1.prop(lights, "energy", text = "")

            main_col = row1.column(align=False)
            intensity_row = main_col.row(align=True)
            exp_col = intensity_row.column(align=True)
            exp_col.scale_y = 0.5
            a1 = exp_col.operator("bpy.ops", text='', icon='TRIA_UP')
            a1.id = "light+0.5"
            a1.object = lights.name
            s1 = exp_col.operator("bpy.ops", text='', icon='TRIA_DOWN')
            s1.id = "light-0.5"
            s1.object = lights.name
            for obj in bpy.context.scene.objects:
                if obj.type == 'LIGHT' and obj.data.name == lights.name:
                    solo = row1.operator("solo.light", icon = "EVENT_S", text= "")
                    solo.light = obj.name
                    if obj in context.selected_objects or obj == context.view_layer.objects.active:
                        selecticon = "RESTRICT_SELECT_OFF"
                    else:
                        selecticon = "RESTRICT_SELECT_ON"
                    if obj.hide_viewport == False:
                        select = row1.operator("bpy.ops", text = "", icon = selecticon, emboss=False)
                        select.object = obj.name
                        select.id = "select"
                    row1.prop(obj, "hide_viewport", text = "", icon = "HIDE_OFF", emboss=False)

            remove = row1.operator("data.blend", text = "", icon = "X", emboss=False)
            remove.blend = lights.name
            remove.type = "light"
            remove.subtype = "remove"
            if context.scene.expandlight == True:
                assetsDraw.drawlight(col, lights)

        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

    def filter_items(self,context,data,propname):
        filtered = []
        ordered = []
        items = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        filtered = [self.bitflag_filter_item] * len(items)

        ordered = helper_funcs.sort_items_by_name(items, "name")

        filtered_items = [o for o in bpy.context.scene.objects if o.type=='LIGHT']

        for i, item in enumerate(items):
            if not item in filtered_items:
                filtered[i] &= ~self.bitflag_filter_item

        return filtered,ordered

class CAMERAS(bpy.types.UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        cam = bpy.data.objects[item.name].data
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            for obj in context.scene.objects:
                if obj.type == 'CAMERA' and obj.data.name == cam.name:

                    if context.scene.camera == bpy.data.objects[item.name]:
                        view = "RESTRICT_RENDER_OFF"
                    else:
                        view = "RESTRICT_RENDER_ON"
                    view = layout.operator("data.blend", text = "", icon = view, emboss=False)
                    view.blend = obj.name
                    view.type = "cam"
                    view.subtype = "view"

                    layout.prop(obj, "name", text="", emboss=False, icon= "CAMERA_DATA")

                    if obj in context.selected_objects or obj == context.view_layer.objects.active:
                        selecticon = "RESTRICT_SELECT_OFF"
                    else:
                        selecticon = "RESTRICT_SELECT_ON"
                    select = layout.operator("bpy.ops", text = "", icon = selecticon, emboss=False)
                    select.object = obj.name
                    select.id = "select"

            remove = layout.operator("data.blend", text = "", icon = "X", emboss=False)
            remove.blend = cam.name
            remove.type = "cam"
            remove.subtype = "remove"
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

    def filter_items(self,context,data,propname):
        filtered = []
        ordered = []
        items = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        filtered = [self.bitflag_filter_item] * len(items)

        ordered = helper_funcs.sort_items_by_name(items, "name")

        filtered_items = [o for o in bpy.context.scene.objects if o.type=='CAMERA']

        for i, item in enumerate(items):
            if not item in filtered_items:
                filtered[i] &= ~self.bitflag_filter_item

        return filtered,ordered

class MARKS(bpy.types.UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        m = item
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            try:
                layout.prop(m.camera, "name", text="", icon = "PMARKER_ACT", emboss=False)
                layout.prop(m, "name", text="", emboss=False)
            except:
                layout.prop(m, "name", text="", icon = "PMARKER_ACT", emboss=False)
            layout.prop(m, "frame", text="", emboss=False)
            delmark = layout.operator("bpy.ops", text = "", icon = "X", emboss=False)
            delmark.object = str(m.name)
            delmark.id = "del marker"

        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class COLLECTION(bpy.types.UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        coll = item
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            if coll:
                count = len(coll.objects)
                layout.prop(coll, "name", text="", emboss=False, icon_value=icon)
                layout.label(text="Count:"+str(count))
                layout.prop(coll, "hide_select", text = "", icon = "RESTRICT_SELECT_OFF", emboss=False)
                layout.prop(coll, "hide_viewport", text = "", icon = "HIDE_OFF", emboss=False)
                clean = layout.operator("data.blend", text = "", icon = "BRUSH_DATA", emboss=False)
                clean.blend = coll.name
                clean.type = "coll"
                clean.subtype = "clean"
                remove = layout.operator("data.blend", text = "", icon = "X", emboss=False)
                remove.blend = coll.name
                remove.type = "coll"
                remove.subtype = "remove"
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class PARTICLES(bpy.types.UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        particles = item
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), or a non-embossed text field,
            # this will also make the row easily selectable in the list! The later also enables ctrl-click rename.
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            # Note "data" names should never be translated!
            if particles:
                layout.prop(particles.settings, "name", text="", emboss=False, icon_value=icon)
                layout.prop(particles, "seed", text="Seed", emboss=False)
                layout.prop(particles.settings, "count", text="N", emboss=False)
                layout.prop(particles.settings, "frame_start", text="S", emboss=False)
                layout.prop(particles.settings, "frame_end", text="E", emboss=False)
                jump = layout.operator("bpy.ops", text = "", icon = "KEYFRAME_HLT", emboss=False)
                jump.object = str(particles.settings.frame_start)
                jump.id = "jump_frame"

        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class Assets_UI(bpy.types.Panel):
    bl_label = "KEN Pipeline"
    bl_idname = "OBJECT_PT_KEN_Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KEN Pipeline"
    
    def draw(self, context):
        addon_prefs = addonPreferences.getAddonPreferences(context)
        pcoll = preview_collections["main"]
        layout = self.layout
        scene = context.scene
        obj = context.view_layer.objects.active
        layout.label(text = "UI for Quick Tools Pipeline")
        box = layout.box()
        row = box.row()
        row.label(text = "Create by KEN", icon = 'RIGHTARROW')
        assetsDraw.drawheader(scene, row, obj)
        row.operator("open.addonprefsofaddon", icon = "SETTINGS", text = "")
        row = box.row()
        addon_updater_ops.check_for_update_background(context)
        addon_updater_ops.update_notice_box_ui(self, context, row)
        box = layout.box()
        row = box.row()
        row.prop(scene, "myProps", expand = True)
        row.scale_y = 1.25
        if scene.myProps == 'one':
            row = box.row()
            if scene.view == True:
                assetsDraw.draw_view(addon_prefs, context, box, row, obj)
                row = box.row()
            if obj:
                assetsDraw.draw_properties(addon_prefs, context, row, obj, pcoll)

                if obj.mode != 'EDIT':
                    assetsDraw.draw_transform(addon_prefs, context, box, obj)
                else:
                    
                    assetsDraw.drawedit_transform(addon_prefs, context, box, obj)
                    
                if obj.RIG_ID not in AnimeProperties.kenriglist:
                    if scene.object_properties == True:
                        assetsDraw.drawobj_properties(self,context, obj)
                    
                assetsDraw.draw_edit(scene, box)

                if scene.tools == True:
                    assetsDraw.draw_tools(scene, obj, self)

                if scene.mat == True:
                    if obj.type == 'MESH':
                        assetsDraw.drawmaterial_properties(self, context)

                if scene.advanced_option == True:
                    if obj:
                        assetsDraw.draw_data(self, context, obj)
                if addon_prefs.registered_name:
                    if all(item.registered_name in AnimeProperties.registered_name for item in addon_prefs.registered_name):
                        minecraftUI.draw_ken_mcrig(self, context, obj)
                for item in addon_prefs.registered_name:
                    if  item.registered_name == AnimeProperties.registered_name[1]:
                        AnimeUI.draw_ken_animerig(self, context, obj)
                if obj.RIG_ID in AnimeProperties.kenriglist:
                    if scene.object_properties == True:
                        assetsDraw.drawobj_properties(self,context, obj)

            else:
               row.label(text = "No Active Object.", icon = "OBJECT_DATAMODE")

        if scene.myProps == 'two':
            row = box.row()
            row.prop(scene, "mytools", expand = True)

            if scene.mytools == 'one':
                obj = context.view_layer.objects.active
                scene = context.scene
                row = box.row()
                row.scale_x = 1.75
                matnum = len(bpy.data.materials)-1
                row.label(text = "Materials Library: Total "+str(matnum), icon = "MATERIAL")
                mat_list = []
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
                row.scale_x = 0.75
                clean = row.operator("data.blend", icon = "BRUSH_DATA", text = "Clean")
                clean.type = "mat"
                clean.subtype = "clean"

                if obj:
                    if obj.type == "MESH":
                        state = "Object Material"
                        row = box.row()
                        row.template_list("MATERIALS", "", obj, "material_slots", obj, "active_material_index")
                    else:
                        state = "Scene Material: Object type does not have material."
                        row = box.row()
                else:
                    state = "Scene Material"
                    row = box.row()
                row.template_list("SCENEMATERIALS", "", bpy.data, "materials", scene, "mat_index")

                if obj:
                    if obj.type == "MESH":
                        try:
                            for mat in bpy.data.materials:
                                mat_list.append(mat)
                            mat = mat_list[scene.mat_index]
                            row = box.row()
                            add = row.operator("data.blend", text = "Append")
                            add.blend = mat.name
                            add.type = "mat"
                            add.subtype = "append"
                            append = row.operator("data.blend", text = "Replace")
                            append.blend = mat.name
                            append.type = "mat"
                            append.subtype = "replace"
                        except:
                            pass

                if scene.scene_mat == False:
                    if obj and obj.type == "MESH":
                        mat = obj.active_material
                    else:
                        try:
                            for mat in bpy.data.materials:
                                mat_list.append(mat)
                            mat = mat_list[scene.mat_index]
                        except:
                            pass
                else:
                    state = "Scene Material"
                    for mat in bpy.data.materials:
                        mat_list.append(mat)
                    mat = mat_list[scene.mat_index]

                row = box.row()
                if obj and obj.type == "MESH":
                    row.prop(scene, "scene_mat", icon = "SCENE_DATA", text = "")
                row.label(text = state)

                assetsDraw.drawmaterial(scene, box, row, obj, mat, state)

            if scene.mytools == 'two':
                row = box.row()
                row.label(text = "Lights Mixer", icon = "LIGHT_DATA")
                if scene.expandlight == False:
                    expand = "FULLSCREEN_ENTER"
                else:
                    expand = "FULLSCREEN_EXIT"
                row.prop(scene, "expandlight", text = "", icon = expand, emboss=False)
                try:
                    light_list = []
                    for light in bpy.data.objects:
                        light_list.append(light)
                    lights = light_list[scene.light_index]
                except:
                    pass
                try:
                    duplicate = row.operator("bpy.ops", text = "", icon = "DUPLICATE", emboss=False)
                    duplicate.id = "duplicate"
                    duplicate.object = lights.name
                except:
                    pass
                if scene.hide == True:
                    hideicon = "HIDE_ON"
                else:
                    hideicon = "HIDE_OFF"
                if scene.hide == False:
                    row.operator("bpy.ops", text = "", icon = "RESTRICT_SELECT_OFF", emboss=False).id = "select light"
                row.prop(scene, "hide", text = "", icon = hideicon, emboss=False)
                removeall = row.operator("data.blend", text = "", icon = "X", emboss=False)
                removeall.type = "light"
                removeall.subtype = "removeall"
                row = box.row()
                row.template_list("LIGHT", "", bpy.data, "objects", scene, "light_index")

                try:
                    row = box.row()
                    row.prop(scene, "light_type", icon = "OBJECT_DATA", text = "")
                    if scene.light_type == True:
                        if obj.type == 'LIGHT':
                            text = "Object Light Data"
                            lights = obj.data
                        else:
                            text = "List Light Data"
                            lights = lights.data
                    else:
                        lights = lights.data
                        text = "List Light Data"
                    row.label(text = text)
                    assetsDraw.drawlight(box, lights)
                except:
                    box.label(text = "Scene has No Light")

                assetsDraw.draw_world(context, box)

            if scene.mytools == 'three':
                row = box.row()
                row.label(text = "Cameras Manager", icon = "CAMERA_DATA")
                if scene.marker == True:
                    icon = "PMARKER_ACT"
                else:
                    icon = "PMARKER_SEL"
                row.prop(scene, "marker", text = "", icon = icon, emboss=False)
                if scene.marker == False:
                    if scene.hide == True:
                        hideicon = "HIDE_ON"
                    else:
                        hideicon = "HIDE_OFF"
                    row.operator("bpy.ops", text = "", icon = "RESTRICT_SELECT_OFF", emboss=False).id = "select cam"
                try:
                    cam_list = []
                    for cam in bpy.data.objects:
                        cam_list.append(cam)
                    cam = cam_list[scene.cam_index]
                except:
                    pass
                try:
                    duplicate = row.operator("bpy.ops", text = "", icon = "DUPLICATE", emboss=False)
                    duplicate.id = "duplicate"
                    duplicate.object = cam.name
                except:
                    pass 

                row = box.row()
                row.template_list("CAMERAS", "", bpy.data, "objects", scene, "cam_index")
                if scene.marker == True:
                    assetsDraw.draw_mark(scene, box, row)

                if cam.type == 'CAMERA':
                    if scene.cam_quick == True:
                        icon = "DOWNARROW_HLT"
                    else:
                        icon = "RIGHTARROW"
                    box.prop(scene, "cam_quick", text = "Quick Camera", icon = icon, emboss=False)
                    if scene.cam_quick == True:
                        type = "list"
                        cambox = box.box()
                        assetsDraw.drawcam(context, cambox, cam, type)
                        
                    if scene.cam_shake == True:
                        icon = "DOWNARROW_HLT"
                    else:
                        icon = "RIGHTARROW"
                    box.prop(context.scene, "cam_shake", text = "Camera Shakify", icon = icon, emboss=False)
                    if context.scene.cam_shake == True:
                        assetsDraw.draw_cam_shake(box, cam)


                    if scene.cam_save == True:
                        icon = "DOWNARROW_HLT"
                    else:
                        icon = "RIGHTARROW"
                    box.prop(context.scene, "cam_save", text = "Camera Save List", icon = icon, emboss=False)
                    if context.scene.cam_save == True:
                        assetsDraw.draw_save_cam(context, box)

                else:
                    box.label(text = "No Selected Camera")
            
            if scene.mytools == 'four':
                row = box.row()
                imgnum = len(bpy.data.images)-1
                row.scale_x = 1.75
                row.label(text = "Image Resources: Total "+str(imgnum), icon = "IMAGE_DATA")
                assetsDraw.drawimage(scene, box, row)

        if scene.myProps == 'three':
            row = box.row()
            row.label(icon = "SCENE_DATA")
            row.prop(scene, "name", text = "")
            row = box.row()
            row.label(text = "Output:", icon = "OUTPUT")
            row = box.row()
            row.label(text = "Resolution")
            row = box.row()
            row.prop(scene.render, "resolution_x", text = "X")
            row.prop(scene.render, "resolution_y", text = "Y")
            row = box.row()
            row.prop(scene.render, "fps", text = "FPS")
            row = box.row()
            row.prop(scene.render, "film_transparent", text = "Transparent")
            row = box.row()
            row.label(text = "Frame Range")
            row = box.row()
            row.prop(scene, "frame_start", text = "Start")
            row.prop(scene, "frame_end", text = "End")
            row = box.row()
            row.prop(scene, "frame_step", text = "Step")
            row = box.row()
            row.label(text = "File:")
            row = box.row()
            row.prop(scene.render, "filepath", text = "")
            row = box.row()
            row.prop(scene.render, "use_file_extension", toggle = True)
            row.prop(scene.render, "use_render_cache", toggle = True)
            row = box.row()
            row.template_image_settings(scene.render.image_settings, color_management=False)
            row = box.row()
            row.label(text = "Color Management:")
            row = box.row()
            row.prop(scene.render.image_settings, "color_management", expand = True)
            row = box.row()
            row.prop(scene.sequencer_colorspace_settings, "name", text = "Color Space")
            layout = self.layout
            box = layout.box()
            row = box.row()
            row.label(text = "Render:", icon = "SCENE")
            row = box.row()
            row.prop(scene, "finalrender", text = "", icon = "RESTRICT_RENDER_OFF")
            if scene.finalrender == True:
                row.operator("render.render", text = "Render Image", icon = "RENDER_STILL")
                row.operator("render.render", text = "Render Animation", icon = "RENDER_ANIMATION").animation = True
            else:
                row.operator("render.opengl", text = "Viewport Render", icon = "RENDER_STILL")
                row.operator("render.opengl", text = "Viewport Animation", icon = "RENDER_ANIMATION").animation = True
            if scene.cycles.denoiser == 'OPTIX':
                row = box.row()
                row.operator("cycles.denoise_animation", text = "Optix Denoising Animation")
            row = box.row()
            row.label(text = "Render Settings")
            row = box.row()
            row.prop(scene.render, "engine", text = "Render Engine")
            if context.scene.render.engine in ["CYCLES"]:
                assetsDraw.draw_cycles(scene, box)
            if context.scene.render.engine in ["BLENDER_EEVEE"]:
                assetsDraw.draw_eevee(scene, box)


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#                   (un)register
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

preview_collections = {}

classes = (
            COLLECTION,
            SCENEMATERIALS,
            MATERIALS,
            CAMERAS,
            MARKS,
            PARTICLES,
            IMAGES,
            LIGHT,
            CAB_PG_Prop,
            Assets_UI,
          )

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        
    bpy.types.Scene.CAB_PG_Prop = bpy.props.PointerProperty(type = CAB_PG_Prop)

    icon = icons.icons("icons")
    pcoll = icon.getColl()
    icon.load(pcoll)
    preview_collections["main"] = pcoll

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()