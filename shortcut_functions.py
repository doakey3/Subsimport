import bpy


class ShiftFrameStart(bpy.types.Operator):
    bl_idname = "sequencerextra.shift_frame_start"
    bl_label = "Shift Frame Start of Next Text Strip"
    bl_description = "Shifts frame start of text strip to the current frame"

    def execute(self, context):
        scene = context.scene
        current_frame = scene.frame_current
        edit_channel = scene.subtitle_edit_channel
        seq = bpy.context.scene.sequence_editor
        if seq:
            all_strips = list(sorted(seq.sequences_all,
                                     key=lambda x: x.frame_start))
            text_strips = []
            for strip in all_strips:
                if strip.type == "TEXT" and strip.channel == edit_channel:
                    text_strips.append(strip)
            if not len(text_strips) == 0:
                for i in range(len(text_strips)):
                    if (text_strips[i].frame_final_start < current_frame and
                            text_strips[i].frame_final_end > current_frame):
                        if not text_strips[i].name.startswith('[locked start]'):
                            text_strips[i].frame_final_start = current_frame
                            return {"FINISHED"}
                        else:
                            return {"FINISHED"}
                    elif (text_strips[i].frame_final_start >= current_frame and
                            text_strips[i].frame_final_end > current_frame and
                            i < len(text_strips)):
                        if not text_strips[i].name.startswith('[locked start]'):
                            text_strips[i].frame_final_start = current_frame
                            return {"FINISHED"}
                        else:
                            return {"FINISHED"}

            else:
                return {"FINISHED"}
        else:
            return {"FINISHED"}

        return {"FINISHED"}


class ShiftFrameEnd(bpy.types.Operator):
    bl_idname = "sequencerextra.shift_frame_end"
    bl_label = "Shift Frame End of Next Text Strip"
    bl_description = "Shifts the frame end of text strip to the current frame"

    def execute(self, context):
        scene = context.scene
        current_frame = scene.frame_current
        seq = bpy.context.scene.sequence_editor
        edit_channel = scene.subtitle_edit_channel
        if seq:
            all_strips = list(sorted(seq.sequences_all,
                                     key=lambda x: x.frame_start))
            text_strips = []
            for strip in all_strips:
                if strip.type == "TEXT" and strip.channel == edit_channel:
                    text_strips.append(strip)
            if not len(text_strips) == 0:
                for i in range(len(text_strips)):
                    if (i == 0 and
                            text_strips[i].frame_final_start >= current_frame):
                        return {"FINISHED"}
                    elif (text_strips[i].frame_final_start < current_frame and
                            text_strips[i].frame_final_end > current_frame):
                        
                        if not text_strips[i].name.startswith('[locked end]'):
                            text_strips[i].frame_final_end = current_frame
                            return {"FINISHED"}
                        else:
                            return {"FINISHED"}
                    
                    elif (text_strips[i].frame_final_start >= current_frame and
                            text_strips[i].frame_final_end > current_frame):
                        
                        if not text_strips[i - 1].name.startswith('[locked end]'):
                            text_strips[i - 1].frame_final_end = current_frame
                            return {"FINISHED"}
                        else:
                            return {"FINISHED"}
                    
                    elif i == len(text_strips) - 1:
                        if not text_strips[i].name.startswith('[locked end]'):
                            text_strips[i].frame_final_end = current_frame
                            return {"FINISHED"}
                        else:
                            return {"FINISHED"}

                return {"FINISHED"}
            else:
                return {"FINISHED"}
        else:
            return {"FINISHED"}

        return {"FINISHED"}


class ShiftFrameStartEnd(bpy.types.Operator):
    bl_idname = "sequencerextra.shift_frame_start_end"
    bl_label = "Shift Frame End then Frame start of next"
    bl_description = "Like pressing D then F"

    def execute(self, context):
        bpy.ops.sequencerextra.shift_frame_start()
        bpy.ops.sequencerextra.shift_frame_end()

        return {"FINISHED"}


class ShiftFrameEndStart(bpy.types.Operator):
    bl_idname = "sequencerextra.shift_frame_end_start"
    bl_label = "Shift Frame End then Frame start of next"
    bl_description = "Like pressing F then D"

    def execute(self, context):
        bpy.ops.sequencerextra.shift_frame_end()
        bpy.ops.sequencerextra.shift_frame_start()

        return {"FINISHED"}


