import bpy

class Toggle_assets_brower(bpy.types.Operator):
	bl_idname = "toggle.assets_brower"
	bl_label = "Toogle Assets Brower"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		bpy.context.area.ui_type = 'ASSETS'
		bpy.ops.screen.area_split(direction='VERTICAL', factor=0.5)
		bpy.context.area.ui_type = 'VIEW_3D'
		self.report({"INFO"}, "Toogle Assets Brower")
		return {'FINISHED'}
	
classes = (
			Toggle_assets_brower,
		  )

def register(): 
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
  
def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)