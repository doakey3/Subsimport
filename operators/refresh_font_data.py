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
            strip.color = scene.subtitle_font_color
            strip.use_shadow = scene.subtitle_font_shadow
            strip.shadow_color = scene.subtitle_font_shadow_color
            strip.font = get_font(scene.subtitle_font)
            strip.location[0] = scene.subtitle_font_xloc
            strip.location[1] = scene.subtitle_font_yloc
            strip.align_x = scene.subtitle_anchor_x
            strip.align_y = scene.subtitle_anchor_y
            strip.wrap_width = scene.subtitle_wrap_width
            # bpy.types.TextSequence.TextSequence(strip).wrap_width = scene.subtitle_wrap_width

        return {"FINISHED"}
