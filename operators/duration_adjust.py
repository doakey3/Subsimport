import bpy
from .tools.get_text_strips import get_text_strips

class SEQUENCER_OT_duration_x_2(bpy.types.Operator):
    bl_label = 'Dur x 2'
    bl_idname = 'sequencerextra.duration_x_two'
    bl_description = 'Make all text strips in subtitle edit channel twice as long'

    @classmethod
    def poll(self, context):
        scene = context.scene
        try:
            text_strips = get_text_strips(scene)

            if len(text_strips) > 0:
                return True
            else:
                return False
        except AttributeError:
            return False

    def execute(self, context):
        scene = context.scene
        fps = scene.render.fps / scene.render.fps_base
        text_strips = get_text_strips(scene)

        text_strips = list(reversed(text_strips))
        for strip in text_strips:
            strip.frame_final_end = strip.frame_final_end * 2
            strip.frame_final_start = strip.frame_final_start * 2

        return {"FINISHED"}

class SEQUENCER_OT_duration_x_half(bpy.types.Operator):
    bl_label = 'Dur / 2'
    bl_idname = 'sequencerextra.duration_x_half'
    bl_description = 'Make all text strips in subtitle edit channel half as long.\nEach strip must be >=2 frames long for this to work.'

    @classmethod
    def poll(self, context):
        scene = context.scene
        try:
            text_strips = get_text_strips(scene)

            if len(text_strips) > 0:
                for strip in text_strips:
                    if strip.frame_final_duration < 2:
                        return False
                return True
            else:
                return False
        except AttributeError:
            return False

    def execute(self, context):
        scene = context.scene
        fps = scene.render.fps / scene.render.fps_base
        text_strips = get_text_strips(scene)

        for strip in text_strips:
            strip.frame_final_end = strip.frame_final_end / 2
            strip.frame_final_start = strip.frame_final_start / 2

        return {"FINISHED"}
