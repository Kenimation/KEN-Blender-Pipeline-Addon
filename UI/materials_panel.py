import bpy
from .. import addonPreferences
from bpy.types import Panel
from bl_ui.properties_material import EEVEE_MATERIAL_PT_context_material as original_EEVEE_MATERIAL_PT_context_material
from cycles.ui import CYCLES_PT_context_material as original_CYCLES_PT_context_material

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
        draw_ken_material_panel(self, context)

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
        draw_ken_material_panel(self, context)

def draw_ken_material_panel(self, context):
    layout = self.layout
    obj = context.view_layer.objects.active
    space = context.space_data
    scene = context.scene
    slot = context.material_slot
    row = layout.row()
    lrow = row.row()
    lrow.alignment = 'LEFT'
    matnum = len(bpy.data.materials)-1
    mat = obj.active_material
    
    lrow.label(text = "Materials Library: Total "+str(matnum), icon = "MATERIAL")
    
    row = row.row()
    row.alignment = 'RIGHT'

    if obj.mode == "OBJECT":
        row.operator("object.material_slot_remove", text = "", icon = "REMOVE", emboss=False)
        row.operator("object.material_slot_add", text = "", icon = "ADD", emboss=False)

    if scene.mat_fake_use == True:
        icon = "FAKE_USER_ON"
    else:
        icon = "FAKE_USER_OFF"
    row.prop(scene, "mat_fake_use", text = "", icon = icon, emboss = False)

    row.operator("materials.clear", text = "", emboss = False, icon = "X")

    box = layout.box()
    row = box.row(align = True)
    row.template_list("MATERIALS", "", obj, "material_slots", obj, "active_material_index")
    row.template_list("SCENEMATERIALS", "", bpy.data, "materials", scene, "mat_index")

    addmat = bpy.data.materials[scene.mat_index]
    if addmat and addmat.name != 'Dots Stroke':
        row = box.row()
        row.operator("materials.append", text = "Append").mat = addmat.name
        row.operator("materials.replace", text = "Replace").mat = addmat.name

    row = box.row()
    row.template_ID(obj, "active_material", new="new.material")

    if slot:
        icon_link = 'MESH_DATA' if slot.link == 'DATA' else 'OBJECT_DATA'
        if mat:
            if obj.data.materials[obj.active_material_index]:
                row.operator("materials.select", icon = "RESTRICT_SELECT_OFF", emboss = False ,text = "").mat = mat.name
            row.prop(slot, "link", icon=icon_link, icon_only=True)

            if obj.mode == 'EDIT':
                row = box.row(align=True)
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

            row.template_ID(space, "pin_id")
            
        if obj.data.materials[obj.active_material_index]:
            box.label(text = "Prep Tools", icon = "TOOL_SETTINGS")
            box.operator("prep.material", text = "Prep Materials").type = "obj"

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

def menu_prep_material(self, context):
    if context.object.type == "MESH":
        if context.object.material_slots:
            for slot in context.object.material_slots:
                # Check if a material is assigned to the slot
                if slot.material is not None:
                    self.layout.separator()
                    self.layout.operator("prep.material", text = "Prep Material")
                    self.layout.operator("materials.clear", text = "Clear Material")
        else:
            self.layout.separator()
            self.layout.operator("new.material", text = "New Material")

def register(): 
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_prep_material)
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
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_prep_material)
    try:
        unregister_class(EEVEE_MATERIAL_PT_context_material)
        unregister_class(CYCLES_PT_context_material)
        register_class(original_EEVEE_MATERIAL_PT_context_material)
        register_class(original_CYCLES_PT_context_material)
    except RuntimeError:
        pass