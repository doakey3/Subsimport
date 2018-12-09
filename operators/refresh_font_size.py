import bpy

from .tools.get_text_strips import get_text_strips

class SEQUENCER_OT_refresh_font_size(bpy.types.Operator):
    bl_label = ""
    bl_idname = 'sequencerextra.refresh_font_size'
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

        return {"FINISHED"}
