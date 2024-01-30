import bpy

class Particles_Set_Frame_Start(bpy.types.Operator):
	bl_idname = "particles.set_frame_start"
	bl_label = "Particles Set Frame Start"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		obj = context.object
		if obj.particle_systems:
			particles_system = obj.particle_systems[obj.particle_systems.active_index]
			particles_data = particles_system.settings
			particles_data.frame_start = context.scene.frame_current
		self.report({"INFO"}, "Particle frame start set curent frame.")
		return {"FINISHED"}
	
class Particles_Set_Frame_End(bpy.types.Operator):
	bl_idname = "particles.set_frame_end"
	bl_label = "Particles Set Frame End"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		obj = context.object
		if obj.particle_systems:
			particles_system = obj.particle_systems[obj.particle_systems.active_index]
			particles_data = particles_system.settings
			particles_data.frame_end = context.scene.frame_current 
		self.report({"INFO"}, "Particle frame end set curent frame.")
		return {"FINISHED"}

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
                layout.operator("particles.set_frame_start", text = "", icon = "PREV_KEYFRAME", emboss=False)
                layout.prop(particles.settings, "frame_start", text="S", emboss=False)
                layout.operator("particles.set_frame_end", text = "", icon = "NEXT_KEYFRAME", emboss=False)
                layout.prop(particles.settings, "frame_end", text="E", emboss=False)
                layout.operator("frames.jump", text = "", icon = "KEYFRAME_HLT", emboss=False).frame = particles.settings.frame_start

        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

def draw_particles(self, context):
	obj = context.object
	layout = self.layout
	box = layout.box()
	row = box.row()
	
	row.label(text = "Particles", icon = "PARTICLES")
	row.operator("object.particle_system_remove", icon = "REMOVE", text = "", emboss=False)
	row.operator("object.particle_system_add", icon = "ADD", text = "", emboss=False)
	row.operator("particle.duplicate_particle_system", icon = "DUPLICATE", text = "", emboss=False).use_duplicate_settings=True

	box.template_list("PARTICLES", "", obj, "particle_systems", obj.particle_systems, "active_index")

	if obj.particle_systems:
		particles_system = obj.particle_systems[obj.particle_systems.active_index]
		particles_data = particles_system.settings

		row = box.row()
		row.label(text="Name")
		row.prop(particles_system, "name", text="")
		box.label(text="- Emission -")
		box.prop(particles_data, "emit_from", text="Emit From")
		box.prop(particles_data, "distribution", text="Distribution")
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

		box.prop(particles_data, "normal_factor", text="Normal")
		row = box.row()
		row.prop(particles_data, "object_align_factor", text="")
		box.prop(particles_data, "object_factor", text="Object Factor")
		box.prop(particles_data, "factor_random", text="Randomness")

		box.prop(particles_data, "use_rotations", text="Rotation", toggle=True)
		if particles_data.use_rotations == True:
			box.prop(particles_data, "rotation_mode", text="Orientation Axis")
			box.prop(particles_data, "rotation_factor_random", text="Randomness")
			box.prop(particles_data, "phase_factor", text="Phase")
			box.prop(particles_data, "phase_factor_random", text="Phase Randomness")
			box.prop(particles_data, "use_dynamic_rotation", text="Dynamic")
			box.prop(particles_data, "angular_velocity_mode", text="Axis")
			box.prop(particles_data, "angular_velocity_factor", text="Amount")

		box.label(text="- Render -")
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

		box.label(text="- Emittter -")
		row = box.row()
		row.prop(context.object, "show_instancer_for_viewport", text="Viewport")
		row.prop(context.object, "show_instancer_for_render", text="Render")

		row = box.row()
		row.operator("ptcache.bake_all", text = "Bake All Dynamics").bake=True
		row.operator("ptcache.free_bake_all", text = "Delete All Bakes")
	else:
		box.label(text = "Object has no Particles System")
		box.operator("object.particle_system_add", text = "New Particle", icon = "PARTICLES")

bpy.types.Scene.particles_properties = bpy.props.BoolProperty(
    name="Particles Propertie",
    description="Particles Propertie",
    default=False,
)

classes = (
			Particles_Set_Frame_Start,
			Particles_Set_Frame_End,
			PARTICLES,
		  )

def register(): 
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
  
def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)