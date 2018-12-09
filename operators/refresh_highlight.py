import bpy

from .tools.get_text_strips import get_text_strips

class SEQUENCER_OT_refresh_highlight(bpy.types.Operator):
    bl_label = ""
    bl_idname = 'sequencerextra.refresh_highlight'
    bl_description = "Refresh the color of highlighted words"

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
            strip.color[0] = scene.enhanced_subs_color[0]
            strip.color[1] = scene.enhanced_subs_color[1]
            strip.color[2] = scene.enhanced_subs_color[2]

        return {"FINISHED"}
