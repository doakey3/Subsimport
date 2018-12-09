import bpy

class SEQUENCER_OT_select_channel_right(bpy.types.Operator):
    bl_label = 'Select Channel Right'
    bl_idname = 'sequencerextra.select_channel_right'
    bl_description = 'Select all strips to the right of the CTI on the Subtitle Edit Channel'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        scn = context.scene
        if scn and scn.sequence_editor:
            return scn.sequence_editor.sequences
        else:
            return False

    def execute(self, context):
        scene = context.scene
        bpy.ops.sequencer.select_all(action="DESELECT")

        all_strips = list(sorted(scene.sequence_editor.sequences,
            key=lambda x: x.frame_start))

        for strip in all_strips:
            if strip.channel == scene.subtitle_edit_channel:
                if strip.frame_final_end > scene.frame_current:
                    strip.select = True

        return {'FINISHED'}

class SEQUENCER_OT_select_channel_left(bpy.types.Operator):
    bl_label = 'Select Channel Left'
    bl_idname = 'sequencerextra.select_channel_left'
    bl_description = 'Select all strips to the right of the CTI on the Subtitle Edit Channel'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        scn = context.scene
        if scn and scn.sequence_editor:
            return scn.sequence_editor.sequences
        else:
            return False

    def execute(self, context):
        scene = context.scene
        bpy.ops.sequencer.select_all(action="DESELECT")

        all_strips = list(sorted(scene.sequence_editor.sequences,
            key=lambda x: x.frame_start))

        for strip in all_strips:
            if strip.channel == scene.subtitle_edit_channel:
                if strip.frame_final_start < scene.frame_current:
                    strip.select = True

        return {'FINISHED'}
