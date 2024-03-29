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
            any_keyframe_selected = False
            offset = 0
            if not rev_bool:
                sel_ob = reversed(sel_ob)
            else:
                sel_ob = sel_ob

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
                                        if kf.select_control_point:
                                            any_keyframe_selected = True
                                            kf.co[0] += offset
                                            kf.handle_left[0] += offset
                                            kf.handle_right[0] += offset
                                        if not any_keyframe_selected:
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
            any_keyframe_selected = False
            offset = 0
            if not rev_bool:
                sel_ob = reversed(sel_ob)
            else:
                sel_ob = sel_ob

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
                                        if kf.select_control_point:
                                            any_keyframe_selected = True
                                            kf.co[0] += offset
                                            kf.handle_left[0] += offset
                                            kf.handle_right[0] += offset
                                        if not any_keyframe_selected:
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
            any_keyframe_selected = False
            offset = 0
            if not rev_bool:
                sel_ob = reversed(sel_ob)
            else:
                sel_ob = sel_ob

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
                                        if kf.select_control_point:
                                            any_keyframe_selected = True
                                            kf.co[0] += offset
                                            kf.handle_left[0] += offset
                                            kf.handle_right[0] += offset
                                        if not any_keyframe_selected:
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

class OBJECT_OT_offset_selected_keyframes(bpy.types.Operator):
    '''Offset Animated - Location, Rotation, Scale'''
    bl_idname = "offset.selected_keyframes"
    bl_label = "Offset Keyframes"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode != 'EDIT' and
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
            any_keyframe_selected = False
            offset = 0
            if not rev_bool:
                sel_ob = reversed(sel_ob)
            else:
                sel_ob = sel_ob

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
                                    if kf.select_control_point:
                                        any_keyframe_selected = True
                                        kf.co[0] += offset
                                        kf.handle_left[0] += offset
                                        kf.handle_right[0] += offset
                                    if not any_keyframe_selected:
                                        kf.co[0] += offset
                                        kf.handle_left[0] += offset
                                        kf.handle_right[0] += offset

                offset += frames_to_offset

        def offset_light_param():
            sel_ob = bpy.context.selected_objects
            any_keyframe_selected = False
            offset = 0
            if not rev_bool:
                sel_ob = reversed(sel_ob)
            else:
                sel_ob = sel_ob
                    
            for o in sel_ob:
                bpy.context.view_layer.objects.active = o

                if o.data.animation_data:
                    if o.data.animation_data.action:
                        if o.data.animation_data.action.fcurves:
                            for c in o.data.animation_data.action.fcurves:
                                keyframePoints = c.keyframe_points


                                for kf in keyframePoints:
                                    if kf.select_control_point:
                                        any_keyframe_selected = True
                                        kf.co[0] += offset
                                        kf.handle_left[0] += offset
                                        kf.handle_right[0] += offset
                                    if not any_keyframe_selected:
                                        kf.co[0] += offset
                                        kf.handle_left[0] += offset
                                        kf.handle_right[0] += offset

                            offset += frames_to_offset

        def armature_name():
            ob = bpy.context.object
            return ob.name
      
        def bone_keyframes_offset():
            
            sel_bones = bpy.context.selected_pose_bones

            arm_name = armature_name()
            arm = bpy.data.objects[arm_name]
            act_bone = bpy.context.active_pose_bone
            any_keyframe_selected = False
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
                                    if kf.select_control_point:
                                        any_keyframe_selected = True
                                        kf.co[0] += offset
                                        kf.handle_left[0] += offset
                                        kf.handle_right[0] += offset
                                    if not any_keyframe_selected:
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
        if act_ob.type == 'LIGHT':
            offset_light_param()

        if act_ob.mode == 'POSE':
            bone_keyframes_offset()

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
            any_keyframe_selected = False

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
                                    if kf.select_control_point:
                                        any_keyframe_selected = True
                                        kf.co[0] += offset
                                        kf.handle_left[0] += offset
                                        kf.handle_right[0] += offset
                                    if not any_keyframe_selected:
                                        kf.co[0] += offset
                                        kf.handle_left[0] += offset
                                        kf.handle_right[0] += offset

                        offset += frames_to_offset

        select_similar_by_act_bone_name()
        bone_keyframes_offset()


        return {'FINISHED'}
  
class OBJECT_OT_clean_keyframes(bpy.types.Operator):
    '''Offset Animated - Location, Rotation, Scale'''
    bl_idname = "clean.keyframes"
    bl_label = "Clean Up Keyframes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode != 'EDIT' and
                len(context.selected_objects) != 0)

    def execute(self, context):
        selected_objects = context.selected_objects
        selected_bone = context.selected_pose_bones

        # Iterate through the selected objects
        for obj in selected_objects:
            if obj.mode == "POSE":
                for b in selected_bone:
                    act_bone_name = b.name

                    if obj.animation_data:
                        # Get the animation data and action
                        anim_data = obj.animation_data
                        action = anim_data.action

                        # Check if the action exists
                        if action:
                            # Get the F-Curves of the action
                            fcurves = action.fcurves

                            # Iterate through the F-Curves
                            for fc in fcurves:
                                # Get the keyframes of the F-Curve
                                if act_bone_name in fc.data_path:

                                    keyframes = fc.keyframe_points

                                    # Iterate through the keyframes in reverse order
                                    for i in reversed(range(len(keyframes))):
                                        # Check if the keyframe has no transition
                                        if i > 0 and i < len(keyframes) - 1:
                                            kf_prev = keyframes[i-1]
                                            kf_current = keyframes[i]
                                            kf_next = keyframes[i+1]
                                            if kf_prev.co[1] == kf_current.co[1] == kf_next.co[1]:
                                                # Remove the keyframe with no transition
                                                keyframes.remove(kf_current)
            else:
                # Check if the object has animation data
                if obj.animation_data:
                    # Get the animation data and action
                    anim_data = obj.animation_data
                    action = anim_data.action

                    # Check if the action exists
                    if action:
                        # Get the F-Curves of the action
                        fcurves = action.fcurves

                        # Iterate through the F-Curves
                        for fc in fcurves:
                            # Get the keyframes of the F-Curve
                            keyframes = fc.keyframe_points

                            # Iterate through the keyframes in reverse order
                            for i in reversed(range(len(keyframes))):
                                # Check if the keyframe has no transition
                                if i > 0 and i < len(keyframes) - 1:
                                    kf_prev = keyframes[i-1]
                                    kf_current = keyframes[i]
                                    kf_next = keyframes[i+1]
                                    if kf_prev.co[1] == kf_current.co[1] == kf_next.co[1]:
                                        # Remove the keyframe with no transition
                                        keyframes.remove(kf_current)

        return {'FINISHED'}

class OBJECT_OT_step_selected_keyframes(bpy.types.Operator):
    '''Offset Animated - Location, Rotation, Scale'''
    bl_idname = "step.keyframes"
    bl_label = "Set step Keyframes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.mode != 'EDIT' and
                len(context.selected_objects) != 0)

    def execute(self, context):
        scene = context.scene
        current_frame = context.scene.frame_current
        selected_objects = context.selected_objects
        start = context.scene.frame_start
        end = context.scene.frame_end

        if scene.SetKeyFramesList == "one":
            step = 1
        elif scene.SetKeyFramesList == "two":
            step = 2
        elif scene.SetKeyFramesList == "three":
            step = 3
        elif scene.SetKeyFramesList == "four":
            step = 4

        bpy.ops.wm.console_toggle()

        def setkey(action, obj, frame):
            bpy.context.scene.frame_set(frame)

            data_paths_with_keyframes = []

            if bpy.context.object.mode == 'POSE':
                if bpy.context.object.type == "ARMATURE":
                    for fcurve in action.fcurves:
                        # Check if keyframes exist for the FCurve
                        if fcurve.data_path.startswith(f'pose.bones["{obj.name}"]'):
                            if fcurve.keyframe_points:
                                for keyframe in fcurve.keyframe_points:
                                    if keyframe.select_control_point:
                                        data_paths_with_keyframes.append(fcurve.data_path)

                    data_paths_with_keyframes = list(set(data_paths_with_keyframes))

                    if data_paths_with_keyframes:
                        for data_path in data_paths_with_keyframes:
                            data_path = data_path.replace(f'pose.bones["{bone.name}"].', '')
                            obj.keyframe_insert(data_path=data_path, frame=frame)

                    else:      
                        for fcurve in action.fcurves:                  
                            if fcurve.data_path.startswith(f'pose.bones["{obj.name}"]'):
                                if fcurve.keyframe_points:
                                    data_paths_with_keyframes.append(fcurve.data_path)

                        data_paths_with_keyframes = list(set(data_paths_with_keyframes))

                        if data_paths_with_keyframes:
                            for data_path in data_paths_with_keyframes:
                                data_path = data_path.replace(f'pose.bones["{bone.name}"].', '')
                                obj.keyframe_insert(data_path=data_path, frame=frame)

            elif bpy.context.object.mode == "OBJECT":
                # Iterate over the FCurves
                for fcurve in action.fcurves:
                    # Check if keyframes exist for the FCurve
                    if fcurve.keyframe_points:
                        for keyframe in fcurve.keyframe_points:
                            if keyframe.select_control_point:
                                data_paths_with_keyframes.append(fcurve.data_path)

                data_paths_with_keyframes = list(set(data_paths_with_keyframes))

                if data_paths_with_keyframes:
                    for data_path in data_paths_with_keyframes:
                        obj.keyframe_insert(data_path=data_path, frame=frame)

                else:
                    for fcurve in action.fcurves:
                        if fcurve.keyframe_points:
                            data_paths_with_keyframes.append(fcurve.data_path)

                    data_paths_with_keyframes = list(set(data_paths_with_keyframes))

                    if data_paths_with_keyframes:
                        for data_path in data_paths_with_keyframes:
                            obj.keyframe_insert(data_path=data_path, frame=frame)

        if scene.SetKeyType == "one":
            # Iterate through the selected objects
            for obj in selected_objects:
                if obj.mode == 'POSE':
                    if obj.type == "ARMATURE":
                        animation_data = obj.animation_data
                        # Check if animation data exists
                        if animation_data and animation_data.action:
                            action = animation_data.action
                            selected_bones = [bone for bone in obj.pose.bones if bone.bone.select]

                            for bone in selected_bones:
                                print("Set keyframes Bone: " + bone.name)

                                selected_keyframes = set()
                            
                                for fcurve in action.fcurves:
                                    if fcurve.data_path.startswith(f'pose.bones["{bone.name}"]'):
                                        for keyframe in fcurve.keyframe_points:
                                            if keyframe.select_control_point:
                                                selected_keyframes.add(int(keyframe.co[0]))
                                
                                if selected_keyframes:
                                    # Assuming you have two keyframes selected
                                    start_frame = min(selected_keyframes)
                                    end_frame = max(selected_keyframes)

                                    # Set keyframes every two frames between the start and end frames
                                    for frame in range(start_frame + step, end_frame, step):

                                        setkey(action, bone, frame)

                                else:
                                    # Get the fcurves for the selected bone
                                    for fcurve in action.fcurves:
                                        if fcurve.data_path.startswith(f'pose.bones["{bone.name}"]'):
                                            for keyframe in fcurve.keyframe_points:
                                                selected_keyframes.add(int(keyframe.co[0]))
                                                keyframe.select_control_point = True
                                                keyframe.select_left_handle = True
                                                keyframe.select_right_handle = True
                                        
                                    start_frame = min(selected_keyframes)
                                    end_frame = max(selected_keyframes)

                                    # Set keyframes every two frames between the start and end frames
                                    for frame in range(start_frame + step, end_frame, step):

                                        setkey(action, bone, frame)
                                    
                            for fcurve in obj.animation_data.action.fcurves:
                                for keyframe in fcurve.keyframe_points:
                                    if keyframe.select_control_point:
                                        selected_keyframes.add(int(keyframe.co[0]))  

                            max_value = max(selected_keyframes)  # Find the maximum value
                            selected_keyframes.remove(max_value) 
                                
                            for fcurve in obj.animation_data.action.fcurves:
                                for bone in selected_bones:
                                    if fcurve.data_path.startswith(bone.path_from_id()):
                                        for kf in fcurve.keyframe_points:
                                            if int(kf.co[0]) in selected_keyframes:
                                                kf.interpolation = 'CONSTANT'

                elif obj.mode == "OBJECT":
                    print("Set keyframes Object: " + obj.name)

                    selected_keyframes = set()

                    animation_data = obj.animation_data
                    
                    # Check if animation data exists
                    if animation_data and animation_data.action:
                        action = animation_data.action

                        for fcurve in obj.animation_data.action.fcurves:
                            for keyframe in fcurve.keyframe_points:
                                if keyframe.select_control_point:
                                    selected_keyframes.add(int(keyframe.co[0]))

                        if selected_keyframes:
                            # Assuming you have two keyframes selected
                            start_frame = min(selected_keyframes)
                            end_frame = max(selected_keyframes)

                            # Set keyframes every two frames between the start and end frames
                            for frame in range(start_frame + step, end_frame, step):

                                setkey(action, obj, frame)

                        else:
                            # Get the fcurves for the selected bone
                            for fcurve in obj.animation_data.action.fcurves:
                                for keyframe in fcurve.keyframe_points:
                                    selected_keyframes.add(int(keyframe.co[0]))
                                    keyframe.select_control_point = True
                                    keyframe.select_left_handle = True
                                    keyframe.select_right_handle = True
                                
                            start_frame = min(selected_keyframes)
                            end_frame = max(selected_keyframes)

                            # Set keyframes every two frames between the start and end frames
                            for frame in range(start_frame + step, end_frame, step):

                                setkey(action, obj ,frame)
                        
                        for fcurve in obj.animation_data.action.fcurves:
                            for keyframe in fcurve.keyframe_points:
                                if keyframe.select_control_point:
                                    selected_keyframes.add(int(keyframe.co[0]))
                            
                        max_value = max(selected_keyframes)  # Find the maximum value
                        selected_keyframes.remove(max_value) 

                        for fcurve in obj.animation_data.action.fcurves:
                            for kf in fcurve.keyframe_points:
                                if int(kf.co[0]) in selected_keyframes:
                                    kf.interpolation = 'CONSTANT'

        elif scene.SetKeyType == "two":

            frames_range = []
            current = start
            while current <= end:
                frames_range.append(current)
                current += step

            for obj in selected_objects:

                if obj.mode == 'POSE':
                    if obj.type == "ARMATURE":
                        animation_data = obj.animation_data
                        
                        # Check if animation data exists
                        if animation_data and animation_data.action:
                            action = animation_data.action

                            selected_bones = [bone for bone in obj.pose.bones if bone.bone.select]
                            for bone in selected_bones:
                                print("Set keyframes Bones: " + bone.name)

                                selected_keyframes = set()
                            
                                for fcurve in action.fcurves:
                                    if fcurve.data_path.startswith(f'pose.bones["{bone.name}"]'):
                                        for keyframe in fcurve.keyframe_points:
                                            if keyframe.select_control_point:
                                                selected_keyframes.add(int(keyframe.co[0]))
                                
                                if selected_keyframes:
                                    # Assuming you have two keyframes selected
                                    start_frame = min(selected_keyframes)
                                    end_frame = max(selected_keyframes)

                                    for frame in frames_range:
                                        if start_frame <= frame <= end_frame:

                                            setkey(action, bone, frame)

                                else:
                                    # Get the fcurves for the selected bone
                                    for fcurve in action.fcurves:
                                        if fcurve.data_path.startswith(f'pose.bones["{bone.name}"]'):
                                            for keyframe in fcurve.keyframe_points:
                                                selected_keyframes.add(int(keyframe.co[0]))
                                                keyframe.select_control_point = True
                                                keyframe.select_left_handle = True
                                                keyframe.select_right_handle = True
                                                                        
                                    start_frame = min(selected_keyframes)
                                    end_frame = max(selected_keyframes)

                                    for frame in frames_range:
                                        if start_frame <= frame <= end_frame:

                                            setkey(action, bone, frame) 
                    
                            for fcurve in obj.animation_data.action.fcurves:
                                for keyframe in fcurve.keyframe_points:
                                    if keyframe.select_control_point:
                                        selected_keyframes.add(int(keyframe.co[0]))  

                            max_value = max(selected_keyframes)  # Find the maximum value
                            selected_keyframes.remove(max_value) 
                                
                            for fcurve in obj.animation_data.action.fcurves:
                                for bone in selected_bones:
                                    if fcurve.data_path.startswith(bone.path_from_id()):
                                        for kf in fcurve.keyframe_points:
                                            if int(kf.co[0]) in selected_keyframes:
                                                kf.interpolation = 'CONSTANT'

                elif obj.mode == "OBJECT":

                    print("Set keyframes Object: " + obj.name)

                    selected_keyframes = set()

                    animation_data = obj.animation_data
                    
                    # Check if animation data exists
                    if animation_data and animation_data.action:
                        action = animation_data.action

                        for fcurve in obj.animation_data.action.fcurves:
                            for keyframe in fcurve.keyframe_points:
                                if keyframe.select_control_point:
                                    selected_keyframes.add(int(keyframe.co[0]))

                        if selected_keyframes:
                            # Assuming you have two keyframes selected
                            start_frame = min(selected_keyframes)
                            end_frame = max(selected_keyframes)

                            for frame in frames_range:
                                if start_frame <= frame <= end_frame:

                                    setkey(action, obj, frame)

                        else:
                            # Get the fcurves for the selected bone
                            for fcurve in obj.animation_data.action.fcurves:
                                for keyframe in fcurve.keyframe_points:
                                    selected_keyframes.add(int(keyframe.co[0]))
                                    keyframe.select_control_point = True
                                    keyframe.select_left_handle = True
                                    keyframe.select_right_handle = True
                                
                            start_frame = min(selected_keyframes)
                            end_frame = max(selected_keyframes)

                            for frame in frames_range:
                                if start_frame <= frame <= end_frame:

                                    setkey(action, obj, frame)
                                    
                    
                        for fcurve in obj.animation_data.action.fcurves:
                            for keyframe in fcurve.keyframe_points:
                                if keyframe.select_control_point:
                                    selected_keyframes.add(int(keyframe.co[0]))
                            
                        max_value = max(selected_keyframes)  # Find the maximum value
                        selected_keyframes.remove(max_value) 

                        for fcurve in obj.animation_data.action.fcurves:
                            for kf in fcurve.keyframe_points:
                                if int(kf.co[0]) in selected_keyframes:
                                    kf.interpolation = 'CONSTANT'

        bpy.ops.wm.console_toggle()

        context.scene.frame_current = current_frame

        return {'FINISHED'}

class PANEL_PT_Animation_Tool(bpy.types.Panel):
    bl_label = "KEN Action"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = "KEN Action" 
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        if scene.SetKeyFramesList == "one":
            step = context.scene.render.fps/1
        elif scene.SetKeyFramesList == "two":
            step = context.scene.render.fps/2
        elif scene.SetKeyFramesList == "three":
            step = context.scene.render.fps/3
        elif scene.SetKeyFramesList == "four":
            step = context.scene.render.fps/4

        layout = self.layout
        box = layout.box() 
        row = box.row()
        row.label(text='Keyframes', icon='DECORATE_KEYFRAME')
        row.operator("clean.keyframes", text='', icon = "TRASH")
        row = box.row(align=True)
        row.operator("action.copy", text='Copy', icon = "COPYDOWN")
        row.operator("action.paste", text='Paste', icon = "PASTEDOWN").flipped=False
        if context.object.mode == "POSE":
            row.operator("action.paste", text='Flipped', icon = "PASTEFLIPDOWN").flipped=True
        row = box.row()
        row.label(text='Offset Keyframes', icon='ONIONSKIN_ON')
        if context.object.mode == "OBJECT":
            row.operator("object.select_by_name_type", text='' , icon='RESTRICT_SELECT_OFF', emboss = False)
        row = box.row()
        row.prop(context.scene, "anim_offest_frames")
        row.prop(context.scene, "revers_anim_offest", icon = "ARROW_LEFTRIGHT")
        if context.object.mode == "OBJECT":
            row = box.row()
            row.operator("offset.selected_keyframes", text='Set Offset')
            row = box.row(align=True)
            row.scale_y = 1.2
            row.operator("object.offset_location", text='Location')
            row.operator("object.offset_rotation", text='Rotation')
            row.operator("object.offset_scale", text='Scale')
        elif context.object.mode == "POSE":
            row = box.row(align=True)
            row.scale_y = 1.2
            row.operator("object.offset_keyframes_similar_bones", text='Similar', icon='BONE_DATA')
            row.operator("offset.selected_keyframes", text='Selected', icon='RESTRICT_SELECT_OFF')
        row = box.row()
        row.label(text='Step Keyframes', icon='IPO_CONSTANT')
        row = box.row()
        row.prop(context.scene, "SetKeyType", expand = True)
        row = box.row()
        row.prop(context.scene, "SetKeyFramesList", text=str(round(step)) +"fps Step")
        row = box.row()
        row.operator("step.keyframes", text='Step Keyframes')

        #---------------------------- Add Cycle Modifier ---------------------------------

classes = (
            OBJECT_OT_select_by_name_type,
            OBJECT_OT_offset_selected_keyframes,
            OBJECT_OT_offset_location,
            OBJECT_OT_offset_rotation,
            OBJECT_OT_offset_scale,
            OBJECT_OT_offset_keyframes_similar_bones,
            OBJECT_OT_step_selected_keyframes,
            OBJECT_OT_clean_keyframes,
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

    bpy.types.Scene.SetKeyType = bpy.props.EnumProperty(
        default='one',
        items=[('one', 'Local', ''),
                ('two', 'Gobal', ''),
                ])

    bpy.types.Scene.SetKeyFramesList = bpy.props.EnumProperty(
        default='two',
        items=[('one', '1/1', ''),
                ('two', '1/2', ''),
                ('three', '1/3', ''),
                ('four', '1/4', ''),
                ])

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.revers_anim_offest
    del bpy.types.Scene.anim_offest_frames


if __name__ == "__main__":
    register() 