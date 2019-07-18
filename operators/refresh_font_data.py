import bpy

from .tools.get_text_strips import get_text_strips
from .tools.get_font import get_font


class SEQUENCER_OT_refresh_font_data(bpy.types.Operator):
    bl_label = "Refresh Font Data"
    bl_idname = 'sequencerextra.refresh_font_data'
    bl_description = "Refresh the font size for all text strips on the edit channel"

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

        text_strips = get_text_strips(scene)

        for strip in text_strips:
            strip.font_size = scene.subtitle_font_size
            strip.font = get_font(scene.subtitle_font)
            strip.location[1] = scene.subtitle_font_height

        return {"FINISHED"}
