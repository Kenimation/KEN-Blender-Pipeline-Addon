import bpy

class OBJECT_OT_select_by_name_type(bpy.types.Operator):
    '''Select Duplicated Objects by Name - Type

-Alt Click = Insert Keys (Loc / Rot / Scale)'''

    bl_idname = "object.select_by_name_type"
    bl_label = "Select by Name-Type"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'OBJECT')


    def invoke(self, context, event):



        cur_frame = bpy.context.scene.frame_current

        def insert_keys(frame):
            sel_ob = bpy.context.selected_objects
            for o in sel_ob:
                o.keyframe_insert(data_path = 'location', frame=frame)
                o.keyframe_insert(data_path = 'scale', frame=frame)
                o.keyframe_insert(data_path = 'rotation_euler', frame=frame)


        # Select Objects by Name / Type
        def select_by_name_type():

            act_name = bpy.context.view_layer.objects.active.name
            act_type = bpy.context.view_layer.objects.active.type

         
            name = act_name.split('.')
            name_spl = name[0]

            for obj in bpy.context.scene.objects:
                if obj.name.startswith(name_spl) and obj.type == act_type:
                    obj.select_set(1)

        if event:
            select_by_name_type()


            sel_ob = bpy.context.selected_objects
            act_ob = bpy.context.view_layer.objects

            first_ob = sel_ob[0]
            last_ob = sel_ob[-1]


            # Active Object = Last in Selected
            for o in bpy.context.selected_objects:
                if act_ob.active != first_ob and act_ob.active != last_ob:
                    act_ob.active = last_ob

                if act_ob.active == first_ob:
                    act_ob.active = last_ob

                if act_ob.active == last_ob:
                    act_ob.active = last_ob

        if event.alt:
            insert_keys(cur_frame)




        return {'FINISHED'}

class OBJECT_OT_offset_loc_rot_scale(bpy.types.Operator):
    '''Offset Animated - Location, Rotation, Scale'''
    bl_idname = "object.offset_loc_rot_scale"
    bl_label = "Offset Loc Rot Scale"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'OBJECT' and
                len(context.selected_objects) != 0)



    def execute(self, context):

        sel_ob = bpy.context.selected_objects
        act_ob = bpy.context.active_object

        # Ref 
        rev_bool = context.scene.revers_anim_offest
        
        frames_to_offset = context.scene.anim_offest_frames
#-------------------------------------------


        # Location Rotation Scale Offset
        def offset_loc_rot_scale():
            sel_ob = bpy.context.selected_objects
            offset = 0
            if rev_bool:
                sel_ob = reversed(sel_ob)

            for o in sel_ob:
                anim_data = o.animation_data
                if anim_data:
                    action = anim_data.action
                    if action:   
                        fcurves = action.fcurves
                        if fcurves:
                            for c in fcurves:
                                keyframePoints = c.keyframe_points

                                for kf in keyframePoints:
                                    kf.co[0] += offset
                                    kf.handle_left[0] += offset
                                    kf.handle_right[0] += offset

                offset += frames_to_offset


#--------------------------------------------

        # Check if Object has Anim Data
        anim_data = act_ob.animation_data

        if anim_data:
            if anim_data.action:
                if anim_data.action.fcurves:
                     offset_loc_rot_scale()


        return {'FINISHED'}

class OBJECT_OT_offset_location(bpy.types.Operator):
    '''Offset Animated - Location'''
    bl_idname = "object.offset_location"
    bl_label = "Offset Animated Location"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'OBJECT' and
                len(context.selected_objects) != 0)



    def execute(self, context):


        sel_ob = bpy.context.selected_objects
        act_ob = bpy.context.active_object

        # Ref 
        rev_bool = context.scene.revers_anim_offest
        
        frames_to_offset = context.scene.anim_offest_frames
#-------------------------------------------



        # Location Offset
        def offset_loc():
            sel_ob = bpy.context.selected_objects
            offset = 0
            if rev_bool:
                sel_ob = reversed(sel_ob)

            for o in sel_ob:
                anim_data = o.animation_data
                if anim_data:
                    action = anim_data.action
                    if action:
                        fcurves = action.fcurves
                        if fcurves:
                            for c in fcurves:
                                if c.data_path.endswith(('location')):
                                    keyframePoints = c.keyframe_points

                                    for kf in keyframePoints:
                                        kf.co[0] += offset
                                        kf.handle_left[0] += offset
                                        kf.handle_right[0] += offset

                offset += frames_to_offset

 
#--------------------------------------------


        # Check if Object  Anim Data
        anim_data = act_ob.animation_data

        if anim_data:
            if anim_data.action:
                if anim_data.action.fcurves:
                    offset_loc()


        return {'FINISHED'}

class OBJECT_OT_offset_rotation(bpy.types.Operator):
    '''Offset Animated - Rotation'''
    bl_idname = "object.offset_rotation"
    bl_label = "Offset Animated Rotation"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'OBJECT' and
                len(context.selected_objects) != 0)



    def execute(self, context):


        sel_ob = bpy.context.selected_objects
        act_ob = bpy.context.active_object

        # Ref 
        rev_bool = context.scene.revers_anim_offest
        
        frames_to_offset = context.scene.anim_offest_frames
#-------------------------------------------



        # Rotation Offset
        def offset_rot():
            sel_ob = bpy.context.selected_objects
            offset = 0
            if rev_bool:
                sel_ob = reversed(sel_ob)

            for o in sel_ob:
                anim_data = o.animation_data
                if anim_data:
                    action = anim_data.action
                    if action:
                        fcurves = action.fcurves
                        if fcurves:
                            for c in fcurves:
                                if c.data_path.endswith(('rotation_euler')):
                                    keyframePoints = c.keyframe_points

                                    for kf in keyframePoints:
                                        kf.co[0] += offset
                                        kf.handle_left[0] += offset
                                        kf.handle_right[0] += offset

                offset += frames_to_offset

 
#--------------------------------------------


        # Check if Object  Anim Data
        anim_data = act_ob.animation_data

        if anim_data:
            if anim_data.action:
                if anim_data.action.fcurves:
                    offset_rot()


        return {'FINISHED'}

class OBJECT_OT_offset_scale(bpy.types.Operator):
    '''Offset Animated - Scale'''
    bl_idname = "object.offset_scale"
    bl_label = "Offset Animated Scale"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode == 'OBJECT' and
                len(context.selected_objects) != 0)



    def execute(self, context):


        sel_ob = bpy.context.selected_objects
        act_ob = bpy.context.active_object

        # Ref 
        rev_bool = context.scene.revers_anim_offest
        
        frames_to_offset = context.scene.anim_offest_frames
#-------------------------------------------



        # Scale Offset
        def offset_scale():
            sel_ob = bpy.context.selected_objects
            offset = 0
            if rev_bool:
                sel_ob = reversed(sel_ob)

            for o in sel_ob:
                anim_data = o.animation_data
                if anim_data:
                    action = anim_data.action
                    if action:
                        fcurves = action.fcurves
                        if fcurves:
                            for c in fcurves:
                                if c.data_path.endswith(('scale')):
                                    keyframePoints = c.keyframe_points

                                    for kf in keyframePoints:
                                        kf.co[0] += offset
                                        kf.handle_left[0] += offset
                                        kf.handle_right[0] += offset

                offset += frames_to_offset

 
#--------------------------------------------


        # Check if Object  Anim Data
        anim_data = act_ob.animation_data

        if anim_data:
            if anim_data.action:
                if anim_data.action.fcurves:
                    offset_scale()


        return {'FINISHED'}

class OBJECT_OT_offset_keyframes_similar_bones(bpy.types.Operator):
    '''Offset Keyframes on Similar - by name of active Bone'''
    bl_idname = "object.offset_keyframes_similar_bones"
    bl_label = "Offset Keyframes - Similar Bones"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return (context.object is not None and
        context.mode == 'POSE' and len(context.selected_pose_bones) != 0)


    def execute(self, context):
        
        def select_similar_by_act_bone_name():
        
            act_bone = bpy.context.active_pose_bone

            name = act_bone.name.split('.')


            if len(name) == 1:
                get_name = name[0] + '*'  
                bpy.ops.object.select_pattern(pattern=get_name, case_sensitive=False)  
                
            if len(name) > 1 and len(name) < 3:
                if name[1] != 'L' and name[1] != 'R':
                    get_name = name[0] + '*'
                    bpy.ops.object.select_pattern(pattern=get_name, case_sensitive=False)      

             
            # If Name has 'L' of 'R' after first '.'  
            if len(name) > 1:
                if name[1] == 'L':
                    name_l = name[0] + '.' + name[1]
                    get_name_l = name_l + '*'
                    bpy.ops.object.select_pattern(pattern=get_name_l, case_sensitive=False)
                
                if name[1] == 'R':
                    name_r = name[0] + '.' + name[1]
                    get_name_r = name_r + '*'
                    bpy.ops.object.select_pattern(pattern=get_name_r, case_sensitive=False)    
                

            # If Name ends with 'L' or 'R' 
            if len(name) > 1:
                if name[-1] == 'L':
                    name_l = name[0] + '*' + name[-1]
                    bpy.ops.object.select_pattern(pattern=name_l, case_sensitive=False) 
                    
                          
            if len(name) > 1:
                if name[-1] == 'R':
                    name_r = name[0] +  '*' + name[-1]
                    bpy.ops.object.select_pattern(pattern=name_r, case_sensitive=False)         
        
        
        
        
        # Ref -----------------------------------------------------
        rev_bool = context.scene.revers_anim_offest
        frames_to_offset = context.scene.anim_offest_frames

        sel_bones = bpy.context.selected_pose_bones
        pose_bones = bpy.context.object.pose.bones

        def armature_name():
            ob = bpy.context.object
            return ob.name
      
        def bone_keyframes_offset():
            
            sel_bones = bpy.context.selected_pose_bones

            arm_name = armature_name()
            arm = bpy.data.objects[arm_name]
            act_bone = bpy.context.active_pose_bone

            offset = 0
            
            if rev_bool:
                sel_bones = reversed(sel_bones) 

            for b in sel_bones:
                act_bone = b
                act_bone_name = b.name

                if arm.animation_data:
                    if arm.animation_data.action:

                        fc = arm.animation_data.action.fcurves

                        for c in fc:
                            if act_bone_name in c.data_path:

                                keyframePoints = c.keyframe_points

                                for kf in keyframePoints:
                                    kf.co[0] += offset
                                    kf.handle_left[0] += offset
                                    kf.handle_right[0] += offset

                        offset += frames_to_offset


        select_similar_by_act_bone_name()
        bone_keyframes_offset()


        return {'FINISHED'}
  
class OBJECT_OT_offset_keyframes_selected_bones(bpy.types.Operator):
    '''Offset Keyframes on Selected Bones'''
    bl_idname = "object.offset_keyframes_selected_bones"
    bl_label = "Offset Keyframes - Selected Bones"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return (context.object is not None and
        context.mode == 'POSE' and len(context.selected_pose_bones) != 0)


    def execute(self, context):
        
        # Ref
        rev_bool = context.scene.revers_anim_offest
        frames_to_offset = context.scene.anim_offest_frames

        sel_bones = bpy.context.selected_pose_bones
        pose_bones = bpy.context.object.pose.bones

        def armature_name():
            ob = bpy.context.object
            return ob.name
      
        def bone_keyframes_offset():
            
            sel_bones = bpy.context.selected_pose_bones

            arm_name = armature_name()
            arm = bpy.data.objects[arm_name]
            act_bone = bpy.context.active_pose_bone

            offset = 0
            
            if rev_bool:
                sel_bones = reversed(sel_bones) 

            for b in sel_bones:
                act_bone = b
                act_bone_name = b.name

                if arm.animation_data:
                    if arm.animation_data.action:

                        fc = arm.animation_data.action.fcurves

                        for c in fc:
                            if act_bone_name in c.data_path:

                                keyframePoints = c.keyframe_points

                                for kf in keyframePoints:
                                    kf.co[0] += offset
                                    kf.handle_left[0] += offset
                                    kf.handle_right[0] += offset

                        offset += frames_to_offset

        bone_keyframes_offset()


        return {'FINISHED'}
    
class PANEL_PT_Animation_Tool(bpy.types.Panel):
    bl_label = "KEN Action"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = "KEN Action" 
    bl_options = {'DEFAULT_CLOSED'}


    def draw(self, context):
        layout = self.layout

        # Offset Bone Keyframes -----------------------------------------------------

        box = layout.box() 
        row = box.row()
        row.label(text='Copy/Paste Keyframes', icon='DUPLICATE')
        row = box.row()
        row.operator("action.copy", text='Copy', icon = "COPYDOWN")
        row = box.row(align=True)
        row.scale_y = 1.2
        row.operator("action.paste", text='Paste', icon = "PASTEDOWN").flipped=False
        if context.object.mode == "POSE":
            row.operator("action.paste", text='Flipped Paste', icon = "PASTEFLIPDOWN").flipped=True
        row = box.row()
        row.label(text='Offset Keyframes', icon='DECORATE_KEYFRAME')
        if context.object.mode == "OBJECT":
            row.operator("object.select_by_name_type", text='' , icon='RESTRICT_SELECT_OFF', emboss = False)
        row = box.row()
        row.prop(context.scene, "anim_offest_frames")
        row.prop(context.scene, "revers_anim_offest", icon = "ARROW_LEFTRIGHT")
        if context.object.mode == "OBJECT":
            row = box.row()
            row.operator("object.offset_loc_rot_scale", text='Set Offset', icon='ONIONSKIN_ON')
            row = box.row(align=True)
            row.scale_y = 1.2
            row.operator("object.offset_location", text='Location')
            row.operator("object.offset_rotation", text='Rotation')
            row.operator("object.offset_scale", text='Scale')
        elif context.object.mode == "POSE":     
            row = box.row(align=True)
            row.scale_y = 1.2
            row.operator("object.offset_keyframes_similar_bones", text='Similar', icon='BONE_DATA')
            row.operator("object.offset_keyframes_selected_bones", text='Selected', icon='RESTRICT_SELECT_OFF')

        #---------------------------- Add Cycle Modifier ---------------------------------

classes = (
            OBJECT_OT_select_by_name_type,
            OBJECT_OT_offset_loc_rot_scale,
            OBJECT_OT_offset_location,
            OBJECT_OT_offset_rotation,
            OBJECT_OT_offset_scale,
            OBJECT_OT_offset_keyframes_similar_bones,
            OBJECT_OT_offset_keyframes_selected_bones,
            PANEL_PT_Animation_Tool,
          )
          
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    #-----------------------Reverse Offset Bool-------------------


    bpy.types.Scene.revers_anim_offest = bpy.props.BoolProperty(
        name="",
        description="REVERSED OFFSET",
        default = False
    )

    #-------------------------------------------------------------
    
    #----------------------- Frames to Offset Bool ---------------
    
    bpy.types.Scene.anim_offest_frames = bpy.props.IntProperty(
        name="Offset Frames",
        default=1,
        description="Frames to Offset",
    )

    #-------------------------------------------------------------


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.revers_anim_offest
    del bpy.types.Scene.anim_offest_frames


if __name__ == "__main__":
    register() 