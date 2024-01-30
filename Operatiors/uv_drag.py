# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
from bpy.props import *


################################################
# アドオン情報

##################################################
##################################################


##################################################
##################################################
# ↓ キーマップ登録ここから ↓



################################################


# ↑ キーマップ登録ここまで必要 ↑
################################################
################################################


##################################################
# アドオン設定


################################################
class UVDRAG_OT_uv_Drag(bpy.types.Operator):
	bl_idname = "uvdrag.toolkit_quick_drag_island"
	bl_label = "Quick Drag Move Island"
	bl_description = "Quick drag Move island"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):

		if context.scene.tool_settings.use_uv_select_sync is True:
			current_mode = tuple(context.tool_settings.mesh_select_mode)
			context.tool_settings.mesh_select_mode = (False, False, True)  # Face
			bpy.ops.uv.select_all(action='DESELECT')
			bpy.ops.uv.select_linked_pick('INVOKE_DEFAULT')
			bpy.ops.transform.translate('INVOKE_DEFAULT')
			context.tool_settings.mesh_select_mode = current_mode
			return {'FINISHED'}
		else:
			bpy.ops.uv.select_all(action='DESELECT')
			bpy.ops.uv.select_linked_pick('INVOKE_DEFAULT')
			bpy.ops.transform.translate('INVOKE_DEFAULT')
			return {'FINISHED'}

################################################
class UVDRAG_OT_uv_Rotate(bpy.types.Operator):
	bl_idname = "uvdrag.toolkit_quick_drag_rotate_island"
	bl_label = "Quick Drag Rotate Island"
	bl_description = "Quick drag Rotate island"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):

		if context.scene.tool_settings.use_uv_select_sync is True:
			current_mode = tuple(context.tool_settings.mesh_select_mode)
			context.tool_settings.mesh_select_mode = (False, False, True)  # Face
			bpy.ops.uv.select_all(action='DESELECT')
			bpy.ops.uv.select_linked_pick('INVOKE_DEFAULT')
			bpy.ops.transform.rotate('INVOKE_DEFAULT')
			context.tool_settings.mesh_select_mode = current_mode
			return {'FINISHED'}
		else:
			bpy.ops.uv.select_all(action='DESELECT')
			bpy.ops.uv.select_linked_pick('INVOKE_DEFAULT')
			bpy.ops.transform.rotate('INVOKE_DEFAULT')
			return {'FINISHED'}




################################################
# クラスの登録
classes = (
UVDRAG_OT_uv_Drag,
UVDRAG_OT_uv_Rotate,
)


################################################
addon_keymaps = []
def register():
	################################################
	# クラスの登録
	for cls in classes:
		bpy.utils.register_class(cls)

################################################
def unregister():
	#クラスの削除
	for cls in classes:
		bpy.utils.unregister_class(cls)

################################################
if __name__ == "__main__":
	register()
