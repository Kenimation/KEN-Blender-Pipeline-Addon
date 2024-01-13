import bpy
import os
from . import AnimeDefs
from ..AssetsUI import assetsDefs
from bpy.props import (StringProperty,
                        IntProperty)

def anime_rig_get_preference(type):
    # select the rig
    rig = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = rig
        # props from user preferencesSettings.cfg
            #   arm ik
            #   flip bone
    flip_bone = assetsDefs.readTextPrefs(16)
    if flip_bone == "False":
        rig.flipBone = 0
    else:
        rig.flipBone = 1
            #   arm ik
    arm_ik = assetsDefs.readTextPrefs(19)
    if arm_ik == "IK":
        arm_ik = 1
    else:
        arm_ik = 0
    rig.Arm_IK_Left = arm_ik
    rig.Arm_IK_Right = arm_ik
        # leg ik
    leg_ik = assetsDefs.readTextPrefs(22)
    if leg_ik == "IK":
        leg_ik = 1
    else:
        leg_ik = 0
    rig.Leg_IK_Left = leg_ik
    rig.Leg_IK_Right = leg_ik

    rig_scale = assetsDefs.readTextPrefs(13)
    rig.RigScale = float(rig_scale)

class Append_TheAnimeRigKENFemale(bpy.types.Operator):
    bl_idname = "append.kenanimefemale"
    bl_label = "KEN Anime Rig [Female]"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        script_file = os.path.realpath(os.path.dirname(__file__))

        script_directory = os.path.dirname(script_file)
        script_directory = os.path.join(script_directory,"Assets" , "Rigs", "Anime")
        script_directory = os.path.normpath(script_directory)

        blendfile = os.path.join(script_directory, "KEN Anime Female Rig.blend")
        section = "Collection"
        obj = "KEN Anime Female Rig"
        filepath  = os.path.join(blendfile,section,obj)
        directory = os.path.join(blendfile,section)
        filename  = obj
        bpy.ops.wm.append(filepath=filepath,filename=filename,directory=directory,link=False,active_collection=False)

        type = "female"
        anime_rig_get_preference(type)

        bpy.ops.object.select_all(action='DESELECT')

        context.scene.view_settings.view_transform = 'Standard'
        self.report({'INFO'}, "KEN Anime Rig has been appended! | Scene Color Space set to Standard")
        return {'FINISHED'}

class Anime_BakeLineArt(bpy.types.Operator):
    bl_idname = "anime.bake_lineart_all"
    bl_label = "Bake All LineArt"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        start = context.scene.frame_start
        end = context.scene.frame_end

        scene = context.scene

        bpy.ops.wm.console_toggle()

        # Get all the markers in the scene
        markers = scene.timeline_markers

        # Iterate over the markers
        camera_mark_list = []

        # Iterate over the markers
        for marker in markers:
            if marker.camera:
                camera_mark_list.append(marker.frame)

        camera_mark_list.append(end)

        bake_list = [(camera_mark_list[i], camera_mark_list[i+1]) for i in range(len(camera_mark_list)-1)]

        print("Baking List:" + str(bake_list))

        for index, list in enumerate(bake_list):
            start_bake, end_bake = bake_list[index]
            print("Start Baking LineArt: " + "Start " + str(start_bake) + "frames" + " End " + str(end_bake - 1) + "frames")
            print("LineArt Baking...")
            context.scene.frame_start = start_bake
            context.scene.frame_end = end_bake - 1
            bpy.ops.object.lineart_bake_strokes_all()
            print("Finish Baking LineArt: " + "Start " + str(start_bake) + "frames" + " End " + str(end_bake - 1) + "frames")

        bpy.ops.wm.console_toggle()

        context.scene.frame_start = start
        context.scene.frame_end = end

        self.report({'INFO'}, "Render LineArt Baking!")
        
        return {'FINISHED'}

class Anime_SnapRender(bpy.types.Operator):
    bl_idname = "render.anime_snap"
    bl_label = "Render Anime Snap"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        original_frame = context.scene.frame_current
        output_path = context.scene.render.filepath
        start = context.scene.frame_start
        end = context.scene.frame_end
        frameRate = context.scene.render.fps
        colorspace = context.scene.sequencer_colorspace_settings.name
        frames = []

        bpy.ops.wm.console_toggle()

        bpy.ops.render.view_show('INVOKE_DEFAULT')

        markers = context.scene.timeline_markers
        for marker in markers:
            frames.append(marker.frame)

        for obj in context.scene.objects:
            if obj.type != 'GPENCIL':
                try:
                    for fcurve in obj.animation_data.action.fcurves:
                        for keyframe_point in fcurve.keyframe_points:
                            x, y = keyframe_point.co
                            if x >= start and x <= end and x not in frames:
                                frames.append(int(x))
                except:
                    continue

        frames.append(start)
        frames.append(end)
        frames = list(set(frames))
        frames = sorted(frames)

        directory, filename = os.path.split(output_path)
        output_directory = directory.replace("\\\\", "\\")
        output_file = os.path.join(output_directory, filename + "_FrameSheet" + '.txt')
        
        current_frame_list = []

        for index, frame in enumerate(frames):
            bpy.context.scene.frame_current = frame
            order_number = index + 1
            self.report({'INFO'}, "Render Frame " +"%04d" % order_number + " | " + "F" + "%04d" % frame)
            rendername = filename + "_" + "%04d" % order_number
            bpy.context.scene.render.filepath = os.path.join(directory, rendername)
            bpy.ops.render.render(write_still=True)
            print("Render Finish: " + str(frame) + "frames")
            current_frame_list.append(frame)
            with open(output_file, 'w') as file:
                file.write("- " + filename + " Render Frame Sheet -" + '\n')
                file.write("Color Space: " + str(colorspace) + '\n')
                file.write("Frame Rate: " + str(frameRate) + '\n')
                file.write("Total Frames: " + str(len(current_frame_list)) + "/" + str(len(frames)) + '\n')
                file.write(str(current_frame_list) + '\n')

        with open(output_file, 'w') as file:
            file.write("- " + filename + " Render Frame Sheet -" + '\n')
            file.write("Color Space: " + str(colorspace) + '\n')
            file.write("Frame Rate: " + str(frameRate) + '\n')
            file.write("Total Frames: " + str(len(current_frame_list)) + '\n')
            file.write(str(current_frame_list) + '\n')

        bpy.context.scene.frame_current = original_frame
        bpy.context.scene.render.filepath = output_path

        bpy.ops.wm.console_toggle()
        
        self.report({'INFO'}, "Render Finished! | File:" + str(output_path))
        
        return {'FINISHED'}

class Anime_SnapRender_Batch(bpy.types.Operator):
    bl_idname = "render.anime_snap_batch"
    bl_label = "Batch Render Anime Snap"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        project_files = [
            "/path/to/project1.blend",
            "/path/to/project2.blend",
            "/path/to/project3.blend",
            # Add more project file paths as needed
        ]
        for project_file in project_files:
            bpy.ops.wm.open_mainfile(filepath=project_file)
            bpy.ops.render.anime_snap()
        return {'FINISHED'}

classes = (
            Append_TheAnimeRigKENFemale,
            Anime_BakeLineArt,
            Anime_SnapRender,
            Anime_SnapRender_Batch,
          )

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()